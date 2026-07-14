# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.3] - 2026-07-14

### Fixed

- Use a raw string for the release-pattern regex in `qrelease.py`,
  silencing Python's `SyntaxWarning: "\d" is an invalid escape sequence`.
  The matched pattern is unchanged.

## [1.3.2] - 2026-07-14

### Added

- Module and class docstrings across `qrelease.py`, `QRelease2.py` and
  `get_rels.py` (Sphinx `:param:`/`:return:` style for the new ones).
- `CHANGELOG.md`.

### Changed

- README rewritten with Deployment, Config (public API) and
  Running-the-scripts sections.

## [1.3.1] - 2024-06-18

### Changed

- Bumped `tabulate` from 0.8.7 to 0.9.0 in `requirements.txt`.

## [1.3.0] - 2020-12-01

### Added

- `ghosts_of_christmas` attribute on `QRelease2`, a sorted list of past,
  present and future releases.

## [1.2.0] - 2020-09-08

### Added

- `folder_str` attribute (`YYYY_MM`) on the `Quarter` object.

## [1.1.0] - 2020-09-08

### Added

- `QRelease2` can obtain more than 2 previous/next releases via the
  `num_rels` parameter.
- `requirements.txt` with pinned dependencies.

### Changed

- Updated README and `get_rels.py` to demonstrate the new features.

## [1.0.2] - 2019-08-12

### Changed

- Added missing trailing newline to `get_rels.py`.

## [1.0.1] - 2019-08-11

### Changed

- Reformatted code to the PEP 8 style guide.

## [1.0.0] - 2019-06-20

### Added

- Initial release: `QRelease` and `QRelease2` classes, sample script
  `get_rels.py`, and README.
