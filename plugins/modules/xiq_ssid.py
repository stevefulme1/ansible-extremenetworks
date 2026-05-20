#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: xiq_ssid
short_description: Manage SSIDs in ExtremeCloud IQ
version_added: "0.2.0"
description:
  - Create, update, or delete SSIDs in ExtremeCloud IQ.
  - Uses the XIQ REST API at C(/ssids).
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.extremenetworks.xiq
options:
  state:
    description:
      - Desired state of the SSID.
    type: str
    choices: [present, absent]
    default: present
  ssid_id:
    description:
      - Numeric ID of the SSID in XIQ.
      - Required when O(state=absent) or when updating an existing SSID.
    type: int
  name:
    description:
      - SSID broadcast name.
      - Required when creating a new SSID.
    type: str
  broadcast_name:
    description:
      - The name broadcast over the air. Defaults to O(name) if not set.
    type: str
  auth_type:
    description:
      - Authentication type for the SSID.
    type: str
    choices: [open, wpa2_personal, wpa2_enterprise, wpa3_personal, wpa3_enterprise]
  passphrase:
    description:
      - Pre-shared key for personal auth types.
    type: str
"""

EXAMPLES = r"""
- name: Create a WPA2 personal SSID
  stevefulme1.extremenetworks.xiq_ssid:
    xiq_token: "{{ xiq_token }}"
    name: "GuestWiFi"
    auth_type: wpa2_personal
    passphrase: "{{ guest_psk }}"
    state: present

- name: Delete an SSID
  stevefulme1.extremenetworks.xiq_ssid:
    xiq_token: "{{ xiq_token }}"
    ssid_id: 200
    state: absent
"""

RETURN = r"""
ssid:
  description: The SSID object returned by XIQ.
  returned: when state is present
  type: dict
  sample:
    id: 200
    name: "GuestWiFi"
    auth_type: "wpa2_personal"
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
        ssid_id=dict(type="int"),
        name=dict(type="str"),
        broadcast_name=dict(type="str"),
        auth_type=dict(
            type="str",
            choices=["open", "wpa2_personal", "wpa2_enterprise", "wpa3_personal", "wpa3_enterprise"],
        ),
        passphrase=dict(type="str", no_log=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[
            ("state", "absent", ["ssid_id"]),
        ],
        supports_check_mode=True,
    )

    client = XIQClient(
        token=module.params["xiq_token"],
        base_url=module.params["xiq_base_url"],
    )
    state = module.params["state"]
    ssid_id = module.params["ssid_id"]

    try:
        if state == "absent":
            try:
                client.get_ssid(ssid_id)
            except XIQClientError as exc:
                if exc.status_code == 404:
                    module.exit_json(changed=False, msg="SSID not found.")
                raise
            if module.check_mode:
                module.exit_json(changed=True, msg="SSID would be deleted.")
            client.delete_ssid(ssid_id)
            module.exit_json(changed=True, msg="SSID deleted.")

        # state == present
        if ssid_id:
            existing = client.get_ssid(ssid_id)
            payload = {}
            for key in ("name", "broadcast_name", "auth_type"):
                if module.params[key] and module.params[key] != existing.get(key):
                    payload[key] = module.params[key]
            if module.params["passphrase"]:
                payload["passphrase"] = module.params["passphrase"]
            if not payload:
                module.exit_json(changed=False, ssid=existing)
            if module.check_mode:
                module.exit_json(changed=True, msg="SSID would be updated.")
            result = client.update_ssid(ssid_id, payload)
            module.exit_json(changed=True, ssid=result)
        else:
            if not module.params["name"]:
                module.fail_json(msg="name is required to create a new SSID.")
            payload = {"name": module.params["name"]}
            if module.params["broadcast_name"]:
                payload["broadcast_name"] = module.params["broadcast_name"]
            if module.params["auth_type"]:
                payload["auth_type"] = module.params["auth_type"]
            if module.params["passphrase"]:
                payload["passphrase"] = module.params["passphrase"]
            if module.check_mode:
                module.exit_json(changed=True, msg="SSID would be created.")
            result = client.create_ssid(payload)
            module.exit_json(changed=True, ssid=result)

    except XIQClientError as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
