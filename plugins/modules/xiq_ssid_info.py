#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: xiq_ssid_info
short_description: Retrieve SSID information from ExtremeCloud IQ
version_added: "0.2.0"
description:
  - Query SSIDs in ExtremeCloud IQ.
  - Returns a single SSID when O(ssid_id) is given, otherwise lists all SSIDs.
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.extremenetworks.xiq
options:
  ssid_id:
    description:
      - Numeric ID of a specific SSID to retrieve.
    type: int
  page:
    description:
      - Page number for paginated results.
    type: int
    default: 1
  limit:
    description:
      - Maximum number of SSIDs per page.
    type: int
    default: 100
"""

EXAMPLES = r"""
- name: List all SSIDs
  stevefulme1.extremenetworks.xiq_ssid_info:
    xiq_token: "{{ xiq_token }}"
  register: ssids

- name: Get a specific SSID
  stevefulme1.extremenetworks.xiq_ssid_info:
    xiq_token: "{{ xiq_token }}"
    ssid_id: 200
  register: ssid
"""

RETURN = r"""
ssids:
  description: List of SSID objects.
  returned: when ssid_id is not specified
  type: list
  elements: dict
ssid:
  description: A single SSID object.
  returned: when ssid_id is specified
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
        ssid_id=dict(type="int"),
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
        if module.params["ssid_id"]:
            result = client.get_ssid(module.params["ssid_id"])
            module.exit_json(changed=False, ssid=result)
        else:
            result = client.list_ssids(
                page=module.params["page"],
                limit=module.params["limit"],
            )
            ssids = result.get("data", result) if isinstance(result, dict) else result
            module.exit_json(changed=False, ssids=ssids)
    except XIQClientError as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
