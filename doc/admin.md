
# Installation and Administration Guide

## Introduction

This guide defines the procedure to install the FIWARE Testbed Deploy.

For general information, please refer to GitHub's [README](https://github.com/telefonicaid/fiware-testbed-deploy/blob/develop/README.md).

## Build and install

### Requirements
- This scripts has been tested on a Debian 7 system, but any other recent Linux
  distribution with the software described should work

The following software must be installed (e.g. using apt-get on Debian and Ubuntu,
or with yum in CentOS):

- Python 2.7
- pip
- virtualenv

### Installation

The recommend installation method is using a virtualenv. Actually, the installation
process is only about the python dependencies, because the scripts do not need
installation.

1) Create a virtualenv 'deleteENV' invoking *virtualenv deleteENV*
2) Activate the virtualenv with *source deleteENV/bin/activate*
3) Install the requirements running *pip install -r requirements.txt
   --allow-all-external*

## Running FIWARE testbed deploy

### Deploying one testbed


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

The *deploythreeglances.py* script deploys 3 OpenStack Image Repositories (Glance) which share the same
Identity Service called Keystone. Each glance is deployed on a different server accessible by a floating IP.
It is possible to access by SSH Key and its configuration variables are in the file config_vars in
/home/ubuntu folder inside the server, in the same way that it was explained in "Deploying one testbed"
section. These 3 Glance testbeds are used for GlanceSync acceptance tests.
