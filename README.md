# stevefulme1.extremenetworks

Ansible Collection for Extreme Networks -- EXOS, VOSS/Fabric Engine, SLX-OS, ExtremeCloud IQ.

**Status: Pre-release. Under active development.**

## Overview

This collection provides operational roles for automating Extreme Networks
switch infrastructure.  The roles wrap the upstream `extreme.exos` collection
modules (`exos_config`, `exos_vlans`, etc.) and add opinionated workflows for
common day-2 tasks.

## Requirements

- ansible-core >= 2.16
- Python >= 3.11
- `extreme.exos` collection (for roles that reference `extreme.exos.exos_config`)

## Installation

```bash
ansible-galaxy collection install stevefulme1.extremenetworks
```

## Included Content

### Modules (ExtremeCloud IQ)

| Module | Description |
|--------|-------------|
| `xiq_device` | Onboard, update, or remove devices |
| `xiq_device_info` | List or retrieve device details |
| `xiq_network_policy` | Create, update, or delete network policies |
| `xiq_network_policy_info` | List or retrieve network policy details |
| `xiq_ssid` | Create, update, or delete SSIDs |
| `xiq_ssid_info` | List or retrieve SSID details |
| `xiq_location` | Create, update, or delete locations/sites |
| `xiq_location_info` | List or retrieve location details |
| `xiq_user` | Create, update, or delete XIQ users |
| `xiq_user_info` | List or retrieve user details |
| `xiq_alert` | Create, update, or delete alert policies |
| `xiq_alert_info` | List or retrieve alert policy details |

All modules authenticate via Bearer token (`xiq_token`) against the ExtremeCloud IQ
REST API at `https://api.extremecloudiq.com`.

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
