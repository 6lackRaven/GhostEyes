# GhostEyes - CHANGELOG

## [v2.1.0] - 2025-07-25
### Added
- **`--version`** flag to display version and author.
- **`--examples`** flag to show example commands.
- **`--quiet`** flag to suppress verbose logs and only show essential output.
- **`--output`** option to allow custom output filenames for scans.
- **Colorized banner** showing GhostEyes version and author (`6lackRaven`).
- Improved error handling with cleaner messages.
- Support for **directory brute-forcing** via `--bruteforce` (under `web` command).
- Clearer structured CLI with short help (`-h`) and long help (`--help`).
- Updated code structure to remove nested `asyncio.run()` issues.

### Changed
- Updated `core/scanner.py` to use async-friendly initialization (no nested `asyncio.run()`).
- Improved CLI output formatting with colors and cleaner messages.
- Default output files changed to `scan_net.json` or `scan_web.json` unless `--output` is specified.

### Fixed
- Fixed `RuntimeWarning: coroutine 'get_interface_details' was never awaited`.
- Fixed crash on `asyncio.run()` when running under certain Python environments.

### Future Roadmap (v3+)
- Plugin system for modular recon scripts.
- Structured JSON logging.
- REST API or Web UI mode.
- Parallelization improvements for faster scans.
