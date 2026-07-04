import { spawn } from 'child_process';

const BRIDGE = 'bricks-mcp-bridge.mjs';
const TIMEOUT = 15000;

function sendAndCollect(messages) {
  return new Promise((resolve, reject) => {
    const child = spawn('node', [BRIDGE], {
      stdio: ['pipe', 'pipe', 'pipe'],
      env: { ...process.env, NODE_TLS_REJECT_UNAUTHORIZED: '0', NODE_NO_WARNINGS: '1' }
    });

    let stdoutData = '';
    let stderrData = '';
    const responses = [];
    const timeout = setTimeout(() => {
      child.kill();
      reject(new Error(`Timeout after ${TIMEOUT}ms`));
    }, TIMEOUT);

    child.stdout.on('data', (chunk) => {
      stdoutData += chunk.toString();
      const lines = stdoutData.split('\n');
      stdoutData = lines.pop() || '';
      for (const line of lines) {
        if (line.trim()) {
          try {
            responses.push(JSON.parse(line.trim()));
          } catch {
            responses.push({ _raw: line.trim() });
          }
        }
      }
    });

    child.stderr.on('data', (chunk) => {
      stderrData += chunk.toString();
    });

    child.on('close', (code) => {
      clearTimeout(timeout);
      if (stdoutData.trim()) {
        try {
          responses.push(JSON.parse(stdoutData.trim()));
        } catch {
          responses.push({ _raw: stdoutData.trim() });
        }
      }
      resolve({ responses, stderr: stderrData, exitCode: code });
    });

    for (const msg of messages) {
      child.stdin.write(JSON.stringify(msg) + '\n');
    }

    setTimeout(() => {
      child.stdin.end();
    }, 10000);
  });
}

async function runTest() {
  console.log('=== Bricks MCP Bridge Smoke Test ===\n');

  // Test 1: Initialize
  console.log('Test 1: initialize');
  const initMsg = {
    jsonrpc: '2.0',
    method: 'initialize',
    params: {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: { name: 'smoke-test', version: '1.0' }
    },
    id: 1
  };

  try {
    const result = await sendAndCollect([initMsg]);
    console.log(`  Exit code: ${result.exitCode}`);
    console.log(`  Responses: ${result.responses.length}`);
    if (result.responses.length > 0) {
      const r = result.responses[0];
      console.log(`  Has result: ${!!r.result}`);
      console.log(`  Protocol version: ${r.result?.protocolVersion || 'N/A'}`);
      console.log(`  Server info: ${JSON.stringify(r.result?.serverInfo || 'N/A')}`);
      console.log(`  Capabilities: ${JSON.stringify(r.result?.capabilities || 'N/A')}`);
    }
    console.log(`  STDERR:\n    ${result.stderr.split('\n').join('\n    ')}`);
    console.log();
  } catch (e) {
    console.log(`  FAILED: ${e.message}\n`);
  }

  // Test 2: tools/list (tests response trimming for large payloads)
  console.log('Test 2: tools/list (large response trimming)');
  const listMsg = {
    jsonrpc: '2.0',
    method: 'tools/list',
    params: {},
    id: 2
  };

  try {
    const result = await sendAndCollect([listMsg]);
    console.log(`  Exit code: ${result.exitCode}`);
    console.log(`  Responses: ${result.responses.length}`);
    if (result.responses.length > 0) {
      const r = result.responses[0];
      const tools = r.result?.tools || [];
      console.log(`  Tool count: ${tools.length}`);
      const totalSize = JSON.stringify(r).length;
      console.log(`  Response size: ${totalSize} bytes`);
      if (tools.length > 0) {
        console.log(`  Sample tool: ${tools[0].name}`);
        const hasEnums = tools.some(t => {
          if (!t.inputSchema?.properties) return false;
          return Object.values(t.inputSchema.properties).some(p => p.enum);
        });
        console.log(`  Has enums: ${hasEnums}`);
      }
    }
    console.log(`  STDERR:\n    ${result.stderr.split('\n').join('\n    ')}`);
    console.log();
  } catch (e) {
    console.log(`  FAILED: ${e.message}\n`);
  }

  // Test 3: Tool call — content get_posts
  console.log('Test 3: tools/call — content get_posts');
  const callMsg = {
    jsonrpc: '2.0',
    method: 'tools/call',
    params: {
      name: 'content',
      arguments: {
        action: 'get_posts',
        post_type: 'page',
        posts_per_page: 1
      }
    },
    id: 3
  };

  try {
    const result = await sendAndCollect([callMsg]);
    console.log(`  Exit code: ${result.exitCode}`);
    console.log(`  Responses: ${result.responses.length}`);
    if (result.responses.length > 0) {
      const r = result.responses[0];
      console.log(`  Has result: ${!!r.result}`);
      console.log(`  isError: ${r.result?.isError}`);
      const content = r.result?.content;
      if (content && Array.isArray(content)) {
        const text = content[0]?.text || '';
        try {
          const parsed = JSON.parse(text);
          console.log(`  Results: ${Array.isArray(parsed) ? parsed.length : 'N/A'} items`);
        } catch {
          console.log(`  Content preview: ${text.substring(0, 100)}...`);
        }
      }
    }
    console.log(`  STDERR:\n    ${result.stderr.split('\n').join('\n    ')}`);
    console.log();
  } catch (e) {
    console.log(`  FAILED: ${e.message}\n`);
  }

  // Test 4: Multi-message sequence (initialize + notification + tools/list)
  console.log('Test 4: Multi-message sequence (init + notif + tools/list)');
  const initNotif = { jsonrpc: '2.0', method: 'notifications/initialized' };
  const initReq = {
    jsonrpc: '2.0',
    method: 'initialize',
    params: {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: { name: 'smoke-test', version: '1.0' }
    },
    id: 10
  };
  const listReq = {
    jsonrpc: '2.0',
    method: 'tools/list',
    params: {},
    id: 11
  };

  try {
    const result = await sendAndCollect([initReq, initNotif, listReq]);
    console.log(`  Exit code: ${result.exitCode}`);
    console.log(`  Responses: ${result.responses.length}`);
    for (let i = 0; i < result.responses.length; i++) {
      const r = result.responses[i];
      console.log(`  Response ${i}: id=${r.id}, hasResult=${!!r.result}, isError=${r.result?.isError ?? 'N/A'}`);
    }
    console.log(`  STDERR:\n    ${result.stderr.split('\n').join('\n    ')}`);
    console.log();
  } catch (e) {
    console.log(`  FAILED: ${e.message}\n`);
  }

  console.log('=== Smoke Test Complete ===');
}

runTest().catch(console.error);
