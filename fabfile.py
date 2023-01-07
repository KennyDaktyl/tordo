from __future__ import with_statement

import os

from fabric.api import *
from contextlib import contextmanager as _contextmanager

# local_user = "michalp"
local_user = "kenny"

env.hosts = os.environ.get("IP_HOST", "51.75.64.242")
env.port = os.environ.get("SSH_PORT", "62211")
env.user = os.environ.get("HOST_USER", "kenny")
env.password = os.environ.get("SSH_PASSWORD")
# env.key_filename = "/home/michalp/.ssh/id_rsa_vps"
env.key_filename = "/home/kenny/.ssh/id_rsa_vps"
env.directory = "/home/kenny/www/tordo"
env.activate = "source {}/env/bin/activate".format(env.directory)
env.export = f'export DB_USER={os.environ.get("DB_USER")} && export DB_PASSWORD={os.environ.get("DB_PASSWORD")}'.format(
    env.directory
)


@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            with prefix(env.export):
                yield


#  fab -f fabfile.py deploy
def deploy():
    local("git add .")
    local('git commit -m "deploy z fabric"')
    local("git push")
    with virtualenv():
        run("sudo git pull")
        run(
            "sudo /home/kenny/www/tordo/env/bin/python manage.py collectstatic --noinput"
        )
        run("sudo /home/kenny/www/tordo/env/bin/python manage.py compress --force")
        run("python manage.py migrate")
        run("sudo systemctl restart tordo.service")


#  fab -f fabfile.py backup_db
def backup_db():
    password = os.environ.get("DB_PASSWORD")
    run(
        'sudo PGPASSWORD="'
        + password
        + '" pg_dump -U postgres -h localhost tordo_dev > /home/kenny/www/tordo/media/files/tordo_dev_backup.sql'
    )
    local(
        f'sshpass -p {os.environ.get("SSH_PASSWORD")} scp -r -P 62211 kenny@51.75.64.242:/home/kenny/www/tordo/media/files/tordo_dev_backup.sql /home/{local_user}/Pulpit/Backup'
    )


#  fab -f fabfile.py restore_local_db
def restore_local_db():
    local(
        f'sshpass -p {os.environ.get("SSH_PASSWORD")} scp -r -P 62211 kenny@51.75.64.242:/home/kenny/www/tordo/media/files/tordo_dev_backup.sql /home/{local_user}/Pulpit/Backup'
    )
    local(
        f'PGPASSWORD={os.environ.get("SSH_PASSWORD")} dropdb -U postgres -h localhost tordo_dev'
    )
    local(
        f'PGPASSWORD={os.environ.get("SSH_PASSWORD")} createdb -U postgres -h localhost tordo_dev'
    )
    local(
        f'PGPASSWORD={os.environ.get("SSH_PASSWORD")} psql -U postgres -h localhost tordo_dev < /home/{local_user}/Pulpit/Backup/tordo_dev_backup.sql'
    )


def push(message=""):
    local("git status")
    local("git add .")
    local('git commit -m "deploy z fabric"')
    local("git push")
