# How to use fiwarecentos with Docker

It includes the deployment of a CentOS 6 image with some FIWARE features, like Python 7.

## 1. Generating docker image
Docker allows you to deploy an fiwarecentos container.

  1. Download [fiware-testbed-deploy' source code](https://github.com/telefonicaid/fiware-testbed-deploy) from GitHub (`git clone https://github.com/telefonicaid/fiware-testbed-deploy.git`)
  2. `cd fiware-testbed-deploy/docker/FiwareCentos`

Then, you just need to create a new docker image executing `docker build -t fiwarecentos -f Dockerfile .`. Please keep in mind that if you do not change the name of the image
 it will automatically update an existing one.

To see that the image is created run `docker images` and you see something like this:

    REPOSITORY     TAG                 IMAGE ID            CREATED             SIZE
    fiwarecentos   latest              103464a8ede0        30 seconds ago      551.3 MB



## 2. Running docker image
Now is time to execute the container. Just execute:

    docker run fiwarecentos


----
## 3. Other info

Things to keep in mind while working with docker containers and fiwarecentos.

### 3.1 Data persistence
Everything you do with fiwarecentos when dockerized is non-persistent. *You will lose all your data* if you turn off thefiwarecentos container. This will happen with either method presented in this README.

### 3.2 Using `sudo`

If you do not want to have to use `sudo` follow [these instructions](http://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo).



