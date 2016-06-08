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

FIWARE_DEFAULT_CLOUD_ROLE_ID = '8605715701e44bf5be1e2fbe49cab0'


class GenerateUser(object):
    """Class to generate users."""
    def __init__(self, user_name, password, tenant_name, role_name):
        """constructor"""
        endpoint = 'http://{ip}:{port}/v3'.format(ip=os.environ["KEYSTONE_HOST"],
                                              port=5000)
        self.keystone = client.Client(
            username="idm",
            password="idm",
            project_name="idm",
            auth_url=endpoint)
        self.id = user_name + ' id'
        self.user_name = user_name
        self.password = password
        self.tenant_name = tenant_name
        self.role_name = role_name

    def add_domain_user_role(self, user, role, domain):
        """ It adds a role to a user.
        :param user: the user
        :param role: the role to add
        :param domain: the domain
        :return:
        """
        manager = self.keystone.roles
        return manager.grant(role, user=user, domain=domain)

    def update_to_community(self, user, duration=None):
        """ It updates the role community to the user.
        :param user: the user
        :param duration: the duration
        :return:
        """
        community_role = self.keystone.roles.find(name="community")
        date = str(datetime.date.today())

        if not duration:
            duration = 180
        self.keystone.users.update(user, community_started_at=date, community_duration=duration)
        self.add_domain_user_role(
            user=user,
            role=community_role.id,
            domain='default')

    def update_to_basic(self, user):
        """ It updates the user to basic
        :param user: the user
        :return:
        """
        basic_role = self.keystone.roles.find(name="basic")
        self.add_domain_user_role(
            user=user,
            role=basic_role.id,
            domain='default')

    def update_to_trial(self, user):
        """ It updates the role trial to the user.
        :param user: the user
        :return:
        """
        trial_role = self.keystone.roles.find(name="trial")
        self.add_domain_user_role(
            user=user,
            role=trial_role.id,
            domain='default')

    def get_purchaser_role(self):
        """ It gets the purcharse role.
        :return:
        """
        role_id = FIWARE_DEFAULT_CLOUD_ROLE_ID
        return self.keystone.roles.get(role_id)

    def add_to_organization(self, user):
        """
        It adds the community the user to the organization.
        :param user: the user
        :return:
        """
        purchaser = self.keystone.roles.find(name="basic")
        FIWARE_CLOUD_APP = 'Cloud'
        self.keystone.fiware_roles.roles.add_to_organization(
            role=purchaser,
            organization=user.cloud_project_id,
            application=FIWARE_CLOUD_APP)

    def create_user(self):
        """ It creates a user
        :return:
        """
        users = self.keystone.users.list(username=self.user_name)
        if not users:
            user = self.keystone.user_registration.users.register_user(
                self.id,
                domain="default",
                password=self.password,
                username=self.user_name)

            user = self.keystone.user_registration.users.activate_user(
                user=user.id,
                activation_key=user.activation_key)
        else:
            user = users[0]

        if self.role_name == "community":
            self.update_to_community(user, 100)
        elif self.role_name == "trial":
            self.update_to_trial(user)
        else:
            self.update_to_basic(user)


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
