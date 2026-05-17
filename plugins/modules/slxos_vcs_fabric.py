#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""slxos_vcs_fabric module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: slxos_vcs_fabric
short_description: Manage SLX-OS VCS fabric
description:
    - Manage SLX-OS VCS fabric.
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
    fabric_id:
        description: Unique identifier of the vcs fabric.
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
- name: Create a vcs fabric
  stevefulme1.extremenetworks.slxos_vcs_fabric:
    host: api.example.com
    name: my-vcs-fabric
    state: present

- name: Delete a vcs fabric
  stevefulme1.extremenetworks.slxos_vcs_fabric:
    host: api.example.com
    fabric_id: "example-id"
    state: absent
"""

RETURN = r"""
vcs_fabric:
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
            fabric_id=dict(type="str"),
            name=dict(type="str"),
            host=dict(type="str", required=True),
            username=dict(type="str"),
            password=dict(type="str", no_log=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[("state", "absent", ("fabric_id",))],
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required Python libraries not found.")

    client = ApiClient(module)
    state = module.params["state"]
    resource_id = module.params.get("fabric_id")

    if state == "present":
        existing = None
        if resource_id:
            existing = client.get("vcs_fabric", resource_id)
        elif module.params.get("name"):
            candidates = client.list("vcs_fabric", {dict(name=module.params.get("name", ""))})
            if candidates:
                existing = candidates[0]

        if existing:
            if module.check_mode:
                module.exit_json(changed=False, vcs_fabric=existing)
            result = client.update("vcs_fabric", resource_id or existing.get("id", ""), module.params)
            module.exit_json(changed=True, vcs_fabric=result)
        else:
            if module.check_mode:
                module.exit_json(changed=True)
            result = client.create("vcs_fabric", module.params)
            module.exit_json(changed=True, vcs_fabric=result)
    else:
        existing = None
        if resource_id:
            existing = client.get("vcs_fabric", resource_id)
        if not existing:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True)
        client.delete("vcs_fabric", resource_id)
        module.exit_json(changed=True)


if __name__ == "__main__":
    main()
