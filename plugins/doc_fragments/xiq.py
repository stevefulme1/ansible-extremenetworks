# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    """Doc fragment for ExtremeCloud IQ authentication parameters."""

    DOCUMENTATION = r"""
options:
  xiq_token:
    description:
      - ExtremeCloud IQ API bearer token.
      - Can also be set via the E(XIQ_TOKEN) environment variable.
    type: str
    required: true
  xiq_base_url:
    description:
      - ExtremeCloud IQ API base URL.
      - Can also be set via the E(XIQ_BASE_URL) environment variable.
    type: str
    default: https://api.extremecloudiq.com
"""
