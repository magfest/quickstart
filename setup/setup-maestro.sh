#!/bin/bash
apt-get install -y fabric
cd /tmp
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
pip install virtualenv
virtualenv /home/vagrant/env
