
# Installation and Administration Guide

## Introduction

This guide defines the procedure to install the FIWARE Testbed Deploy.

For general information, please refer to GitHub's [README](https://github.com/telefonicaid/fiware-testbed-deploy/blob/master/README.md).

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

- 1.- Create a virtualenv 'ENV' invoking *virtualenv ENV*
- 2.- Activate the virtualenv with *source ENV/bin/activate*
- 3.- Install the requirements running *pip install -r requirements.txt
   --allow-all-external*

## Running FIWARE testbed deploy

### Deploying one testbed
To deploy just a testbed, it is required just execute one script (launch_vm.py). This script requires some environment variables
 to be exported before, corresponding
to the Cloud environment where the server is going to be deployed (to install the Openstack inside it).

    export OS_AUTH_URL=<the authentication URL for the keystone in the Cloud>
    export OS_USERNAME=<a user with an account in the Cloud>
    export OS_TENANT_NAME=<a project name from the account in the Cloud>
    export OS_PASSWORD=<the password for an account in the Cloud>
    export OS_REGION_NAME=<the region name>
    export OS_USER_DOMAIN_NAME=<OpenStack user domain name>
    export OS_PROJECT_DOMAIN_NAME=<OpenStack project domain name>
    export BOOKED_IP=<a booked IP in your Cloud infrastructure to deploy the server>
    export Region1=<the name for the region of the Cloud to be deployed>

Then, we execute the launch_vm.py script:

    python fiwaretestbeddeploy/launch_vm.py

The *launch_vm.py* ends in a few seconds, showing the floating IP. Then, it is
 possible to connect to the server using the
SSH key at *~/.ssh/testbedskuld_key*). For an Ubuntu server, it is possible access as:

    ssh ubuntu@floating_ip

Although the server is active, the installation is still running
inside the server and needs a few minutes to complete. Usually the installation
process lasts between 10 and 20 minutes. The job is finished after the file
*config_vars* is copied into the */home/ubuntu* folder inside the virtual machine.

When the installation is finished, the credential may be loaded with *. ~/config_vars*.
The command *nova list* shows a cirros testing server that has been created during the installation
inside the testbed (that is, it is a cirros virtual machine running inside the testbed
virtual machine). The floating IP 192.168.58.201 is associated to this
server (that is the second IP of the pool, the first was assigned to the router). It is
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
same, but with 0GB of disk (i.e. a minimal disk to boot the image is created
but with barely free space)

### Deploying three testbeds
To deploy the three testbeds with the three Glances, it is required execute the script deploythreeglances. This script requires some environment variables
 to be exported before, corresponding
to the Cloud environment where the server is going to be deployed (to install the Openstack inside it).

    export OS_AUTH_URL=<the authentication URL for the keystone in the Cloud>
    export OS_USERNAME=<a user with an account in the Cloud>
    export OS_TENANT_NAME=<a project name from the account in the Cloud>
    export OS_PASSWORD=<the password for an account in the Cloud>
    export OS_REGION_NAME=<the region name>
    export OS_USER_DOMAIN_NAME=<OpenStack user domain name>
    export OS_PROJECT_DOMAIN_NAME=<OpenStack project domain name>
    export BOOKED_IP=<a booked IP in your Cloud infrastructure to deploy the keystone server>
    export Region1=<the name for the first region of the Cloud to be deployed>
    export Region2=<the name for the second region of the Cloud to be deployed>
    export Region3=<the name for the third region of the Cloud to be deployed>

Then, we execute the deploythreeglances.py script:

    python fiwaretestbeddeploy/deploythreeglances.py

The *deploythreeglances.py* script deploys 3 OpenStack Image Repositories (Glance) which share the same
Identity Service called Keystone. Each glance is deployed on a different server accessible by a floating IP.
It is possible to access by SSH Key and its configuration variables are in the file config_vars in
/home/ubuntu folder inside the server, in the same way that it was explained in "Deploying one testbed"
section. These 3 Glance testbeds are used for GlanceSync acceptance tests (see [more information] (https://github.com/telefonicaid/fiware-glancesync/blob/master/README.rst).

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
