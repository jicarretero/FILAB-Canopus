#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##
# Copyright 2018 FIWARE Foundation, e.V.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##


__author__ = "Jose Ignacio Carretero Guarde"


import requests
import json
from functions import *


class OpenstackQueries:
    instance = None

    def __init__(self, config):
        self.token = None

        self.config = config
        self.user = config.user
        self.password = config.password
        self.url = config.auth_url
        self.project = None
        self.token = None

        self.get_admin_token3()

    def get_admin_token3(self):
        headers = {'content-type': 'application/json'}
        data = {"auth": {
                    "identity": {
                        "methods": ["password"],
                        "password": {
                            "user": {
                                "name": "admin",
                                "domain": {"id": "default"},
                                "password": "zMCGfpTLTAMF2L2c"
                            }
                        }
                    }
               }}
        url = self.url + "/v3/auth/tokens"
        r = requests.post(url=url, headers=headers, data=json.dumps(data))

        if r.status_code == 201:
            self.token = r.headers['X-Subject-Token']
            r_dict = json.loads(r.text)
            self.project = r_dict['token']['project']['id']

        return r.status_code

    def change_password(self, user_id):
        url = self.url + "/v3/users/%s" % user_id
        headers = {'content-type': 'application/json', "X-Auth-Token": self.token}
        password = random_string(20)
        data = {"user": {
                    "password": password
               }}
        r = requests.patch(url=url, headers=headers, data=json.dumps(data))

        return password, r.status_code

    def get_user(self, name):
        url = self.url + "/v3/users"
        headers = {'content-type': 'application/json', "X-Auth-Token": self.token}

        r = requests.get(url=url, headers=headers)
        
        if r.status_code == 200:
            data = json.loads(r.text)
            return [d for d in data['users'] if d['name'] == name or d['id'] == name][0]['id'], 200

        return r.text, r.status_code

    @classmethod
    def get_openstack(cls, config=None):
        if cls.instance is None:
            cls.instance = OpenstackQueries(config)
        return cls.instance


if __name__ == "__main__":
    from Config import Config
    config = Config("config.ini")

    os = OpenstackQueries.get_openstack(config)
    print os.token

    print os.get_user('joseignacio.carretero@gmail.com')
