#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2016 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FIWARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#

"""script to change idm user default password with a random one"""

import os.path
from subprocess import check_call
import time
import json
from subprocess import Popen, PIPE
import socket
import errno

from utils.change_password import PasswordChanger
from utils.osclients import OpenStackClients


def wait_net_service(server, port, timeout=None):
    """ Wait for network service to appear
        @param timeout: in seconds, if None or 0 wait forever
        @return: True of False, if timeout is None may return only True or
                 throw unhandled network exception
    """

    s = socket.socket()
    if timeout:
        from time import time as now
        # time module is needed to calc timeout shared between two exceptions
        end = now() + timeout

    while True:
        try:
            if timeout:
                next_timeout = end - now()
                if next_timeout < 0:
                    return False
                else:
                    s.settimeout(next_timeout)

            s.connect((server, port))

        except socket.timeout, err:
            # this exception occurs only if timeout is set
            if timeout:
                return False

        except socket.error, err:
            # catch timeout exception from underlying network library
            # this one is different from socket.timeout
            pass
        else:
            s.close()
            return True

file_path = '/home/ubuntu/idm/conf/settings.py'
etckeystone_path = '/home/ubuntu/idm/keystone/etc/keystone.conf'

# reset the password
p2 = Popen(["curl", "http://169.254.169.254/openstack/latest/meta_data.json"], stdout=PIPE)
metadatajson, err = p2.communicate()
meta = json.loads(metadatajson)["meta"]
keystone_ip = meta["keystone_ip"]
region = meta["Region"]
region2 = meta["region_keystone"]
if region2:
    os.environ['OS_REGION_NAME'] = region2

wait_net_service(keystone_ip, 5000, timeout=720)

osclients = OpenStackClients('http://{0}:5000/v3/'.format(keystone_ip))

osclients.set_credential('idm', 'idm', 'idm')

# create idm region user

password_changer = PasswordChanger(osclients)
idm = password_changer.get_user_byname("idm")
idm = password_changer.get_user_byname('idm')
# new_password = password_changer.reset_password(idm)
new_password = 'idm'


credential = """export OS_AUTH_URL=http://{0}:5000/v3/
export OS_AUTH_URL_V2=http://{0}:5000/v2.0/
export OS_USERNAME={2}
export OS_TENANT_NAME=idm
export OS_PROJECT_DOMAIN_NAME=default
export OS_USER_DOMAIN_NAME=default
export OS_REGION_NAME={3}
export OS_IDENTITY_API_VERSION=3
""".format(keystone_ip, keystone_ip, "idm", region)

# Generate the credential file
with open(os.path.expanduser('~/credential'), 'w') as f:
    f.write(credential)
    f.write('export OS_PASSWORD=' + new_password + '\n')

# Change the password in the settings file
content = open(file_path).read()
content = content.replace("'password': 'idm'", "'password': '" +
                          new_password + "'")
content = content.replace("KEYSTONE_ADMIN_TOKEN = 'ADMIN'",
                          "KEYSTONE_ADMIN_TOKEN = '" + new_password + "'")

with open(file_path, 'w') as f:
    f.write(content)

# Change the admin token in the keystone config file
os.environ['OS_REGION_NAME'] = region
content = open(etckeystone_path).read()
content = content.replace("admin_token=ADMIN", "admin_token=" + new_password)
check_call(['sudo', 'chmod', '777', etckeystone_path])
with open(etckeystone_path, 'w') as f:
    f.write(content)
check_call(['sudo', 'chmod', '600', etckeystone_path])

# Restart keystone to apply admin_token change
check_call(['sudo', 'service', 'keystone_idm', 'restart'])

# Pause needed before running other commands that connects to keystone
time.sleep(10)
