#!/bin/sh
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
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
# File to execute the covertura and unit test and generate the information
# to be shown in sonar
#
# __author__ = 'fla'
set -e

if [ ! $1 = "travis_build" ];
then
    virtualenv ENV --system-site-packages
    . ENV/bin/activate
fi

mkdir -p target/site/cobertura
mkdir -p target/surefire-reports

pip install -r requirements.txt

#PYCLIPS installation
export SETTINGS_TYPE=test
python setup.py install 
coverage report -m


if [ ! $1 = "travis_build" ];
then
    deactivate
    echo "Deactivate completed"
else
    echo "Travis does not have deactivate command for no reason :SS"
fi
