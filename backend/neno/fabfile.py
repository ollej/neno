from djangofab.api import *
from django.conf import settings
from djangofab.vcs.git import update_remote, update_local, push, commit, add, local
env.capture_default = False

env.tarball = '../../releases/neno_latest.tgz'

# apply the settings from fab.cfg default section
# sets DJANGO_SETTINGS which allows access to django.conf.settings values
apply_settings()

#use the default section of fab.cfg
@user_settings()
def prod():
    "Production settings"
    env.hosts = ['root@gardener.se']
    env.path = '%(prod_path)s'
    env.giturl = '%(giturl)s'
    env.site_user = 'neno'
    env.site_group = 'neno'

#use the local section
@user_settings('fab.cfg','local')
def localhost():
    "Local settings"
    env.path = '%(dev_path)s'
    env.giturl = '%(giturl)s'

@user_settings()
def upload():
    put(env.tarball, env.path)

def deploy():
    "Push local changes and update checkout on the remote host"
    push()
    update_remote() # reset and pull on the remote server
    upload()
    #remote_export()
    change_ownership()
    touch_wsgi()

@user_settings()
def pack():
    local("tar -czf %(tarball)s -X .gitignore --exclude '.git*' ." % env, capture=False)

def test():
    print "website using database %s " % (settings.DATABASE_NAME,)

