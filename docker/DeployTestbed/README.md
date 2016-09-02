# How to use fiware-testbed-deploy for deploying a testbed with Docker

A set of scripts to create a secure environment for testing is provided. The
environment is created in a virtual machine using a Cloud infrastructure.
The installation of the testbed is fully automatized and consists on an OpenStack
instance where the original keystone server was replaced with the KeyRock server.
This is work in progress; the current version only installs Glance, Nova and Neutron,
but skuld also purges Swift, Cinder and Blueprint resources.

Docker allows you to deploy an fiware-testbed-deploy container, which deploys a VM with a Cloud infrastructure in a few minutes.
This method requires that you have installed docker or can deploy container into the FIWARE Lab (see previous details about it).
1. Download [Skuld' source code](https://github.com/telefonicaid/fiware-testbed-deploy) from GitHub (`git clone https://github.com/telefonicaid/fiware-testbed-deploy.git`)
2. `cd fiware-testbed-deploy/docker/DeployTestbed`

Then, you just need to create a new docker image executing `docker build -t fiware-deploy-one-testbed -f Dockerfile .`. Please keep in mind that if you do not change the name of the image
 it will automatically update an existing one.

To see that the image is created run `docker images` and you see something like this:

    REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
    fiware-deploy-one-testbed   latest              103464a8ede0        30 seconds ago      551.3 MB

Now is time to execute the container. This time, we take advantage of the docker compose.  Previously you should configure a set variables with the
 FIWARE Lab (or a Cloud) credentials. You have to define the following environment variables:

    export OS_AUTH_URL=<the authentication URL for the keystone in the Cloud>
    export OS_USERNAME=<a user with an account in the Cloud>
    export OS_TENANT_NAME=<a project name from the account in the Cloud>
    export OS_PASSWORD=<the password for an account in the Cloud>
    export OS_REGION_NAME=<the region name>
    export OS_USER_DOMAIN_NAME=<OpenStack user domain name>
    export OS_PROJECT_DOMAIN_NAME=<OpenStack project domain name>
    export BOOKED_IP=<a booked IP in your Cloud infrastructure to deploy the VM>
    export Region1=<the name for the region of the Cloud to be deployed>

Just execute `docker-compose up` to launch the architecture. You can take a look to the log generated executing `docker-compose logs`. You will see
that a VM will be deployed and some software is installed. Then you will see a set of logs, specifiying that the VM is being booting and that keystone and
all the services in Openstack have been deployed.

   [36mdeploy_one_testbed_1 | [0mValladolid: VM with UUID 6a380709-e32a-45f5-9ec8-ea2450f24775
   [36mdeploy_one_testbed_1 | [0mWaiting for ACTIVE status. (Try 1/30)
   [36mdeploy_one_testbed_1 | [0mWaiting for ACTIVE status. (Try 2/30)
   [36mdeploy_one_testbed_1 | [0mKeystone IP 130.206.125.56
   [36mdeploy_one_testbed_1 | [0mRegion1 IP: Valladolid 130.206.125.56
   [36mdeploy_one_testbed_1 | [0mAssigning floating IP 130.206.125.56
   [36mdeploy_one_testbed_1 | [0mwaiting for keystone
   [36mdeploy_one_testbed_1 | [0mwaiting for testbed one

----
## 4. Other info

Things to keep in mind while working with docker containers and Skuld.

### 4.1 Data persistence
Everything you do with Skuld when dockerized is non-persistent. *You will lose all your data* if you turn off the Skuld container. This will happen with either method presented in this README.

### 4.2 Using `sudo`

If you do not want to have to use `sudo` follow [these instructions](http://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo).



