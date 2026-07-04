import { stdin, stdout, stderr } from 'process';

const ENDPOINT = 'https://digitrust-lab.local/wp-json/bricks-mcp/v1/mcp';
const AUTH = 'Basic YWRtaW46UlBFUiBCelBlIHRMS3UgazRldyB2bEZrIHRhY0E=';
const REQUEST_TIMEOUT_MS = 60000;

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
process.env.NODE_NO_WARNINGS = '1';

// Suppress Node.js warnings on stderr — Claude Desktop may interpret stderr output as a bridge error
process.removeAllListeners('warning');
process.on('warning', () => {});

function log(...args) {
  stderr.write(
    '[bridge] ' +
      args.map(a => (typeof a === 'string' ? a : JSON.stringify(a))).join(' ') +
      '\n',
  );
}

// --- MCP stdio transport: newline-delimited JSON (NDJSON) ---
let readBuffer = Buffer.alloc(0);

function writeMessage(obj) {
  // MCP stdio transport = newline-delimited JSON (one JSON object per line).
  stdout.write(JSON.stringify(obj) + '\n');
}

function tryParseMessages() {
  // Messages are delimited by newlines; a message must not contain embedded newlines.
  while (true) {
    const nlIdx = readBuffer.indexOf('\n');
    if (nlIdx === -1) return; // wait for a complete line
    const line = readBuffer.slice(0, nlIdx).toString('utf8').trim();
    readBuffer = readBuffer.slice(nlIdx + 1);
    if (line) handleMessage(line);
  }
}

stdin.on('data', chunk => {
  readBuffer = Buffer.concat([readBuffer, chunk]);
  tryParseMessages();
});

async function streamSseResponse(response, msg, deadline) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let wroteResponse = false;

  const processLine = line => {
    if (!line.startsWith('data: ')) return false;

    const data = line.slice(6).trim();
    if (!data || data === '[DONE]') return false;

    try {
      const parsed = JSON.parse(data);

      // Inject isError: false for tools/call results that don't have it
      if (parsed.result && parsed.result.content && parsed.result.isError === undefined) {
        parsed.result.isError = false;
      }

      // Downgrade protocol version to match Claude Desktop's expected version
      if (parsed.result && parsed.result.protocolVersion && parsed.result.protocolVersion !== '2024-11-05') {
        log('protocol downgrade', parsed.result.protocolVersion, '-> 2024-11-05');
        parsed.result.protocolVersion = '2024-11-05';
      }

      // Trim large tools/list responses — Claude Desktop has a stdio buffer limit (~8KB)
      // Keep all parameter names (critical for tool calls) but strip aggressively
      if (parsed.result && parsed.result.tools && Array.isArray(parsed.result.tools)) {
        const originalSize = JSON.stringify(parsed).length;
        if (originalSize > 8000) {
          for (const tool of parsed.result.tools) {
            // Truncate description to 60 chars
            if (tool.description && tool.description.length > 60) {
              tool.description = tool.description.substring(0, 60) + '...';
            }
            // Remove annotations, outputSchema, defaults — not needed for tool discovery
            delete tool.annotations;
            delete tool.outputSchema;
            delete tool.defaults;
            if (tool.inputSchema && tool.inputSchema.properties) {
              for (const key of Object.keys(tool.inputSchema.properties)) {
                const prop = tool.inputSchema.properties[key];
                const trimmed = { type: prop.type || 'string' };
                // Only keep enum for 'action' property — other enums (status, type, response_format)
                // are not validated by Claude Desktop and just waste space
                if (key === 'action' && prop.enum) {
                  trimmed.enum = prop.enum;
                }
                tool.inputSchema.properties[key] = trimmed;
              }
              // Strip required to just 'action' — other required fields cause false validation errors
              if (tool.inputSchema.required) {
                tool.inputSchema.required = tool.inputSchema.required.includes('action') ? ['action'] : [];
              }
            }
          }
          log('tools trimmed', originalSize, '->', JSON.stringify(parsed).length);
        }
      }

      writeMessage(parsed);
      wroteResponse = true;
      log(
        'SSE out',
        parsed.id,
        parsed.method || parsed.result ? 'result' : 'error',
        'isError=' + (parsed.result?.isError ?? 'n/a'),
      );
      return parsed.id === msg.id;
    } catch {
      return false;
    }
  };

  // Check if buffer contains a complete data: line (with or without trailing newline)
  const tryProcessBuffer = () => {
    // Split on newlines — last element may be incomplete (no trailing newline)
    const lines = buffer.split(/\r?\n/);
    buffer = lines.pop() || '';

    for (const line of lines) {
      if (processLine(line.trim())) {
        return true;
      }
    }

    // Also try processing the remaining buffer if it looks like a complete data: line
    // (starts with "data: " and contains a complete JSON object ending with "}")
    const remaining = buffer.trim();
    if (remaining.startsWith('data: ') && remaining.endsWith('}')) {
      if (processLine(remaining)) {
        buffer = '';
        return true;
      }
    }

    return false;
  };

  const remaining = () => Math.max(deadline - Date.now(), 0);
  const raceTimeout = () =>
    new Promise((_, reject) => {
      setTimeout(() => reject(new Error('SSE read timeout')), remaining());
    });

  try {
    while (true) {
      const { value, done } = await Promise.race([
        reader.read(),
        raceTimeout(),
      ]);

      if (done) {
        if (buffer.trim()) processLine(buffer.trim());
        return wroteResponse;
      }

      buffer += decoder.decode(value, { stream: true });

      if (tryProcessBuffer()) {
        await reader.cancel();
        return true;
      }
    }
  } finally {
    try {
      await reader.cancel();
    } catch {}
  }
}

