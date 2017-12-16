**WARNING: SUPPORT FOR THIS PROJECT IS DOSCONTINUED AND THIS REPOSITORY IS NO MORE MAINTANED**

#<a name="top"></a>FIWARE Testbed Deploy

[![License badge](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](LICENSE)
[![Documentation badge](https://readthedocs.org/projects/fiware-testbed-deploy/badge/?version=latest)](http://fiware-testbed-deploy.readthedocs.org/en/latest/?badge=latest)
[![Docker badge](https://img.shields.io/docker/pulls/fiware/fiware-testbed-deploy.svg)](https://hub.docker.com/r/fiware/deploy-one-testbed/)

* [Introduction](#introduction)
* [Overall description](#overall-description)
* [Build and Install](#build-and-install)
* [API Overview](#api-overview)
* [Testing](#testing)
    * [Unit Tests](#unit-tests)
    * [End-to-end tests](#end-to-end-tests)
* [Advanced topics](#advanced-topics)
* [Support](#support)
* [License](#license)


## Introduction

This is the code repository for **FIWARE Testbed Deploy component**. This project is a scripts sets developed to deploy Openstack testbeds

This project is part of [FIWARE](http://www.fiware.org).

Any feedback on this documentation is highly welcome, including bugs, typos
or things you think should be included but aren't. You can use [github issues](https://github.com/telefonicaid/fiware-testbed-deploy/issues/new) to provide feedback.

[Top](#top)

## Overall description
A set of scripts to create a secure environment for testing is provided. The
environment is created in a virtual machine using the FIWARE Lab infrastructure.
The environment variables OS_AUTH_URL, OS_REGION_NAME, OS_USERNAME, OS_PASSWORD
and OS_TENANT_NAME must be filled with the data of a valid FIWARE Lab account.

The installation of the testbed is fully automatized and consists on an OpenStack
instance where the original keystone server was replaced with the KeyRock server.
This is work in progress; the current version only installs Glance, Nova and Neutron,
but also purges Swift, Cinder and Blueprint resources.

### Deploying one testbed
By using a fiware-testbed-deploy script (*launch_vm.py*), it is possible to deploy an entire Openstack testbed.
The script uses a floating IP and creates both a keypair (it saves the SSH private key as
~/.ssh/testbedskuld_key) and a security group. The security group opens
the port 22 (SSH) and allows the ICMP traffic. It is also possible to connect
to any port from a VM using the same security group.

The names of the keypair, the security group, the booked floating IP are configurable in
the *settings.py* file, but most of the users may
ignore this file securely. However, to use the script in a different platform
than FIWARE Lab, probably is necessary to change the parameter about the
public shared network name.

Although it is already possible to connect to the ubuntu account of the server, the installation is still running
inside the server and needs a few minutes to complete. Usually the installation
process needs between 10 and 20 minutes. The job is finished after the file
*config_vars* is copied into the */home/ubuntu* folder inside the virtual machine.

When the installation is finished, the credential may be loaded with *. ~/config_vars*.
The command *nova list* shows a cirros testing server that has been created during the installation
inside the testbed (that is, it is a cirros virtual machine running inside the testbed
virtual machine). The floating IP 192.168.58.201 is associated to this
VM (that is the second IP of the pool, the first was assigned to the router). It is
possible to connect to the server following this steps:

    eval $(ssh-agent -s)
    ssh-add ~/.ssh/testkey
    ip a add dev br-ex 192.168.58.1/24
    ssh cirros@192.168.58.201

Of course, if a new server is instantiated using the same network, there will
be network visibility between both servers, according the rules of the
security groups.

     . ~/config_vars
     NETID =
     nova boot testvm2 --poll --flavor micro2 --image cirros --nic net-id=$NETID\
      --key-name testkey --security-groups ssh
     ssh -A cirros@192.168.58.201
     $ ssh cirros@192.168.58.3

The micro flavor provides 64MB of RAM, 1 VCPU and 1GB of disk. The micro2 flavor is the
same, but without extra disk (i.e. a minimal disk to boot the image is created
but with barely free space).

### Deploying three testbeds

The *deploythreeglances.py* script deploys 3 OpenStack Image Repositories (Glance) which share the same
Identity Service called Keystone. Each Glance is deployed on a different server accessible by a floating IP.
It is possible to access by SSH Key and their configuration variables are in the file config_vars in
/home/ubuntu folder inside the server, in the same way that it was explained in "Deploying one testbed"
section. These 3 Glance testbeds are used for GlanceSync acceptance tests (see [more information] (https://github.com/telefonicaid/fiware-glancesync/blob/master/README.rst).

### Undeploy testbed
The *destroytestbeds.py* script undeploys an Openstack testbed belonging to the user specified in the environment variables.

### Deploy phonehome
The script *launch_vm_phonehome* deploys a VM in a Cloud infrastructure, with all the security groups rules and software required
to execute the phone home.

[Top](#top)

## Build and install

### Requirements

The following software must be installed (e.g. using apt-get on Debian and Ubuntu,
or with yum in CentOS):

- Python 2.7
- pip
- virtualenv

### Installation

The recommended installation method is using a virtualenv. Actually, the installation
process is only about the python dependencies, because the scripts do not need
installation.

- 1. Create a virtualenv 'ENV' invoking *virtualenv ENV*
- 2. Activate the virtualenv with *source ENV/bin/activate*
- 3. Install the requirements running *pip install -r requirements.txt
   --allow-all-external*

Now the system is ready to use. Just it is needed to execute the right script,
[Top](#top)

## Sanity check procedures

The Sanity Check procedures are the steps that a System Administrator
takes to verify that an installation is ready to be tested. This is
therefore a preliminary set of tests to ensure that obvious or basic
malfunctioning is fixed before proceeding to unit tests, integration
tests and user validation.

### End to End testing

As fiware-testbed-deploy is composed by a set of scripts without any API, there
is not a simple way to do an end-to-end testing. If we want to test, we should execute
one of the scripts, for instance *launch_vm.py*, which deploys a server and installs an entire
Opentack.

To do that, just export these set of variables:

    export OS_AUTH_URL=<the authentication URL for the keystone in the Cloud>
    export OS_USERNAME=<a user with an account in the Cloud>
    export OS_TENANT_NAME=<a project name from the account in the Cloud>
    export OS_PASSWORD=<the password for an account in the Cloud>
    export OS_REGION_NAME=<the region name>
    export OS_USER_DOMAIN_NAME=<OpenStack user domain name>
    export OS_PROJECT_DOMAIN_NAME=<OpenStack project domain name>
    export BOOKED_IP=<a booked IP in your Cloud infrastructure to deploy the server>
    export Region1=<the name for the region of the Cloud to be deployed>

And execute:

    fiwaretestbeddeploy/launch_vm.py

If everything works correctly, you will obtain a set of logs like that:

    RegionOne: VM with UUID 6a380709-e32a-45f5-9ec8-ea2450f24775
    Waiting for ACTIVE status. (Try1 /30)
    Waiting for ACTIVE status. (Try 2/30)
    Keystone IP 130.206.125.56
    Region1 IP: RegionOne 130.206.125.56
    Assigning floating IP 130.206.125.56
    waiting for keystone
    waiting for testbed one

[Top](#top)

## Support

Ask your thorough programming questions using [stackoverflow](http://stackoverflow.com/questions/ask)
and your general questions on [FIWARE Q&A](https://ask.fiware.org). In both cases please use the tag `fiware-testbed-deploy`

[Top](#top)

## License

\(c) 2015-2016 Telefónica I+D, Apache License 2.0
