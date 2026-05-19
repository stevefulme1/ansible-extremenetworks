# Changelog

## [2.0.1] - 2026-05-18

### Security
- Prevent credential leak in API request bodies: connection params (password,
  api_key, username, host, validate_certs) are now stripped before POST/PUT
- Added request timeout (30 s) to all HTTP methods to prevent hung connections
- Hardened .gitignore against accidental credential commits

## [2.0.0] - 2026-05-17

### Added
- Idempotency: get-before-write with state comparison in 33 modules
- Pagination support (limit/offset) for all _info modules
- 3 operational roles for Extreme Networks switches
- Comprehensive unit and integration test suites (35 unit tests, 5 integration targets)
- Pre-commit and linting configuration
- Sanity tests for ansible-core 2.16/2.17/2.18/2.20

### Fixed
- Pylint unhashable-member false positives resolved
- Stale sanity ignore files removed
- Role README files added for Galaxy compliance
- Galaxy import validation issues resolved
- CI failures resolved

### Security
- Bumped requests>=2.32.5 to fix CVE-2023-32681, CVE-2024-35195

## [1.2.0] - 2026-05-15

### Added
- 68 modules covering full Extreme Networks platform (EXOS, VOSS, SLX-OS, ExtremeCloud IQ)
- 10 Day-2 operation roles
- 4 EDA source plugins
- Dynamic inventory plugin

## [1.0.0] - 2026-05-15

### Added
- Initial release with EXOS, VOSS, and SLX-OS modules
- EDA source plugins for event-driven automation
- Unit tests and CI pipeline
