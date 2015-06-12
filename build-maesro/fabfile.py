from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib.files import exists
import os
from os.path import expanduser
import subprocess

home_dir = '/home/vagrant'


def set_remote_hostname():
    sudo('hostname ' + env.host)


# get the IP of a particular host
def get_host_ip(hostname):
    # this ONLY uses DNS. no /etc/hosts
    # ip = subprocess.check_output(['/usr/bin/dig', '+short', hostname])

    # this uses /etc/hosts first then DNS
    ip = ""
    output = subprocess.check_output(['/usr/bin/getent', 'hosts', hostname])
    if len(output) > 0:
        ip = output.split(" ")[0]
    return ip


# somewhat optional, but if we don't do this, it will prompt us yes/no
# for accepting the key for a new server, which we don't want if we're
# fully automated.  or if this is a rebuild, the keys will mismatch
# and it will stop.  
#
# ONLY DO THIS ON SERVER INIT. DO NOT DO THIS EACH TIME WHICH WILL DEFEAT
# THE SECURITY MEASURES.
def register_remote_ssh_keys():
    ssh_dir = home_dir + "/.ssh/"
    known_hosts = ssh_dir + "known_hosts"
    # remove and re-add the new server's SSH key
    ip_of_host = get_host_ip(env.host)
    print("ip is " + ip_of_host)

    if os.path.exists(known_hosts):
        print('removing existing keys')
        local('ssh-keygen -R ' + env.host)
        local('ssh-keygen -R ' + ip_of_host)

    local('ssh-keyscan -H ' + env.host + ' >> ' + known_hosts)
    local('ssh-keyscan -H ' + ip_of_host + ' >> ' + known_hosts)


def init_ssh_keys():
    generate_ssh_key_control_server_if_non_exists()

    # make it so we can SSH into root@localhost as though it was another node
    print("copying SSH key to local root user")
    local("sudo mkdir -p /root/.ssh/")
    local("sudo cp -f ~/.ssh/id_rsa.pub /root/.ssh/authorized_keys")

    register_remote_ssh_keys()


# generate an ssh key
def generate_ssh_key_control_server_if_non_exists():
    if os.path.exists("~/.ssh/id_rsa.pub"):
        return

    local("ssh-keygen -f ~/.ssh/id_rsa -t rsa -C 'root@magfest-vagrant.com' -N '' ")


def test():
    print("TEST")
    print("full hoststring = "+env.host_string)
    print("Executing on %(host)s as %(user)s" % env)
    print("port = " + env.port)
    print("ip_of_host = "+get_host_ip(env.host))
    print("remotely exec'ing: 'uname -a'")
    sudo("uname -a")
