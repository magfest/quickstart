#!/bin/bash
apt-get install -y fabric python-dev
cd /tmp
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py # install it for python 2.7
pip2 install virtualenv
virtualenv /home/vagrant/env
