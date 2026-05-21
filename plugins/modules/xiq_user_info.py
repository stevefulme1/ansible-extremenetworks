#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: xiq_user_info
short_description: Retrieve user information from ExtremeCloud IQ
version_added: "0.2.0"
description:
  - Query users in the ExtremeCloud IQ account.
  - Returns a single user when O(user_id) is given, otherwise lists all users.
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.extremenetworks.xiq
options:
  user_id:
    description:
      - Numeric ID of a specific user to retrieve.
    type: int
  page:
    description:
      - Page number for paginated results.
    type: int
    default: 1
  limit:
    description:
      - Maximum number of users per page.
    type: int
    default: 100
"""

EXAMPLES = r"""
- name: List all users
  stevefulme1.extremenetworks.xiq_user_info:
    xiq_token: "{{ xiq_token }}"
  register: users

- name: Get a specific user
  stevefulme1.extremenetworks.xiq_user_info:
    xiq_token: "{{ xiq_token }}"
    user_id: 400
  register: user
"""

RETURN = r"""
users:
  description: List of user objects.
  returned: when user_id is not specified
  type: list
  elements: dict
user:
  description: A single user object.
  returned: when user_id is specified
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
        user_id=dict(type="int"),
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
        if module.params["user_id"]:
            result = client.get_user(module.params["user_id"])
            module.exit_json(changed=False, user=result)
        else:
            result = client.list_users(
                page=module.params["page"],
                limit=module.params["limit"],
            )
            users = result.get("data", result) if isinstance(result, dict) else result
            module.exit_json(changed=False, users=users)
    except XIQClientError as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
