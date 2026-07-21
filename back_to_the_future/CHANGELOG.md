# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.3] - 2026-07-14

### Added

- Module, class-method and function docstrings across `BackToTheFuture.py`
  and `great_scott.py` (Sphinx `:param:`/`:return:` style).
- `CHANGELOG.md`.

### Changed

- README rewritten with Deployment, Config and Running-the-scripts sections.

## [1.1.2] - 2019-08-14

### Fixed

- `.gitignore` fix; restored `test_round.py` to the repository.

## [1.1.1] - 2019-08-11

### Changed

- Reformatted `BackToTheFuture.py` and `great_scott.py` to the PEP 8 style
  guide.

## [1.1.0] - 2019-06-20

### Added

- Argument parser (`BackToTheFuture.parse`) with `--year`, `--month`,
  `--number-of-years`, `--monthly` and `--annually` options, used by the
  sample script `great_scott.py`.

## [1.0.1] - 2019-06-20

### Fixed

- Added the extra days from leap years onto the number of days traversed.
- Used floor division when computing the traversal span.

## [1.0.0] - 2019-06-20

### Added

- Initial release: `BackToTheFuture` class, sample scripts `great_scott.py`
  and `test_round.py`, and README.
