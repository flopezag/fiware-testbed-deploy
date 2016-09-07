#<a name="top"></a>Welcome to FIWARE Testbed Deploy

## Introduction

FIWARE Testbed Deploy is a set sof scripts developed to deploy/undeploy Openstack testbeds required for testings.
It involves the deployment or undeployment of virtual machine using a Cloud infrastructure, and installing the required
 software by using cloud-init functionality. The software involves the installation and configuration of Openstack services.
  a set of scripts to create a secure environment for testing is provided. To execute the fiware-testbed-deploy only it is required to have
some valid credentials to access to a Cloud.

The installation of the testbed is fully automatized and consists on an OpenStack
instance where the original keystone server was replaced with the KeyRock server.
This is work in progress; the current version only installs Glance, Nova and Neutron,
but also purges Swift, Cinder and Blueprint resources.

FIWARE Testbeb Deploy source code can be found [here](https://github.com/telefonicaid/fiware-testbed-deploy.git).


## Documentation

GitHub's [README](../README.md) provides a good documentation summary.
The [Admin Guide](admin.md) and the [User Manual](user.md) cover more advanced topics.

