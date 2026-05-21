#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: xiq_device_info
short_description: Retrieve device information from ExtremeCloud IQ
version_added: "0.2.0"
description:
  - Query devices managed by ExtremeCloud IQ.
  - Returns a single device when O(device_id) is given, otherwise lists all devices.
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.extremenetworks.xiq
options:
  device_id:
    description:
      - Numeric ID of a specific device to retrieve.
    type: int
  page:
    description:
      - Page number for paginated results.
    type: int
    default: 1
  limit:
    description:
      - Maximum number of devices per page.
    type: int
    default: 100
"""

EXAMPLES = r"""
- name: List all devices
  stevefulme1.extremenetworks.xiq_device_info:
    xiq_token: "{{ xiq_token }}"
  register: devices

- name: Get a specific device
  stevefulme1.extremenetworks.xiq_device_info:
    xiq_token: "{{ xiq_token }}"
    device_id: 12345
  register: device
"""

RETURN = r"""
devices:
  description: List of device objects.
  returned: when device_id is not specified
  type: list
  elements: dict
device:
  description: A single device object.
  returned: when device_id is specified
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
        device_id=dict(type="int"),
        page=dict(type="int", default=1),
        limit=dict(type="int", default=100),
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
        if module.params["device_id"]:
            result = client.get_device(module.params["device_id"])
            module.exit_json(changed=False, device=result)
        else:
            result = client.list_devices(
                page=module.params["page"],
                limit=module.params["limit"],
            )
            devices = result.get("data", result) if isinstance(result, dict) else result
            module.exit_json(changed=False, devices=devices)
    except XIQClientError as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
