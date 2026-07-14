# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2026-07-14

### Added

- Module, class and method docstrings across `animate_frames.py`
  (Sphinx `:param:`/`:return:` style).
- `CHANGELOG.md`.

### Changed

- README rewritten with Deployment, Config and Running-the-scripts
  sections.

## [1.0.2] - 2025-10-22

### Changed

- Updated the animate command from the ImageMagick 6 `convert` syntax to
  the ImageMagick 7 `magick` command.

## [1.0.1] - 2022-01-10

### Changed

- Changed the interpreter shebang from a hardcoded venv path to
  `/usr/bin/env python3`.

## [1.0.0] - 2019-08-14

### Added

- Initial release: `FrameAnimator` class and CLI in `animate_frames.py`,
  README, and `requirements.txt`.
