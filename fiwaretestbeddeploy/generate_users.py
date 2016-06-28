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

import os
from keystoneclient.v3 import client
import datetime
from utils.osclients import osclients
from subprocess import Popen, PIPE
import json


class GenerateUser(object):
    """Class to generate users."""
    def __init__(self, user_name, password, tenant_name, role_name=None):
        """constructor"""
        keystone_ip = self.get_keystone_host()
        endpoint = 'http://{ip}:{port}/v3'.format(ip=keystone_ip,
                                                  port=5000)
        self.keystone = client.Client(
            username="idm",
            password="idm",
            project_name="idm",
            auth_url=endpoint)
        self.user_name = user_name
        self.password = password
        self.tenant_name = tenant_name
        self.role_name = role_name

    def get_keystone_host(self):
        p = Popen(["curl", "http://169.254.169.254/openstack/latest/meta_data.json"], stdout=PIPE)
        metadatajson, err = p.communicate()
        meta = json.loads(metadatajson)["meta"]
        return meta["keystone_ip"]

    def add_domain_user_role(self, user, role, domain):
        """ It adds a role to a user.
        :param user: the user
        :param role: the role to add
        :param domain: the domain
        :return:
        """
        manager = self.keystone.roles
        return manager.grant(role, user=user, domain=domain)

    def update_domain_to_role(self, user, role_name, duration=100):
        """
        It updates the domain to the role
        :param user: the user
        :param role_name: the role
        :param duration: the duration for community
        :return:
        """
        role = self.keystone.roles.find(name=role_name)

        date_out = str(datetime.date.today() - datetime.timedelta(days=30))
        date_out_2 = str(datetime.date.today() - datetime.timedelta(days=180))

        if self.role_name == "community":
            self.keystone.users.update(user, community_started_at=date_out_2, community_duration=duration)

        if self.role_name == "trial":
            self.keystone.users.update(user, trial_started_at=date_out)

        self.add_domain_user_role(
            user=user,
            role=role.id,
            domain='default')

    def create_user(self):
        """ It creates a user
        :return:
        """
        print("Create user {0}".format(self.user_name))
        users = self.keystone.users.list(username=self.user_name)
        if not users:
            user = self.keystone.user_registration.users.register_user(
                self.user_name,
                domain="default",
                password=self.password,
                username=self.user_name)

            self.keystone.user_registration.users.activate_user(
                user=user.id,
                activation_key=user.activation_key)
            users = self.keystone.users.list(username=self.user_name)

        if self.role_name:
            self.update_domain_to_role(users[0], self.role_name)
            self.update_quota(users[0], self.role_name)

    def update_quota(self, user, role):
        """ It updates the quota for the user according to role requirements
        :param user: the user
        :param role: the role
        :return: nothing
        """
        nova_c = osclients.get_novaclient()
        neutron_c = osclients.get_neutronclient()
        kargs = self.get_nova_quota(user, role)
        nova_c.quotas.update(user.cloud_project_id, **kargs)
        neutron_c.update_quota(user.cloud_project_id, self.get_neutron_quota(role))

    def get_neutron_quota(self, role):
        """
        It gets the neutron quota parameters
        :param role: the user role
        :return:
        """
        if role == 'community':
            return {"quota": {"subnet": 1, "network": 1, "floatingip": 1,
                              "security_group_rule": 20, "security_group": 20,
                              "router": 1, "port": 10}}
        elif role == 'trial':
            return {"quota": {"subnet": 0, "network": 0, "floatingip": 1,
                              "security_group_rule": 10, "security_group": 10,
                              "router": 0, "port": 10}}
        else:
            return {"quota": {"subnet": 0, "network": 0, "floatingip": 0,
                              "security_group_rule": 0, "security_group": 0,
                              "router": 0, "port": 0}}

    def get_nova_quota(self, user, role):
        """
        It gest the nova quota parameters
        :param user: the user
        :param role: the role
        :return: nothing
        """

        if role == 'basic':
            return {"user_id": user.id, "instances": 0, "ram": 0,
                    "cores": 0, "floating_ips": 0}
        elif role == "trial":
            return {"user_id": user.id, "instances": 3, "ram": 0,
                    "cores": 0, "floating_ips": 1}
        else:
            return {"user_id": user.id, "instances": 5, "ram": 10240,
                    "cores": 10, "floating_ips": 0}

# If the program receives a parameter, it is interpreted as a file with the
# JSON to register. Otherwise, it uses default_region_json, replacing the
# variables with the environment.
if __name__ == '__main__':
    create = GenerateUser("community_user", "community_user", "community_user", "community")
    create.create_user()
    create = GenerateUser("trial_user", "trial_user", "trial_user", "trial")
    create.create_user()
    create = GenerateUser("basic_user", "basic_user", "basic_user", "basic")
    create.create_user()
    create = GenerateUser("test", "test", "test", "community")
    create.create_user()
