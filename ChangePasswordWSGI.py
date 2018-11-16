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


from flask import Flask
from flask_restful import Resource, Api, reqparse
from OpenstackOps import OpenstackQueries
from functions import *
from Mailer import  Mailer
from Store import Store
import json


class AskForPasswordChange(Resource):
    def post(self, mail):
        global users
        klog("Asked for Password " + mail)
        code = random_string(128)
        

        os = OpenstackQueries.get_openstack()
        user_id, http_result = os.get_user(mail)

        if http_result == 200:
            Store.get_store().set(code, json.dumps({"email": mail, "id": user_id}))
            klog(code)
            klog(json.dumps({"email": mail, "id": user_id}))
            base_url = global_config().base_url
            confirm_url = base_url + "/confirm/" + code
            Mailer.get_mailer().send_recover_link(mail, confirm_url)
            return "A confirmation message has been sent to your email"
        else:
            return user_id, http_result


class ConfirmPasswordChange(Resource):
    def get(self, code):
        global users
        klog("Confirm change for code " + code)

        data_js = Store.get_store().get(code)

        if data_js is not None:
            data = json.loads(data_js) 
            mail = data['email']
            uid = data['id']

            os = OpenstackQueries.get_openstack()
            password, http_result = os.change_password(uid)

            Mailer.get_mailer().send_new_password(mail, password)

            Store.get_store().delete(code)
            return "Password changed. Please, check your email", http_result
        else:
            return "Not found Code", 404


class Dump(Resource):
    def get(self):
        klog("Dump called") 
        return {}


app = Flask(__name__)
api = Api(app)

api.add_resource(AskForPasswordChange, '/reset/<string:mail>')
api.add_resource(ConfirmPasswordChange, '/confirm/<string:code>')
api.add_resource(Dump, '/dump')


class API:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

        self.api.add_resource(AskForPasswordChange, '/reset/<string:mail>')
        self.api.add_resource(ConfirmPasswordChange, '/confirm/<string:code>')
        self.api.add_resource(Dump, '/dump')
	app = self.app


    def run(self):
        self.app.run()

