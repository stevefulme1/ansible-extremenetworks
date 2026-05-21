# Changelog

## [0.2.0] - 2026-05-20

### Added
- 12 ExtremeCloud IQ (XIQ) modules for cloud-managed device automation:
  - `xiq_device` / `xiq_device_info` -- manage and list devices
  - `xiq_network_policy` / `xiq_network_policy_info` -- manage network policies
  - `xiq_ssid` / `xiq_ssid_info` -- manage SSIDs
  - `xiq_location` / `xiq_location_info` -- manage locations/sites
  - `xiq_user` / `xiq_user_info` -- manage XIQ users
  - `xiq_alert` / `xiq_alert_info` -- manage alert policies
- `plugins/module_utils/xiq_client.py` -- shared REST API client for XIQ
- `plugins/doc_fragments/xiq.py` -- shared auth params (xiq_token, xiq_base_url)
- All modules support check mode and idempotent CRUD operations
- Auth via Bearer token against `https://api.extremecloudiq.com`

## [3.0.0] - 2026-05-20

### Removed
- **All 68 custom modules deleted** -- every module used fabricated REST API
  endpoints (`/api/v1/<resource>`) that do not exist in any Extreme Networks
  product (EXOS JSONRPC/RESTCONF, VOSS CLI, SLX-OS CLI, or ExtremeCloud IQ
  REST API).  Real EXOS automation should use the official `extreme.exos`
  collection or the EXOS JSONRPC / RESTCONF interfaces.
- Dynamic inventory plugin (`extremenetworks_inventory`) removed -- used same
  fabricated `/api/v1/hosts` endpoint.
- Fabricated `api_client.py` module utility removed.

### Retained
- 12 operational roles that wrap the upstream `extreme.exos` collection.
- EDA source plugins (if present).
- CI/CD workflows and test infrastructure.

## [2.1.2] - 2026-05-18

### Security
- Added `no_log: true` to all `password` and `api_key` role arguments to prevent credential exposure in logs
- Changed EDA webhook default listen address from `0.0.0.0` to `127.0.0.1` to prevent unintended network exposure
- Added payload size limit (1 MB) to EDA webhook event source

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
