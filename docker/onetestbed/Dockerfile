FROM ubuntu
RUN apt-get update && apt-get -y install python-pip python-dev \
  libmysqlclient-dev libpq-dev \
  libxml2-dev libxslt1-dev git \
  libffi-dev netcat zip python-mysqldb
RUN git clone https://github.com/telefonicaid/fiware-testbed-deploy /home/ubuntu/fiware-testbed-deploy/
WORKDIR /home/ubuntu/fiware-testbed-deploy
RUN git pull origin develop
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python setup.py install
RUN mkdir /root/.ssh
COPY start.sh /home/ubuntu/fiware-testbed-deploy/start.sh
CMD ./start.sh
