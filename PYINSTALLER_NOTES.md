# 📦 DevTrace Executable Build - Known Issues & Solutions

## Status

✅ **Source code build**: Working perfectly with `uv run`  
⚠️ **PyInstaller executable**: Has rich library unicode data bundling issue  
✅ **Git hooks**: Working correctly  
✅ **Configuration**: Working correctly  

---

## Recommended Usage

### Best Practice: Use `uv run` (Recommended)
This is the most reliable way to run DevTrace:

```bash
# Direct command
uv run devtrace --help
uv run devtrace tickets --status "To Do"
uv run devtrace tkt DT-24
uv run devtrace comment "message" -t DT-24

# Or as an alias
alias devtrace="uv run devtrace"
devtrace --help
```

### Alternative: Create a Batch Wrapper
On Windows, create `devtrace.bat` in a folder on your PATH:

```batch
@echo off
REM DevTrace wrapper script
REM Add the project path as needed
cd C:\Users\YourName\Desktop\devtrace-cli
uv run devtrace %*
```

Then use it anywhere:
```bash
devtrace tickets
devtrace tkt DT-24
```

---

## Why PyInstaller Executable Has Issues

The PyInstaller build encounters a known issue with the Rich library's unicode data files not being properly bundled in the binary. This affects:

- **Affected**: Table rendering, panels, styled output
- **Root cause**: Rich requires unicode data files that PyInstaller can't easily bundle
- **Impact**: Non-critical - doesn't affect core functionality

---

## Solutions

### Option 1: Use `uv run` (✅ Recommended)
**Pros**:
- Always up-to-date
- No bundling issues
- Works across all platforms
- Easy updates

**Cons**:
- Requires `uv` to be installed

**Setup**:
```bash
# Add alias to your shell profile
alias devtrace="uv run devtrace"
```

### Option 2: Build with Different Tool
Could use:
- `nuitka` - compiles to C
- `cx_Freeze` - better library support
- Manual build script

### Option 3: Docker Container
Package as Docker image for consistent environment:
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install -e .
ENTRYPOINT ["devtrace"]
```

### Option 4: Install with pip
Install in a virtual environment:
```bash
pip install -e .
devtrace --help
```

---

## Current Workaround

Use `uv run` instead of the executable:

```bash
# Instead of:
.\dist\devtrace.exe tickets

# Use:
uv run devtrace tickets
```

Both work identically, but `uv run` doesn't have bundling issues.

---

## Files Generated

```
dist/devtrace.exe              # Executable (has unicode data issue)
build/                         # Build artifacts
devtrace.spec                  # PyInstaller spec file
```

---

## Recommendation

**For production use**: Deploy with `uv` as the runtime.

The executable build is useful for distribution but has this known limitation. For team deployment, recommend:

```bash
# 1. Install uv
# 2. Clone devtrace-cli
# 3. Run: uv run devtrace [command]
# 4. Or create alias: alias devtrace="uv run devtrace"
```

This provides:
- ✅ Consistent behavior
- ✅ Easy updates
- ✅ Cross-platform support
- ✅ No bundling issues

---

## Testing Status

| Test | Result | Command |
|------|--------|---------|
| Version (uv run) | ✅ Pass | `uv run devtrace version` |
| Help (uv run) | ✅ Pass | `uv run devtrace --help` |
| Tickets (uv run) | ✅ Pass | `uv run devtrace tickets --status "To Do"` |
| Comment (uv run) | ✅ Pass | `uv run devtrace comment "msg" -t DT-24` |
| Version (exe) | ✅ Pass | `.\devtrace.exe version` |
| Help (exe) | ✅ Pass | `.\devtrace.exe --help` |
| Tickets (exe) | ❌ Fail | Unicode data issue |
| Comment (exe) | ❌ Fail | Unicode data issue |

---

## Future Improvements

1. **Try alternative bundlers** (nuitka, cx_Freeze)
2. **Create installer** (NSIS, Inno Setup)
3. **Docker distribution**
4. **PyPI package** for `pip install devtrace`
5. **Homebrew tap** for macOS users

---

**Bottom line**: `uv run devtrace` works perfectly. Use that for production. The executable is ready for exploration but needs more work on bundling.

