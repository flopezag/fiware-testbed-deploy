.. _Top:
=============================
FIWARE Trial Users Management
=============================

|License Badge| |Build Status| |Coveralls|

.. contents:: :local:

Introduction
============



This project is a scripts sets developed to deploy Openstack testbeds.

This project is part of FIWARE_.

Top_


Description
===========

A set of scripts to create a secure environment for testing is provided. The
environment is created in a virtual machine using the FIWARE Lab infrastructure.
The environment variables OS_AUTH_URL, OS_REGION_NAME, OS_USERNAME, OS_PASSWORD
and OS_TENANT_NAME must be filled with the data of a valid FIWARE Lab account.

The installation of the testbed is fully automatized and consists on an OpenStack
instance where the original keystone server was replaced with the KeyRock server.
This is work in progress; the current version only installs Glance, Nova and Neutron,
but skuld also purges Swift, Cinder and Blueprint resources.

To install, it is only necessary to configure the same virtualenv than for
running skuld, set PYTHONPATH with the path of the project, and invoke
the script *./tests/install_testbed/launch_vm.py*.

The script uses a floating IP and creates both a keypair (it saves the SSH private key as
~/.ssh/testbedskuld_key) and a security group. The security group opens
the port 22 (SSH) and allows the ICMP traffic. It is also possible to connect
to any port from a VM using the same security group.

The names of the keypair, the security group and other parameters as the preferable
floating IP are configurable in the *settings.py* file, but most of the users may
ignore this file securely. However, to use the script in a different platform
than FIWARE Lab, probably is necessary to change the parameter about the
public shared network name.

Deploying one testbed
*********************

The *launch_vm.py* ends in a few seconds, showing the floating IP. Although it is
already possible to connect to the ubuntu account of the server (using the
SSH key at *~/.ssh/testbedskuld_key*), the installation is still running
inside the VM and needs a few minutes to complete. Usually the installation
process lasts between 10 and 20 minutes. The job is finished after the file
*config_vars* is copied into the */home/ubuntu* folder inside the virtual machine.

When the installation is finished, the credential may be loaded with *. ~/config_vars*.
The command *nova list* shows a testing VM that has been created during the installation
inside the testbed (that is, it is a virtual machine running inside the testbed
virtual machine). The floating IP 192.168.58.201 is associated to this
VM (that is the second IP of the pool, the first was assigned to the router). It is
possible to connect to the server following this steps:

.. code::

   eval $(ssh-agent -s)
   ssh-add ~/.ssh/testkey
   ip a add dev br-ex 192.168.58.1/24
   ssh cirros@192.168.58.201

Of course, if a new server is instantiated using the same network, there will
be network visibility between both servers, according the rules of the
security groups.

.. code::

    . ~/config_vars
    NETID =
    nova boot testvm2 --poll --flavor micro2 --image cirros --nic net-id=$NETID\
     --key-name testkey --security-groups ssh
    ssh -A cirros@192.168.58.201
    $ ssh cirros@192.168.58.3

The micro flavor provides 64MB of RAM, 1 VCPU and 1GB of disk. The micro2 flavor is the
same, but with 0GB of disk (i.e. a minimal disk to boot the image is created
but with barely free space)

Deploying three testbeds
************************

The *deploythreeglances.py* script deploys three Openstack Image Repository service (Glance) which
shares the same keystone. Each glance is deploy in a different VMs accesible by floating IPs.
As well as previoly, it is possible to access by SSH Key at *~/.ssh/testbedskuld_key*). Usually the installation
process lasts between 10 and 20 minutes. The job is finished after the file
*config_vars* is copied into the */home/ubuntu* folder inside the virtual machines.
This three glance testbed is used for GlanceSync tests.


Build and Install
=================

Requirements
************

- This scripts has been tested on a Debian 7 system, but any other recent Linux
  distribution with the software described should work

The following software must be installed (e.g. using apt-get on Debian and Ubuntu,
or with yum in CentOS):

