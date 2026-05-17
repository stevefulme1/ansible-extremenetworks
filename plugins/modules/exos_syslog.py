#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""exos_syslog module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: exos_syslog
short_description: Manage ExtremeXOS syslog targets
description:
    - Manage ExtremeXOS syslog targets.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    state:
        description: Desired state of the resource.
        type: str
        default: present
        choices: [present, absent]
    host:
        description: API host address.
        type: str
        required: true
    syslog_target:
        description: Unique identifier of the syslog.
        type: str
    name:
        description: Display name.
        type: str
    username:
        description: Authentication username.
        type: str
    password:
        description: Authentication password.
        type: str
    api_key:
        description: API key for authentication.
        type: str
    validate_certs:
        description: Validate SSL certificates.
        type: bool
        default: true
"""

EXAMPLES = r"""
- name: Create a syslog
  stevefulme1.extremenetworks.exos_syslog:
    host: api.example.com
    name: my-syslog
    state: present

- name: Delete a syslog
  stevefulme1.extremenetworks.exos_syslog:
    host: api.example.com
    syslog_target: "example-id"
    state: absent
"""

RETURN = r"""
syslog:
    description: Resource details.
    returned: on success
    type: dict
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.stevefulme1.extremenetworks.plugins.module_utils.api_client import ApiClient
    HAS_CLIENT = True
except ImportError:
    HAS_CLIENT = False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", default="present", choices=["present", "absent"]),
            syslog_target=dict(type="str"),
            name=dict(type="str"),
            host=dict(type="str", required=True),
            username=dict(type="str"),
            password=dict(type="str", no_log=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[("state", "absent", ("syslog_target",))],
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required Python libraries not found.")

    client = ApiClient(module)
    state = module.params["state"]
    resource_id = module.params.get("syslog_target")

    if state == "present":
        existing = None
        if resource_id:
            existing = client.get("syslog", resource_id)
        elif module.params.get("name"):
            name_filter = module.params.get("name", "")
            candidates = client.list("syslog", {"name": name_filter})
            if candidates:
                existing = candidates[0]

        if existing:
            if module.check_mode:
                module.exit_json(changed=False, syslog=existing)
            result = client.update("syslog", resource_id or existing.get("id", ""), module.params)
            module.exit_json(changed=True, syslog=result)
        else:
            if module.check_mode:
                module.exit_json(changed=True)
            result = client.create("syslog", module.params)
            module.exit_json(changed=True, syslog=result)
    else:
        existing = None
        if resource_id:
            existing = client.get("syslog", resource_id)
        if not existing:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True)
        client.delete("syslog", resource_id)
        module.exit_json(changed=True)


if __name__ == "__main__":
    main()
