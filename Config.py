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


from ConfigParser import ConfigParser

class Config:
    def __init__(self, config_file):
        parser = ConfigParser()
        parser.read(config_file)

        d = {
            "auth_url": parser.get("keystone", "url"),
            "user": parser.get("keystone", "user"),
            "password": parser.get("keystone", "password"),

            "email_host": parser.get("email", "host"),
            "email_from": parser.get("email", "from"),
            "from_name": parser.get("email", "from_name"),
            "recover_html_template": parser.get("email", "recover_html_template"),
            "recover_text_template": parser.get("email", "recover_text_template"),
            "recover_subject": parser.get("email", "recover_subject"),
            "new_password_html_template": parser.get("email", "new_password_html_template"),
            "new_password_text_template": parser.get("email", "new_password_text_template"),
            "new_password_subject": parser.get("email", "new_password_subject"),
            "base_url": parser.get("server", "base_url"),
            "use_memcached": bool(parser.get("memcached", "use_memcached")),
            "memcached_host": parser.get("memcached", "memcached_host"),
            "memcached_port": int(parser.get("memcached", "memcached_port"))
        }

        self.__dict__.update(d)
