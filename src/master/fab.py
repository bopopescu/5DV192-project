from fabric import Connection
import subprocess

#
# config
#
HOSTNAME = "master-2"
ZONE = "europe-north1-a"
SSH_USERNAME = 'c15knn'

#
# runtime script
#
host_master = str(subprocess.check_output(['./get-hostname.sh', HOSTNAME, ZONE]).strip().decode("utf-8"))
master = Connection(host_master, user=SSH_USERNAME)
result = master.run('hostname')

print(result)
