FROM ubuntu
RUN apt-get update && apt-get -y install python-pip python-dev \
  libmysqlclient-dev libpq-dev \
  libxml2-dev libxslt1-dev git \
  libffi-dev zip python-mysqldb netcat
RUN git clone https://github.com/telefonicaid/fiware-testbed-deploy/ /home/ubuntu/fiware-testbed-deploy/
WORKDIR /home/ubuntu/fiware-testbed-deploy/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install python-openstackclient
RUN mkdir /root/.ssh
COPY start.sh /home/ubuntu/fiware-testbed-deploy/start.sh
CMD ./start.sh
