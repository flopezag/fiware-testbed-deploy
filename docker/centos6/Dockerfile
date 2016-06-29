# docker build -t fiwarecentos:6.6 .

FROM centos:6.6
WORKDIR /opt
RUN yum update -y && yum install -y system-config-firewall gcc git wget tar zlib-devel bzip2-devel openssl-devel ncurses-devel openssh-server openssh-clients
RUN wget http://python.org/ftp/python/2.7.6/Python-2.7.6.tgz
RUN tar -xzf Python-2.7.6.tgz
RUN cd Python-2.7.6;./configure --prefix=/usr/local --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
RUN cd Python-2.7.6;make && make altinstall
RUN wget --no-check-certificate http://pypi.python.org/packages/source/d/distribute/distribute-0.6.35.tar.gz
RUN tar xf distribute-0.6.35.tar.gz
RUN cd distribute-0.6.35;python2.7 setup.py install
RUN easy_install-2.7 pip
RUN pip2.7 install --upgrade setuptools
RUN pip2.7 install --upgrade distribute
