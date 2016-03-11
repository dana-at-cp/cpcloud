# -*- coding: utf-8 -*-

"""
cpcloud.checkpoint
~~~~~~~~~~~~~~~~~~

This module contains the primary objects for using
APIs enabled on Check Point security gateways and managers.

Tested on Gaia R77.30 and R80.
"""
from .exceptions import CheckPointClientError

import json
import requests

class IdentityAwarenessClient:
    CLIENT_ID = "cpcloud-IdentityAwarenessClient/0.0.1"
    BASE_API_PATH = "/_IA_MU_Agent/idasdk/"

    def __init__(self, gateway_ip, shared_secret, verify=True):
        self.gateway_ip = gateway_ip
        self.shared_secret = shared_secret
        self.verify = verify

    def build_url(self, endpoint):
        url = 'https://' + self.gateway_ip + IdentityAwarenessClient.BASE_API_PATH + endpoint
        return url

    def build_headers(self):
        headers = { 'content-type': 'application/json', 'user-agent': IdentityAwarenessClient.CLIENT_ID }
        return headers

    def show_identity(self, ip_address):
        url = self.build_url('show-identity')
        headers = self.build_headers()
        payload = { 'shared-secret': self.shared_secret,
                    'ip-address': ip_address }
        r = requests.post(url, headers=headers, data=json.dumps(payload), verify=self.verify)
        if r.status_code != 200:
            raise CheckPointClientError("Failed to show identity via IDA API", r.status_code)
        return r.json()

    def add_identity(self, ip_address, machine, domain, access_roles=[ "IA_API" ], session_timeout=43200):
        url = self.build_url('add-identity')
        headers = self.build_headers()
        payload = { 'shared-secret': self.shared_secret,
                    'ip-address': ip_address,
                    'machine': machine,
                    'identity-source': IdentityAwarenessClient.CLIENT_ID,
                    'domain': domain,
                    'calculate-roles': 0,
                    'fetch-machine-groups': 0,
                    'session-timeout': session_timeout,
                    'roles': access_roles }
        r = requests.post(url, headers=headers, data=json.dumps(payload), verify=self.verify)
        if r.status_code != 200:
            raise CheckPointClientError("Failed to add identity via IDA API", r.status_code)
        return r.json()
