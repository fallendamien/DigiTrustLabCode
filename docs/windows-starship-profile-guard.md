# Windows Starship profile guard

## Why this exists

Codex command sessions advertise `TERM=dumb`. Starship cannot render its prompt in that terminal mode, so an unconditional `starship init powershell` prints:

```text
[ERROR] - (starship::print): Under a 'dumb' terminal (TERM=dumb).
```

The fix is to initialize Starship only when `TERM` is not `dumb`. Normal interactive terminals keep Starship; automation shells stay quiet.

## Apply on another Windows machine

After pulling this repository, open a fresh PowerShell session in the repo and run:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\ensure-starship-automation-guard.ps1
```

The script is idempotent. It edits only the current user's `$PROFILE`, creates a timestamped backup before changing an existing profile, and does nothing if no unguarded Starship initialization is present.

Open a new terminal pane after the script finishes so the profile is loaded again.

## Verify

In a fresh Codex/automation shell, the output should contain `TERM=dumb` without the Starship error. In a normal interactive terminal, Starship should still render.

## Rollback

Restore the timestamped `*.bak-starship-*` file beside the profile, or remove the guard block manually. The repository script never deletes the backup.
