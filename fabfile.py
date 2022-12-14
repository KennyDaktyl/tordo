from __future__ import with_statement
from fabric.api import *

env.hosts = ['51.75.64.242']
env.port = '62211'
env.user = 'kenny'
env.key_filename = '/home/michalp/.ssh/id_rsa_vps'


def deploy():
    with cd('/home/kenny/www/tordo'):
        # run('git pull')
        run('sudo source env/bin/activate')
        run('sudo source env/export.txt')
        run('python manage.py collectstatic --noinput')
        run('python manage.py compress --force')
        run('sudo systemctl restart tordo.service')


def push(message=""):
    local('git status')
    local('git add .')
    local('git commit -m "' + message + '"')
    local('git push')
