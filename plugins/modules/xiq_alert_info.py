#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: xiq_alert_info
short_description: Retrieve alert policy information from ExtremeCloud IQ
version_added: "0.2.0"
description:
  - Query alert policies in ExtremeCloud IQ.
  - Returns a single policy when O(policy_id) is given, otherwise lists all policies.
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.extremenetworks.xiq
options:
  policy_id:
    description:
      - Numeric ID of a specific alert policy to retrieve.
    type: int
  page:
    description:
      - Page number for paginated results.
    type: int
    default: 1
  limit:
    description:
      - Maximum number of policies per page.
    type: int
    default: 100
"""

EXAMPLES = r"""
- name: List all alert policies
  stevefulme1.extremenetworks.xiq_alert_info:
    xiq_token: "{{ xiq_token }}"
  register: alerts

- name: Get a specific alert policy
  stevefulme1.extremenetworks.xiq_alert_info:
    xiq_token: "{{ xiq_token }}"
    policy_id: 500
  register: alert
"""

RETURN = r"""
policies:
  description: List of alert policy objects.
  returned: when policy_id is not specified
  type: list
  elements: dict
policy:
  description: A single alert policy object.
  returned: when policy_id is specified
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
        policy_id=dict(type="int"),
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
        if module.params["policy_id"]:
            result = client.get_alert_policy(module.params["policy_id"])
            module.exit_json(changed=False, policy=result)
        else:
            result = client.list_alert_policies(
                page=module.params["page"],
                limit=module.params["limit"],
            )
            policies = result.get("data", result) if isinstance(result, dict) else result
            module.exit_json(changed=False, policies=policies)
    except XIQClientError as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
