#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2016 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-Core project.
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
import generate_users


def create_users(role):
    """
    It create a set of users with the required role.
    :param role: the role
    :return:
    """
    vars = [1, 2, 3, 4]
    for i in vars:
        create = generate_users.GenerateUser(user_name="{0}_username{1}".format(role, i),
                                             password="{0}_password{1}".format(role, i),
                                             tenant_name="{0}_tenantname{1}".format(role, i),
                                             role_name="role")
        create.create_user()


if __name__ == '__main__':
    create_users("basic")
    create_users("community")
    create_users("trial")
    create = generate_users.GenerateUser("test", "test", "test", "community")
    create.create_user()
