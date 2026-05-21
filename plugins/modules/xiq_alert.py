#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: xiq_alert
short_description: Manage alert policies in ExtremeCloud IQ
version_added: "0.2.0"
description:
  - Create, update, or delete alert policies in ExtremeCloud IQ.
  - Uses the XIQ REST API at C(/alert-policies).
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.extremenetworks.xiq
options:
  state:
    description:
      - Desired state of the alert policy.
    type: str
    choices: [present, absent]
    default: present
  policy_id:
    description:
      - Numeric ID of the alert policy in XIQ.
      - Required when O(state=absent) or when updating an existing policy.
    type: int
  name:
    description:
      - Name of the alert policy.
      - Required when creating a new policy.
    type: str
  description:
    description:
      - Description of the alert policy.
    type: str
  severity:
    description:
      - Severity level of the alert policy.
    type: str
    choices: [CRITICAL, MAJOR, MINOR, INFORMATIONAL]
  enabled:
    description:
      - Whether the alert policy is enabled.
    type: bool
"""

EXAMPLES = r"""
- name: Create an alert policy
  stevefulme1.extremenetworks.xiq_alert:
    xiq_token: "{{ xiq_token }}"
    name: "AP Down Alert"
    description: "Alert when an AP goes offline"
    severity: CRITICAL
    enabled: true
    state: present

- name: Delete an alert policy
  stevefulme1.extremenetworks.xiq_alert:
    xiq_token: "{{ xiq_token }}"
    policy_id: 500
    state: absent
"""

RETURN = r"""
policy:
  description: The alert policy object returned by XIQ.
  returned: when state is present
  type: dict
  sample:
    id: 500
    name: "AP Down Alert"
    severity: "CRITICAL"
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
        policy_id=dict(type="int"),
        name=dict(type="str"),
        description=dict(type="str"),
        severity=dict(
            type="str",
            choices=["CRITICAL", "MAJOR", "MINOR", "INFORMATIONAL"],
        ),
        enabled=dict(type="bool"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[
            ("state", "absent", ["policy_id"]),
        ],
        supports_check_mode=True,
    )

    client = XIQClient(
        token=module.params["xiq_token"],
        base_url=module.params["xiq_base_url"],
    )
    state = module.params["state"]
    policy_id = module.params["policy_id"]

    try:
        if state == "absent":
            try:
                client.get_alert_policy(policy_id)
            except XIQClientError as exc:
                if exc.status_code == 404:
                    module.exit_json(changed=False, msg="Alert policy not found.")
                raise
            if module.check_mode:
                module.exit_json(changed=True, msg="Alert policy would be deleted.")
            client.delete_alert_policy(policy_id)
            module.exit_json(changed=True, msg="Alert policy deleted.")

        # state == present
        if policy_id:
            existing = client.get_alert_policy(policy_id)
            payload = {}
            for key in ("name", "description", "severity"):
                if module.params[key] and module.params[key] != existing.get(key):
                    payload[key] = module.params[key]
            if module.params["enabled"] is not None and module.params["enabled"] != existing.get("enabled"):
                payload["enabled"] = module.params["enabled"]
            if not payload:
                module.exit_json(changed=False, policy=existing)
            if module.check_mode:
                module.exit_json(changed=True, msg="Alert policy would be updated.")
            result = client.update_alert_policy(policy_id, payload)
            module.exit_json(changed=True, policy=result)
        else:
            if not module.params["name"]:
                module.fail_json(msg="name is required to create a new alert policy.")
            payload = {"name": module.params["name"]}
            for key in ("description", "severity"):
                if module.params[key]:
                    payload[key] = module.params[key]
            if module.params["enabled"] is not None:
                payload["enabled"] = module.params["enabled"]
            if module.check_mode:
                module.exit_json(changed=True, msg="Alert policy would be created.")
            result = client.create_alert_policy(payload)
            module.exit_json(changed=True, policy=result)

    except XIQClientError as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
