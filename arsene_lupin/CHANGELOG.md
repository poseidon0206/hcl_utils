# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.18] - 2026-07-14

### Added

- Module and function docstrings in `grab_pix_from_html.py`
  (Sphinx `:param:`/`:return:` style).
- `CHANGELOG.md`.

### Changed

- README rewritten with Deployment, Config and Running-the-scripts
  sections.

## [1.2.17] - 2026-06-23

### Security

- Bumped `idna` from 3.7 to 3.15 (dependabot).

## [1.2.16] - 2026-04-08

### Security

- Bumped `requests` from 2.32.4 to 2.33.0 (dependabot).

## [1.2.15] - 2025-06-24

### Security

- Bumped `requests` (dependabot).

## [1.2.14] - 2025-06-17

### Security

- Dependency bump via GitHub dependabot.

## [1.2.13] - 2024-07-07

### Changed

- Bumped the `certifi` module version.

## [1.2.12] - 2024-06-18

### Changed

- Updated datetime calls to timezone-aware `datetime.now(tz=timezone.utc)`.
- Updated `urllib3` version.

## [1.2.11] - 2024-06-11

### Security

- Bumped `requests` to 2.32.3.

## [1.2.10] - 2024-04-12

### Removed

- Unnecessary packages dropped from `requirements.txt`.

### Changed

- Updated the required packages.

## [1.2.9] - 2024-04-12

### Security

- Bumped `idna` from 3.4 to 3.7 (dependabot).

## [1.2.8] - 2023-10-17

### Security

- Bumped `urllib3` from 2.0.6 to 2.0.7 (dependabot).

## [1.2.7] - 2023-10-03

### Security

- Dependabot dependency updates.

## [1.2.6] - 2023-08-15

### Changed

- Requirement pins use `>=` instead of `==`.

## [1.2.5] - 2023-07-25

### Security

- Bumped `certifi` from 2022.12.7 to 2023.7.22 (dependabot).

## [1.2.4] - 2023-05-23

### Changed

- Bumped the `requests` version.

## [1.2.3] - 2023-01-29

### Changed

- Default logger output only displays the delta; start and finish times
  moved to debug level.

## [1.2.2] - 2022-12-08

### Security

- Bumped `certifi` from 2021.10.8 to 2022.12.7 (dependabot).

## [1.2.1] - 2022-03-21

### Fixed

- Corrected the requirement entries.

## [1.2.0] - 2022-03-21

### Removed

- `fancy_logger` moved out to a stand-alone repo
  (github.com/poseidon0206/fancy_logger) and is now installed via pip
  requirements.

## [1.1.0] - 2022-01-10

### Added

- Fancy logger for `grab_pix_from_html.py`.

### Changed

- Adjusted the logger of `grab_pix_from_html.py`.

## [1.0.0] - 2022-01-10

### Added

- Initial release: `grab_pix_from_html.py` jpg scraper, README, and
  `requirements.txt`.
