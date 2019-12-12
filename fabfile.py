from fabric.api import *

env.user = 'nygrenkaj'
env.hosts = ['35.190.177.143']
env.use_ssh_config = True

def deploy():

    run('git clone git@github.com:nygrenkaj/5DV192-project.git')
    run('gcloud ...')
