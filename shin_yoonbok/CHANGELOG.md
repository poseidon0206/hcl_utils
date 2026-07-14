# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.19] - 2026-07-14

### Added

- Module, class and method docstrings across `ImageBuilder.py` and
  `build_image.py` (Sphinx `:param:`/`:return:` style).
- `CHANGELOG.md`.

### Changed

- README rewritten with Deployment, Config and Running-the-scripts
  sections.

## [1.0.18] - 2026-05-20

### Security

- Bumped `idna` from 3.7 to 3.15 (dependabot).

## [1.0.17] - 2026-04-08

### Security

- Bumped `requests` from 2.32.4 to 2.33.0 (dependabot).

## [1.0.16] - 2025-06-24

### Security

- Bumped `requests` (dependabot).

## [1.0.15] - 2025-06-17

### Security

- Dependency bump via GitHub dependabot.

## [1.0.14] - 2024-07-07

### Changed

- Bumped the `certifi` module version.

## [1.0.13] - 2024-06-18

### Changed

- Updated datetime calls to timezone-aware `datetime.now(tz=timezone.utc)`.
- Updated `urllib3` version.

## [1.0.12] - 2024-06-11

### Security

- Bumped `requests` to 2.32.3.

## [1.0.11] - 2024-04-12

### Changed

- Updated the other required packages.

## [1.0.10] - 2024-04-12

### Security

- Bumped `idna` from 3.4 to 3.7 (dependabot).

## [1.0.9] - 2023-10-17

### Security

- Bumped `urllib3` from 2.0.6 to 2.0.7 (dependabot).

## [1.0.8] - 2023-10-03

### Security

- Dependabot dependency updates.

## [1.0.7] - 2023-08-15

### Changed

- Requirement pins use `>=` instead of `==`.

## [1.0.6] - 2023-07-25

### Security

- Bumped `certifi` from 2022.12.7 to 2023.7.22 (dependabot).

## [1.0.5] - 2023-05-23

### Changed

- Bumped the `requests` version.

## [1.0.4] - 2022-12-08

### Security

- Bumped `certifi` from 2019.6.16 to 2022.12.7 (dependabot).

## [1.0.3] - 2021-06-02

### Security

- Bumped `urllib3` from 1.25.8 to 1.26.5 (dependabot).

## [1.0.2] - 2021-04-30

### Security

- Bumped `urllib3` from 1.25.3 to 1.25.8 (dependabot).

## [1.0.1] - 2019-08-12

### Fixed

- Corrected a typo in the README; updated the namesake section.

## [1.0.0] - 2019-08-12

### Added

- Initial release: `ImageBuilder` class and `build_image.py`, a docker
  image builder that tags and pushes to the registries configured in
  `config.py`.
