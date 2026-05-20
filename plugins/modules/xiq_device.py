#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: xiq_device
short_description: Manage devices in ExtremeCloud IQ
version_added: "0.2.0"
description:
  - Onboard, update, or remove devices managed by ExtremeCloud IQ.
  - Uses the XIQ REST API at C(/devices).
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.extremenetworks.xiq
options:
  state:
    description:
      - Desired state of the device.
    type: str
    choices: [present, absent]
    default: present
  device_id:
    description:
      - Numeric ID of the device in XIQ.
      - Required when O(state=absent) or when updating an existing device.
    type: int
  serial_number:
    description:
      - Serial number of the device to onboard.
      - Required when O(state=present) and creating a new device.
    type: str
  hostname:
    description:
      - Hostname to assign to the device.
    type: str
  network_policy_id:
    description:
      - ID of the network policy to assign.
    type: int
"""

EXAMPLES = r"""
- name: Onboard a device by serial number
  stevefulme1.extremenetworks.xiq_device:
    xiq_token: "{{ xiq_token }}"
    serial_number: "SN123456"
    hostname: "switch-floor1"
    state: present

- name: Remove a device
  stevefulme1.extremenetworks.xiq_device:
    xiq_token: "{{ xiq_token }}"
    device_id: 12345
    state: absent
"""

RETURN = r"""
device:
  description: The device object returned by XIQ.
  returned: when state is present
  type: dict
  sample:
    id: 12345
    hostname: "switch-floor1"
    serial_number: "SN123456"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.stevefulme1.extremenetworks.plugins.module_utils.xiq_client import (
    XIQClient,
    XIQClientError,
)


def main():
    argument_spec = dict(
        xiq_token=dict(type="str", required=True, no_log=True),
        xiq_base_url=dict(type="str", default="https://api.extremecloudiq.com"),
        state=dict(type="str", default="present", choices=["present", "absent"]),
        device_id=dict(type="int"),
        serial_number=dict(type="str"),
        hostname=dict(type="str"),
        network_policy_id=dict(type="int"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[
            ("state", "absent", ["device_id"]),
        ],
        supports_check_mode=True,
    )

    client = XIQClient(
        token=module.params["xiq_token"],
        base_url=module.params["xiq_base_url"],
    )
    state = module.params["state"]
    device_id = module.params["device_id"]

    try:
        if state == "absent":
            # Check if device exists
            try:
                client.get_device(device_id)
            except XIQClientError as exc:
                if exc.status_code == 404:
                    module.exit_json(changed=False, msg="Device not found.")
                raise
            if module.check_mode:
                module.exit_json(changed=True, msg="Device would be deleted.")
            client.delete_device(device_id)
            module.exit_json(changed=True, msg="Device deleted.")

        # state == present
        if device_id:
            # Update existing device
            existing = client.get_device(device_id)
            payload = {}
            if module.params["hostname"] and module.params["hostname"] != existing.get("hostname"):
                payload["hostname"] = module.params["hostname"]
            if module.params["network_policy_id"] and module.params["network_policy_id"] != existing.get("network_policy_id"):
                payload["network_policy_id"] = module.params["network_policy_id"]
            if not payload:
                module.exit_json(changed=False, device=existing)
            if module.check_mode:
                module.exit_json(changed=True, msg="Device would be updated.")
            result = client.update_device(device_id, payload)
            module.exit_json(changed=True, device=result)
        else:
            # Create new device
            if not module.params["serial_number"]:
                module.fail_json(msg="serial_number is required to onboard a new device.")
            payload = {"serial_number": module.params["serial_number"]}
            if module.params["hostname"]:
                payload["hostname"] = module.params["hostname"]
            if module.params["network_policy_id"]:
                payload["network_policy_id"] = module.params["network_policy_id"]
            if module.check_mode:
                module.exit_json(changed=True, msg="Device would be onboarded.")
            result = client.create_device(payload)
            module.exit_json(changed=True, device=result)

    except XIQClientError as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
