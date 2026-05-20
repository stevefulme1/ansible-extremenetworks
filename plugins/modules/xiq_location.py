#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: xiq_location
short_description: Manage locations in ExtremeCloud IQ
version_added: "0.2.0"
description:
  - Create, update, or delete locations (sites) in ExtremeCloud IQ.
  - Uses the XIQ REST API at C(/locations).
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.extremenetworks.xiq
options:
  state:
    description:
      - Desired state of the location.
    type: str
    choices: [present, absent]
    default: present
  location_id:
    description:
      - Numeric ID of the location in XIQ.
      - Required when O(state=absent) or when updating an existing location.
    type: int
  name:
    description:
      - Name of the location.
      - Required when creating a new location.
    type: str
  parent_id:
    description:
      - ID of the parent location in the hierarchy.
    type: int
  location_type:
    description:
      - Type of location in the XIQ hierarchy.
    type: str
    choices: [BUILDING, FLOOR, SITE]
  address:
    description:
      - Physical address of the location.
    type: str
"""

EXAMPLES = r"""
- name: Create a building location
  stevefulme1.extremenetworks.xiq_location:
    xiq_token: "{{ xiq_token }}"
    name: "HQ Building A"
    location_type: BUILDING
    address: "123 Main St, Anytown, USA"
    state: present

- name: Delete a location
  stevefulme1.extremenetworks.xiq_location:
    xiq_token: "{{ xiq_token }}"
    location_id: 300
    state: absent
"""

RETURN = r"""
location:
  description: The location object returned by XIQ.
  returned: when state is present
  type: dict
  sample:
    id: 300
    name: "HQ Building A"
    location_type: "BUILDING"
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
        location_id=dict(type="int"),
        name=dict(type="str"),
        parent_id=dict(type="int"),
        location_type=dict(type="str", choices=["BUILDING", "FLOOR", "SITE"]),
        address=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[
            ("state", "absent", ["location_id"]),
        ],
        supports_check_mode=True,
    )

    client = XIQClient(
        token=module.params["xiq_token"],
        base_url=module.params["xiq_base_url"],
    )
    state = module.params["state"]
    location_id = module.params["location_id"]

    try:
        if state == "absent":
            try:
                client.get_location(location_id)
            except XIQClientError as exc:
                if exc.status_code == 404:
                    module.exit_json(changed=False, msg="Location not found.")
                raise
            if module.check_mode:
                module.exit_json(changed=True, msg="Location would be deleted.")
            client.delete_location(location_id)
            module.exit_json(changed=True, msg="Location deleted.")

        # state == present
        if location_id:
            existing = client.get_location(location_id)
            payload = {}
            for key in ("name", "address", "location_type"):
                if module.params[key] and module.params[key] != existing.get(key):
                    payload[key] = module.params[key]
            if module.params["parent_id"] and module.params["parent_id"] != existing.get("parent_id"):
                payload["parent_id"] = module.params["parent_id"]
            if not payload:
                module.exit_json(changed=False, location=existing)
            if module.check_mode:
                module.exit_json(changed=True, msg="Location would be updated.")
            result = client.update_location(location_id, payload)
            module.exit_json(changed=True, location=result)
        else:
            if not module.params["name"]:
                module.fail_json(msg="name is required to create a new location.")
            payload = {"name": module.params["name"]}
            if module.params["parent_id"]:
                payload["parent_id"] = module.params["parent_id"]
            if module.params["location_type"]:
                payload["location_type"] = module.params["location_type"]
            if module.params["address"]:
                payload["address"] = module.params["address"]
            if module.check_mode:
                module.exit_json(changed=True, msg="Location would be created.")
            result = client.create_location(payload)
            module.exit_json(changed=True, location=result)

    except XIQClientError as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
