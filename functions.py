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


import string
import random
import inspect, os
import sys


def random_string(n):
    s = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(n))
    print "returning " +s 
    return s


def my_path():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory


cfg = None
def global_config(c=None):
    global cfg
    if c is not None:
        cfg = c
    return cfg


def klog(str):
    print str
    sys.stdout.flush()
