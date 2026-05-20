#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: xiq_location_info
short_description: Retrieve location information from ExtremeCloud IQ
version_added: "0.2.0"
description:
  - Query locations in ExtremeCloud IQ.
  - Returns a single location when O(location_id) is given, otherwise returns the location tree.
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.extremenetworks.xiq
options:
  location_id:
    description:
      - Numeric ID of a specific location to retrieve.
    type: int
"""

EXAMPLES = r"""
- name: List all locations
  stevefulme1.extremenetworks.xiq_location_info:
    xiq_token: "{{ xiq_token }}"
  register: locations

- name: Get a specific location
  stevefulme1.extremenetworks.xiq_location_info:
    xiq_token: "{{ xiq_token }}"
    location_id: 300
  register: location
"""

RETURN = r"""
locations:
  description: Location tree structure.
  returned: when location_id is not specified
  type: list
  elements: dict
location:
  description: A single location object.
  returned: when location_id is specified
  type: dict
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
        location_id=dict(type="int"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    client = XIQClient(
        token=module.params["xiq_token"],
        base_url=module.params["xiq_base_url"],
    )

    try:
        if module.params["location_id"]:
            result = client.get_location(module.params["location_id"])
            module.exit_json(changed=False, location=result)
        else:
            result = client.list_locations()
            locations = result.get("data", result) if isinstance(result, dict) else result
            module.exit_json(changed=False, locations=locations)
    except XIQClientError as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
