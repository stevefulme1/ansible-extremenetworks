# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

"""ExtremeCloud IQ REST API client for Ansible modules."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.module_utils.urls import open_url


class XIQClientError(Exception):
    """Exception raised by XIQClient on API errors."""

    def __init__(self, message, status_code=None, response_body=None):
        super(XIQClientError, self).__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class XIQClient(object):
    """Client for the ExtremeCloud IQ REST API.

    Uses ansible.module_utils.urls.open_url so no external dependencies
    (like ``requests``) are needed at runtime.
    """

    def __init__(self, token, base_url="https://api.extremecloudiq.com"):
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": "Bearer %s" % token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    # ------------------------------------------------------------------
    # Low-level helpers
    # ------------------------------------------------------------------

    def _request(self, method, path, data=None, params=None):
        """Send an HTTP request and return the parsed JSON response."""
        url = "%s%s" % (self.base_url, path)

        if params:
            query = "&".join(
                "%s=%s" % (k, v) for k, v in sorted(params.items()) if v is not None
            )
            if query:
                url = "%s?%s" % (url, query)

        body = json.dumps(data).encode("utf-8") if data is not None else None

        try:
            resp = open_url(
                url,
                method=method,
                headers=self.headers,
                data=body,
                validate_certs=True,
            )
            raw = resp.read()
            if raw:
                return json.loads(raw)
            return None
        except Exception as exc:
            status = getattr(exc, "code", None)
            resp_body = None
            if hasattr(exc, "read"):
                try:
                    resp_body = exc.read().decode("utf-8")
                except Exception:
                    pass
            raise XIQClientError(
                "XIQ API %s %s failed: %s" % (method, path, str(exc)),
                status_code=status,
                response_body=resp_body,
            )

    def get(self, path, params=None):
        """HTTP GET."""
        return self._request("GET", path, params=params)

    def post(self, path, data=None):
        """HTTP POST."""
        return self._request("POST", path, data=data)

    def put(self, path, data=None):
        """HTTP PUT."""
        return self._request("PUT", path, data=data)

    def delete(self, path):
        """HTTP DELETE."""
        return self._request("DELETE", path)

    # ------------------------------------------------------------------
    # Devices
    # ------------------------------------------------------------------

    def list_devices(self, page=1, limit=100):
        """List managed devices."""
        return self.get("/devices", params={"page": page, "limit": limit})

    def get_device(self, device_id):
        """Get a single device by ID."""
        return self.get("/devices/%s" % device_id)

    def create_device(self, payload):
        """Onboard a device."""
        return self.post("/devices", data=payload)

    def update_device(self, device_id, payload):
        """Update a device."""
        return self.put("/devices/%s" % device_id, data=payload)

    def delete_device(self, device_id):
        """Delete (remove) a device."""
        return self.delete("/devices/%s" % device_id)

    # ------------------------------------------------------------------
    # Network Policies
    # ------------------------------------------------------------------

    def list_network_policies(self, page=1, limit=100):
        """List network policies."""
        return self.get(
            "/network-policies", params={"page": page, "limit": limit}
        )

    def get_network_policy(self, policy_id):
        """Get a single network policy."""
        return self.get("/network-policies/%s" % policy_id)

    def create_network_policy(self, payload):
        """Create a network policy."""
        return self.post("/network-policies", data=payload)

    def update_network_policy(self, policy_id, payload):
        """Update a network policy."""
        return self.put("/network-policies/%s" % policy_id, data=payload)

    def delete_network_policy(self, policy_id):
        """Delete a network policy."""
        return self.delete("/network-policies/%s" % policy_id)

    # ------------------------------------------------------------------
    # SSIDs
    # ------------------------------------------------------------------

    def list_ssids(self, page=1, limit=100):
        """List SSIDs."""
        return self.get("/ssids", params={"page": page, "limit": limit})

    def get_ssid(self, ssid_id):
        """Get a single SSID."""
        return self.get("/ssids/%s" % ssid_id)

    def create_ssid(self, payload):
        """Create an SSID."""
        return self.post("/ssids", data=payload)

    def update_ssid(self, ssid_id, payload):
        """Update an SSID."""
        return self.put("/ssids/%s" % ssid_id, data=payload)

    def delete_ssid(self, ssid_id):
        """Delete an SSID."""
        return self.delete("/ssids/%s" % ssid_id)

    # ------------------------------------------------------------------
    # Locations
    # ------------------------------------------------------------------

    def list_locations(self):
        """List locations (tree structure)."""
        return self.get("/locations/tree")

    def get_location(self, location_id):
        """Get a single location."""
        return self.get("/locations/%s" % location_id)

    def create_location(self, payload):
        """Create a location."""
        return self.post("/locations", data=payload)

    def update_location(self, location_id, payload):
        """Update a location."""
        return self.put("/locations/%s" % location_id, data=payload)

    def delete_location(self, location_id):
        """Delete a location."""
        return self.delete("/locations/%s" % location_id)

    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------

    def list_users(self, page=1, limit=100):
        """List XIQ users."""
        return self.get("/account/viq", params={"page": page, "limit": limit})

    def get_user(self, user_id):
        """Get a single user."""
        return self.get("/account/viq/%s" % user_id)

    def create_user(self, payload):
        """Create a user."""
        return self.post("/account/viq", data=payload)

    def update_user(self, user_id, payload):
        """Update a user."""
        return self.put("/account/viq/%s" % user_id, data=payload)

    def delete_user(self, user_id):
        """Delete a user."""
        return self.delete("/account/viq/%s" % user_id)

    # ------------------------------------------------------------------
    # Alerts
    # ------------------------------------------------------------------

    def list_alert_policies(self, page=1, limit=100):
        """List alert policies."""
        return self.get(
            "/alert-policies", params={"page": page, "limit": limit}
        )

    def get_alert_policy(self, policy_id):
        """Get a single alert policy."""
        return self.get("/alert-policies/%s" % policy_id)

    def create_alert_policy(self, payload):
        """Create an alert policy."""
        return self.post("/alert-policies", data=payload)

    def update_alert_policy(self, policy_id, payload):
        """Update an alert policy."""
        return self.put("/alert-policies/%s" % policy_id, data=payload)

    def delete_alert_policy(self, policy_id):
        """Delete an alert policy."""
        return self.delete("/alert-policies/%s" % policy_id)
