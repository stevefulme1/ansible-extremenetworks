# stevefulme1.extremenetworks

Ansible Collection for Extreme Networks -- EXOS, VOSS/Fabric Engine, SLX-OS, ExtremeCloud IQ.

**Status: Pre-release. Under active development.**

## Overview

This collection provides operational roles for automating Extreme Networks
switch infrastructure.  The roles wrap the upstream `extreme.exos` collection
modules (`exos_config`, `exos_vlans`, etc.) and add opinionated workflows for
common day-2 tasks.

> **Note:** All custom modules and the dynamic inventory plugin were removed
> during an audit because they used fabricated REST API endpoints that do not
> match any real Extreme Networks API (JSONRPC, RESTCONF, or CLI).  Real EXOS
> automation should use the official `extreme.exos` collection or the EXOS
> JSONRPC / RESTCONF interfaces.

## Requirements

- ansible-core >= 2.16
- Python >= 3.11
- `extreme.exos` collection (for roles that reference `extreme.exos.exos_config`)

## Installation

```bash
ansible-galaxy collection install stevefulme1.extremenetworks
```

## Included Content

### Roles

| Role | Description |
|------|-------------|
| `acl_management` | Configure ACLs via `exos_config` |
| `extreme_acl_management` | Configure ACLs across platforms |
| `extreme_backup_restore` | Backup and restore switch configs |
| `extreme_bgp_setup` | Configure BGP peering |
| `extreme_fabric_setup` | Deploy SPB/VXLAN fabric |
| `extreme_firmware_upgrade` | Firmware lifecycle management |
| `extreme_monitoring` | Set up SNMP and syslog monitoring |
| `extreme_port_provisioning` | Provision switch ports |
| `extreme_security_hardening` | Security baseline configuration |
| `extreme_vlan_deploy` | VLAN provisioning and management |
| `fabric_deploy` | Fabric deployment via `exos_config` |
| `switch_baseline` | Switch baseline configuration |

## License

GPL-3.0-or-later
