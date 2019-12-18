from fabric.api import *

env.user = 'nygrenkaj'
env.hosts = ['35.190.177.143']
env.use_ssh_config = True

def deploy():

    run('ls')