#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: xiq_user
short_description: Manage users in ExtremeCloud IQ
version_added: "0.2.0"
description:
  - Create, update, or delete users in the ExtremeCloud IQ account.
  - Uses the XIQ REST API at C(/account/viq).
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.extremenetworks.xiq
options:
  state:
    description:
      - Desired state of the user.
    type: str
    choices: [present, absent]
    default: present
  user_id:
    description:
      - Numeric ID of the user in XIQ.
      - Required when O(state=absent) or when updating an existing user.
    type: int
  login_name:
    description:
      - Login name (email) of the user.
      - Required when creating a new user.
    type: str
  password:
    description:
      - Password for the new user.
      - Required when creating a new user.
    type: str
  first_name:
    description:
      - First name of the user.
    type: str
  last_name:
    description:
      - Last name of the user.
    type: str
  user_role:
    description:
      - Role to assign to the user.
    type: str
    choices: [ADMIN, MONITOR, OPERATOR, HELPDESK, GUEST_MANAGEMENT]
"""

EXAMPLES = r"""
- name: Create an admin user
  stevefulme1.extremenetworks.xiq_user:
    xiq_token: "{{ xiq_token }}"
    login_name: "admin@example.com"
    password: "{{ user_password }}"
    first_name: "Jane"
    last_name: "Doe"
    user_role: ADMIN
    state: present

- name: Delete a user
  stevefulme1.extremenetworks.xiq_user:
    xiq_token: "{{ xiq_token }}"
    user_id: 400
    state: absent
"""

RETURN = r"""
user:
  description: The user object returned by XIQ.
  returned: when state is present
  type: dict
  sample:
    id: 400
    login_name: "admin@example.com"
    user_role: "ADMIN"
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
        user_id=dict(type="int"),
        login_name=dict(type="str"),
        password=dict(type="str", no_log=True),
        first_name=dict(type="str"),
        last_name=dict(type="str"),
        user_role=dict(
            type="str",
            choices=["ADMIN", "MONITOR", "OPERATOR", "HELPDESK", "GUEST_MANAGEMENT"],
        ),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[
            ("state", "absent", ["user_id"]),
        ],
        supports_check_mode=True,
    )

    client = XIQClient(
        token=module.params["xiq_token"],
        base_url=module.params["xiq_base_url"],
    )
    state = module.params["state"]
    user_id = module.params["user_id"]

    try:
        if state == "absent":
            try:
                client.get_user(user_id)
            except XIQClientError as exc:
                if exc.status_code == 404:
                    module.exit_json(changed=False, msg="User not found.")
                raise
            if module.check_mode:
                module.exit_json(changed=True, msg="User would be deleted.")
            client.delete_user(user_id)
            module.exit_json(changed=True, msg="User deleted.")

        # state == present
        if user_id:
            existing = client.get_user(user_id)
            payload = {}
            for key in ("first_name", "last_name", "user_role"):
                if module.params[key] and module.params[key] != existing.get(key):
                    payload[key] = module.params[key]
            if module.params["password"]:
                payload["password"] = module.params["password"]
            if not payload:
                module.exit_json(changed=False, user=existing)
            if module.check_mode:
                module.exit_json(changed=True, msg="User would be updated.")
            result = client.update_user(user_id, payload)
            module.exit_json(changed=True, user=result)
        else:
            if not module.params["login_name"]:
                module.fail_json(msg="login_name is required to create a new user.")
            if not module.params["password"]:
                module.fail_json(msg="password is required to create a new user.")
            payload = {
                "login_name": module.params["login_name"],
                "password": module.params["password"],
            }
            for key in ("first_name", "last_name", "user_role"):
                if module.params[key]:
                    payload[key] = module.params[key]
            if module.check_mode:
                module.exit_json(changed=True, msg="User would be created.")
            result = client.create_user(payload)
            module.exit_json(changed=True, user=result)

    except XIQClientError as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
