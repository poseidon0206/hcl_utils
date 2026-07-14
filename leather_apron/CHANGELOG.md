# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.7.2] - 2026-07-14

### Added

- Module, class and method docstrings in `enc_vid.py`
  (Sphinx `:param:`/`:return:` style).
- `CHANGELOG.md`.

### Changed

- README rewritten with Deployment, Config and Running-the-scripts
  sections.

### Deprecated

- `rename_subbed.py` — a one-off tool to mass rename existing "subbed"
  videos; everything is renamed. Kept in the repo for record keeping.

## [1.7.1] - 2025-11-18

### Changed

- Updated the `uv run` command in `enc_vid.sh` to install the modules
  from `requirements.txt` via `--with-requirements`.

## [1.7.0] - 2025-10-29

### Added

- uv-based packaging: `pyproject.toml`, `uv.lock` and `.python-version`
  (Python 3.14), with installation instructions in the README.

### Changed

- `enc_vid.py` shebang runs through `uv run`; `enc_vid.sh` adjusted
  accordingly.

## [1.6.1] - 2025-09-25

### Changed

- Suppressed ffmpeg info output (log level raised to warning).

## [1.6.0] - 2025-04-05

### Added

- `rename_subbed.py` to rename "subbed" folders and files, added to the
  repo for record keeping.

## [1.5.1] - 2024-06-18

### Changed

- Updated datetime calls to timezone-aware `datetime.now(tz=timezone.utc)`.

## [1.5.0] - 2023-04-18

### Changed

- x265 encoding now uses the hardware `hevc_videotoolbox` encoder.
- Bitrate is specified in KB.

## [1.4.3] - 2023-04-15

### Fixed

- Updated the ffmpeg path to the Apple-silicon Homebrew directory
  (`/opt/homebrew/bin`).

## [1.4.2] - 2023-01-29

### Changed

- Default logger output only displays the encoding delta; start and
  finish times moved to debug level.

## [1.4.1] - 2022-03-21

### Fixed

- Corrected the requirement entries.

## [1.4.0] - 2022-03-21

### Removed

- `fancy_logger` moved out to a stand-alone repo
  (github.com/poseidon0206/fancy_logger) and is now installed via pip
  requirements.

## [1.3.2] - 2022-01-16

### Changed

- Hidden the ffmpeg banner.

## [1.3.1] - 2022-01-15

### Changed

- Log messages go through `fancy_logger`.

## [1.3.0] - 2022-01-14

### Added

- Fancy logger for `enc_vid.py`.
- `--x264` option to encode with x264.
- `--fake` and `--verbose` options.

### Changed

- Default video encoder is x265 instead of x264.

## [1.2.1] - 2021-09-08

### Changed

- Removed hardcoding.

## [1.2.0] - 2021-03-20

### Added

- Check for the ffmpeg binary.
- Stop when the rip does not exit zero.

### Changed

- Methods take kwargs instead of named args; some methods renamed.

## [1.1.0] - 2020-05-30

### Added

- Path to ffmpeg.
- More checks on the subprocess.
- Default input and output files.

## [1.0.0] - 2019-08-14

### Added

- Initial release: `enc_vid.py` video encoder and `enc_vid.sh` batch
  wrapper.
