"""
    Automatic deployment
"""
from __future__ import with_statement
import os
from fabric.api import run, cd, env
import time
from fabric.operations import sudo


def deploy():
    # download distrib from git
    tmp_dir = "/tmp/"
    dist_url = "https://github.com/jarig/eventlist/archive/trunk.zip"
    with cd(tmp_dir):
        run("wget %s distrib.zip" % dist_url)
        new_rel_folder = "release_%s" % time.time()
        run("unzip -o distrib.zip %s/%s" % (env.release_folder, new_rel_folder))
        stop()
        pass
    pass


def stop():
    # stop running instance
    sudo("httpd stop")
    with cd(env.project_root):
        run("./manage.py stop_solr")
    pass


def start():
    pass


def prepare_node():
    # install all necessary dependencies
    sudo("apt get python-pip")
    sudo("pip install MySQL-Python==1.2.4")
    sudo("pip install South==0.8.1")
    sudo("pip install pil==1.1.7")
    sudo("pip install pysolr==3.1.0")
    #sudo("pip install django-pipeline")
    #sudo("pip install yuglify")
    pass


def staging_env():
    env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'eventlist_key')]
    env.app_root = ""
    env.project_root = "%s/current" % env.app_root
    env.release_folder = "%s/releases" % env.app_root
    env.PRODUCTION = "true"
    return "server.address"


env.roledefs = {
    'staging': [staging_env],
    'production': ['ns1']
}