- Python 2.7
- pip
- virtualenv

Installation
************

The recommend installation method is using a virtualenv. Actually, the installation
process is only about the python dependencies, because the scripts do not need
installation.

1) Create a virtualenv 'deleteENV' invoking *virtualenv deleteENV*
2) Activate the virtualenv with *source deleteENV/bin/activate*
3) Install the requirements running *pip install -r requirements.txt
   --allow-all-external*

Now the system is ready to use. For future sessions, only the step2 is required.

Execution with dockers
**********************
Several dockers have been created to deploy the installation of one testbed or three
glances. Even a docker for undeploying the testbed has been created.

To create just one testbed, it is required, firstly to create the image and then to execute
docker-compose for runnning it

..code::
    docker run -t deploy_one_testbed -f docker/onetestbed/Dockerfile docker/onetestbed
    export OS_AUTH_URL = {the auth uri of the testbed against the tests are going to be execute}
    export OS_USERNAME = {the user name}
    export OS_TENANT_NAME = {the tenant name}
    export OS_PASSWORD = {the password}
    export OS_REGION_NAME = {the region}
    export OS_PROJECT_DOMAIN_NAME = {the project domain name}
    export OS_USER_DOMAIN_NAME = {the user domain name}
    export Region1 = {The region name for the deployed testbed}
    export BOOKED_IP = {The floating Ip for the keystone}
    docker-compose -f docker/onetestbed/docker-compose.yml up

In case, we want to deploy the three glance testbeds, it is required:
..code::
    docker run -t deploy-three-glances -f docker/threeglances/Dockerfile docker/threeglances/
    export OS_AUTH_URL = {the auth uri of the testbed against the tests are going to be execute}
    export OS_USERNAME = {the user name}
    export OS_TENANT_NAME = {the tenant name}
    export OS_PASSWORD = {the password}
    export OS_REGION_NAME = {the region}
    export OS_PROJECT_DOMAIN_NAME = {the project domain name}
    export OS_USER_DOMAIN_NAME = {the user domain name}
    export Region1 = {The region name for the first deployed testbed}
    export Region2 = {The region name for the second deployed testbed}
    export Region3 = {The region name for the third deployed testbed}
    export BOOKED_IP = {The floating Ip for the keystone}
    docker-compose -f docker/threeglances/docker-compose.yml up

And finally, when we want to undeploy the testbeds:
..code::
    docker run -t delete_testbed -f docker/destroy_testbed/Dockerfile docker/destroy_testbed/
    export OS_AUTH_URL = {the auth uri of the testbed against the tests are going to be execute}
    export OS_USERNAME = {the user name}
    export OS_TENANT_NAME = {the tenant name}
    export OS_PASSWORD = {the password}
    export OS_REGION_NAME = {the region}
    export OS_PROJECT_DOMAIN_NAME = {the project domain name}
    export OS_USER_DOMAIN_NAME = {the user domain name}
    docker-compose -f docker/destroy_testbed/docker-compose.yml up


License
=======

\(c) 2016 Telefónica I+D, Apache License 2.0

.. IMAGES

.. |Build Status| image:: https://travis-ci.org/telefonicaid/fiware-testbed-deploy.svg?branch=develop
   :target: https://travis-ci.org/telefonicaid/fiware-testbed-deploy
   :alt: Build status
.. |Coveralls| image:: https://coveralls.io/repos/telefonicaid/fiware-testbed-deploy/badge.svg?branch=develop&service=github
   :target: https://coveralls.io/github/telefonicaid/fiware-testbed-deploy?branch=develop
   :alt: Unit tests coverage
.. |License Badge| image:: https://img.shields.io/badge/license-Apache_2.0-blue.svg
   :target: LICENSE
   :alt: Apache 2.0

.. REFERENCES

.. _FIWARE: http://www.fiware.org/
.. _stackoverflow: http://stackoverflow.com/questions/ask
.. _`FIWARE Q&A`: https://ask.fiware.org