async function handleMessage(raw) {
  let msg;
  try {
    msg = JSON.parse(raw);
  } catch {
    return;
  }

  const isNotification = msg.id === undefined || msg.id === null;
  log(
    'in',
    isNotification ? 'notif' : 'req',
    msg.method || msg.id,
    'id=' + (msg.id ?? 'none'),
  );

  // Notifications: fire-and-forget; server never sends a response.
  if (isNotification) {
    fetch(ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: AUTH,
        Accept: 'text/event-stream',
      },
      body: JSON.stringify(msg),
      keepalive: false,
    }).catch(() => {});
    return;
  }

  const deadline = Date.now() + REQUEST_TIMEOUT_MS;

  try {
    const controller = new AbortController();
    
    // Parse _additional_params string into structured arguments
    if (msg.params?.arguments?._additional_params) {
      const paramsStr = msg.params.arguments._additional_params;
      const parsed = {};
      paramsStr.trim().split(/\s+/).forEach(pair => {
        const eqIdx = pair.indexOf('=');
        if (eqIdx > -1) {
          const key = pair.slice(0, eqIdx);
          const val = pair.slice(eqIdx + 1);
          parsed[key] = isNaN(val) || val === '' ? val : Number(val);
        }
      });
      delete msg.params.arguments._additional_params;
      Object.assign(msg.params.arguments, parsed);
      log('params parsed', JSON.stringify(parsed));
    }

    // Use Promise.race so a hung TCP/TLS connection can't outlive our timeout
    const fetchPromise = fetch(ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: AUTH,
        Accept: 'text/event-stream',
      },
      body: JSON.stringify(msg),
      signal: controller.signal,
      keepalive: false,
    });

    const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => {
        controller.abort();
        reject(new Error(`Request timed out after ${REQUEST_TIMEOUT_MS}ms`));
      }, REQUEST_TIMEOUT_MS),
    );

    const response = await Promise.race([fetchPromise, timeoutPromise]);

    // Check HTTP status — non-2xx should be treated as an error
    if (!response.ok) {
      const errText = await response.text().catch(() => '');
      throw new Error(`HTTP ${response.status}: ${errText.slice(0, 200)}`);
    }

    const contentType = response.headers.get('content-type') || '';

    if (contentType.includes('text/event-stream')) {
      await streamSseResponse(response, msg, deadline);
      return;
    }

    const text = await response.text();
    if (text.trim()) {
      try {
        const parsed = JSON.parse(text.trim());
        if (parsed.result && parsed.result.content && parsed.result.isError === undefined) {
          parsed.result.isError = false;
        }
        if (parsed.result && parsed.result.protocolVersion && parsed.result.protocolVersion !== '2024-11-05') {
          parsed.result.protocolVersion = '2024-11-05';
        }
        writeMessage(parsed);
      } catch {}
    }
  } catch (err) {
    log('error', msg.id, err.message);
    writeMessage({
      jsonrpc: '2.0',
      error: { code: -32603, message: err.message },
      id: msg.id ?? null,
    });
  }
}

// Keep the process alive during idle periods — don't let Node exit
// just because there's no pending I/O. Claude Desktop may go minutes
// between tool calls.
const keepalive = setInterval(() => {}, 1 << 30);

stdin.on('end', () => {
  clearInterval(keepalive);
  process.exit(0);
});

// Catch unexpected errors so the bridge doesn't silently crash
process.on('uncaughtException', err => {
  log('uncaughtException', err.message);
});
process.on('unhandledRejection', err => {
  log('unhandledRejection', err?.message || String(err));
});
