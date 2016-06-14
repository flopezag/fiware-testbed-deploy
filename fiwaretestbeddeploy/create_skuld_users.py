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

if __name__ == '__main__':
    create = generate_users.GenerateUser("community_user", "community_user", "community_user", "community")
    create.create_user()
    create = generate_users.GenerateUser("trial_user", "trial_user", "trial_user", "trial")
    create.create_user()
    create = generate_users.GenerateUser("basic_user", "basic_user", "basic_user", "basic")
    create.create_user()
    create = generate_users.GenerateUser("test", "test", "test", "community")
    create.create_user()
