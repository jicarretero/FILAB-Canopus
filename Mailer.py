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


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from Config import Config


class Mailer:
    instance = None

    def __init__(self, config):
        self.config = config

        self.recover_html_template = open(config.recover_html_template, 'r').read()
        self.recover_text_template = open(config.recover_text_template, 'r').read()
        self.new_password_html_template = open(config.new_password_html_template, 'r').read()
        self.new_password_text_template = open(config.new_password_text_template, 'r').read()
        self.recover_subject = config.recover_subject

        self.recover_2_html = Template(self.recover_html_template)
        self.recover_2_text = Template(self.recover_text_template)
        self.new_password_2_html = Template(self.new_password_html_template)
        self.new_password_2_text = Template(self.new_password_text_template)
        self.new_password_subject = config.new_password_subject

    def send_recover_link(self, to, link):
        message_html = self.recover_2_html.render(change_password_link=link)
        message_text = self.recover_2_text.render(change_password_link=link)
        self.send_multipart(to, self.recover_subject, message_html, message_text)

    def send_new_password(self, to, password):
        message_html = self.new_password_2_html.render(new_password=password)
        message_text = self.new_password_2_text.render(new_password=password)
        self.send_multipart(to, self.new_password_subject, message_html, message_text)

    def send_multipart(self, to, subject, message_html, message_text):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject

        part1 = MIMEText(message_text, 'plain')
        part2 = MIMEText(message_html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        s = smtplib.SMTP(self.config.email_host)
        try:
            msg['From'] = self.config.from_name
            msg['To'] = to
            s.sendmail(self.config.email_from, [to], msg.as_string())
            print "mail sent: ", to
        except Exception as e:
            print "Error sending mail to: ", to
            print e
        s.quit()

    @classmethod
    def get_mailer(cls, config=None):
        if cls.instance is None:
            cls.instance = Mailer(config)
        return cls.instance


if __name__ == "__main__":
    config = Config("config.ini")
    Mailer.get_mailer(config)

    mailer = Mailer.get_mailer()
    mailer.send_recover_link("joseignacio.carretero@gmail.com", "https://admtools.lab.fiware.org/ip/")
    mailer.send_new_password("joseignacio.carretero@gmail.com", "requetepiruleja")
