# stevefulme1.extremenetworks

Ansible Collection for Extreme Networks -- EXOS, VOSS/Fabric Engine, SLX-OS, ExtremeCloud IQ with ACLs, BGP, VXLAN, SPB fabric, and EDA telemetry.

## Overview

This collection provides **69 modules** for automating Extreme Networks switch infrastructure, along with 13 operational roles, a dynamic inventory plugin, and CI/CD workflows.

## Requirements

- ansible-core >= 2.16
- Python >= 3.11

## Installation

```bash
ansible-galaxy collection install stevefulme1.extremenetworks
```

Or from source:

```bash
ansible-galaxy collection build
ansible-galaxy collection install stevefulme1-extremenetworks-2.0.0.tar.gz
```

## Included Content

### Modules (69)

CRUD and info modules covering:

- **EXOS** — VLANs, ports, ACLs, STP, OSPF, BGP, MLAG, stacking
- **VOSS/Fabric Engine** — SPB fabric, IS-IS, VXLAN, IP shortcuts
- **SLX-OS** — interfaces, VRF, route maps, prefix lists
- **ExtremeCloud IQ** — device onboarding, policy management, monitoring
- **Cross-platform** — firmware, backup/restore, configuration management

### Roles (13)

| Role | Description |
|------|-------------|
| `extreme_acl_management` | Configure ACLs across platforms |
| `extreme_backup_restore` | Backup and restore switch configs |
| `extreme_bgp_setup` | Configure BGP peering |
| `extreme_fabric_setup` | Deploy SPB/VXLAN fabric |
| `extreme_firmware_upgrade` | Firmware lifecycle management |
| `extreme_monitoring` | Set up SNMP and syslog monitoring |
| `extreme_port_provisioning` | Provision switch ports |
| `extreme_security_hardening` | Security baseline configuration |
| `extreme_vlan_deploy` | VLAN provisioning and management |
| `extreme_xiq_onboard` | ExtremeCloud IQ device onboarding |
| `acl_management` | Legacy ACL role |
| `fabric_deploy` | Legacy fabric deployment |
| `switch_baseline` | Switch baseline configuration |

### Inventory Plugin

- `extremenetworks_inventory` -- Dynamic inventory from Extreme Networks devices

## Usage

```yaml
- name: Create a VLAN on EXOS switch
  stevefulme1.extremenetworks.exos_vlan:
    host: "{{ switch_host }}"
    username: "{{ switch_user }}"
    password: "{{ switch_pass }}"
    name: SERVERS
    vlan_id: 100
    state: present
```

## License

Apache-2.0
