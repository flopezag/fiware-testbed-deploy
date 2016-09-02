# How to use fiware-testbed-deploy with Docker

There are several options to use fiware-testbed-deploy, according to its use:

- _"Deploying one Testbed"_. See Section **1. Deploying one testbed**.
- _"Deploying three Glances"_  . See Section **2. Deploying three glances**.
- _"Destroying testbed"_  . See Section **3. Destroying testbed**.
- _"Deploying phome home"_  . See Section **4. Deploying phome home**.

You do not need to do all of them, just use the one you require. the first one if you want to have a fully operational Skuld instance and maybe third one to check if your Skuld instance run properly.

You do need to have docker in your machine. See the [documentation](https://docs.docker.com/installation/) on how to do this. Additionally, you can use the proper FIWARE Lab docker functionality to deploy dockers image there. See the [documentation](https://docs.docker.com/installation/).


Docker allows you to deploy an fiware-testbed-deploy container in a few minutes. This method requires that you have installed docker or
can deploy container into the FIWARE Lab (see previous details about it).
1. Download [Skuld' source code](https://github.com/telefonicaid/fiware-testbed-deploy) from GitHub (`git clone https://github.com/telefonicaid/fiware-testbed-deploy.git`)
2. `cd fiware-testbed-deploy/docker`

----
## 1. Deploying one testbed

Taking into account that you download the repository from GitHub, this method will launch a container running fiware-tested-deploy, and
execute the script associated to deploy a testbed. You should move to the UnitTests folder `./DeployTestbed`. Just create a new docker image
 executind `docker build -t fiware-deploy-one-testbed -f Dockerfile .`. Please keep in mind that if you do not change the name of the image
 it will automatically update an existing one.

To see that the image is created run `docker images` and you see something like this:

    REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
    fiware-deploy-one-testbed   latest              103464a8ede0        30 seconds ago      551.3 MB

Now is time to execute the container. This time, we take advantage of the docker compose.  Previously you should configure a set variables with the
 FIWARE Lab credentials. You have to define the following environment variables:

    export OS_AUTH_URL=<the authentication URL for the keystone in the Cloud>
    export OS_USERNAME=<a user with an account in the Cloud>
    export OS_TENANT_NAME=<a project name from the account in the Cloud>
    export OS_PASSWORD=<the password for an account in the Cloud>
    export OS_REGION_NAME
    export OS_USER_DOMAIN_NAME=<OpenStack user domain name>
    export OS_PROJECT_DOMAIN_NAME=<OpenStack project domain name>
    export BOOKED_IP
    export Region1=<>
    export KEYSTONE_IP=<IP of the keystone instance>
    export ADM_TENANT_ID=<admin tenant id in the OpenStack environment>
    export ADM_TENANT_NAME=<admin tenant name>
    export ADM_USERNAME=<admin username>
    export ADM_PASSWORD=<admin password>
    export Region1=<Region name>
    export OS_USER_DOMAIN_NAME=<OpenStack user domain name>
    export OS_PROJECT_DOMAIN_NAME=<OpenStack project domain name>


Just execute `docker-compose up` to launch the architecture. You can take a look to the log generated executing `docker-compose logs`. If you want to get the result of the acceptance tests, just execute `docker cp docker_fiware-skuld-aceptance_1:/opt/fiware-skuld/test/acceptance/testreport .`

Please keep in mind that if you do not change the name of the image it will automatically create a new one for unit tests and change the previous one to tag none.


> TIP: If you are trying these methods or run them more than once and come across an error saying that the container already exists you can delete it with `docker rm fiware-skuld-unittests`. If you have to stop it first do `docker stop fiware-skuld-unittests`.

Keep in mind that if you use these commands you get access to the tags and specific versions of Skuld. If you do not specify a version you are pulling from `latest` by default.

----
## 2. Run Acceptance tests

Taking into account that you download the repository from GitHub. This method will launch a container to run
the E2E tests of the Skuld component, previously you should launch or configure a FIWARE Lab access. You have to define the following environment variables:

    export KEYSTONE_IP=<IP of the keystone instance>
    export ADM_TENANT_ID=<admin tenant id in the OpenStack environment>
    export ADM_TENANT_NAME=<admin tenant name>
    export ADM_USERNAME=<admin username>
    export ADM_PASSWORD=<admin password>
    export Region1=<Region name>
    export OS_USER_DOMAIN_NAME=<OpenStack user domain name>
    export OS_PROJECT_DOMAIN_NAME=<OpenStack project domain name>

Take it, You should move to the AcceptanceTests folder `./AcceptanceTests`. Just create a new docker image executing `docker build -t fiware-skuld-acceptance .`. To see that the image is created run `docker images` and you see something like this:

    REPOSITORY                 TAG                 IMAGE ID            CREATED             SIZE
    fiware-skuld-acceptance   latest              eadbe0b2e186        About an hour ago   579.3 MB
    ...

Now is time to execute the container. This time, we take advantage of the docker compose. Just execute `docker-compose up` to launch the architecture. You can take a look to the log generated executing `docker-compose logs`. If you want to get the result of the acceptance tests, just execute `docker cp docker_fiware-skuld-aceptance_1:/opt/fiware-skuld/test/acceptance/testreport .`

Please keep in mind that if you do not change the name of the image it will automatically create a new one for unit tests and change the previous one to tag none.

> TIP: you can launch a FIWARE Lab testbed container to execute the Skuld E2E test. Just follow the indications in [FIWARE Testbed Deploy](https://hub.docker.com/r/fiware/testbed-deploy/). It will launch a virtual machine in which a reproduction of the FIWARE Lab is installed.


Several dockers have been created to deploy the installation of one testbed or three
glances. Even a docker for undeploying the testbed has been created.

To create just one testbed, the following commands are needed:

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

----
## 4. Other info

Things to keep in mind while working with docker containers and Skuld.

### 4.1 Data persistence
Everything you do with Skuld when dockerized is non-persistent. *You will lose all your data* if you turn off the Skuld container. This will happen with either method presented in this README.

### 4.2 Using `sudo`

If you do not want to have to use `sudo` follow [these instructions](http://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo).



