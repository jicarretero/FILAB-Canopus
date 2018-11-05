import os, inspect
import sys

base_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, base_path)

from functions import *

activate_this = base_path + '/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from OpenstackOps import OpenstackQueries
from ChangePasswordWSGI import app as application
from Config import Config
from Mailer import Mailer
from Store import Store
from functions import *

sys.stdout = open('/tmp/krt_output.logs', 'w')
klog("Abierto fichero de trazas");

config = Config(base_path + "/config.ini")
global_config(config)

OpenstackQueries.get_openstack(config)
Mailer.get_mailer(config)
Store.get_store(config)
