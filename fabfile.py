# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import sys
import pdb
import collections

from fabric.colors import green, cyan, white, red, magenta, yellow
from fabric.api import *
from fabric.contrib import django

django.settings_module('db.settings')

# define a fabric environment variables
env.use_ssh_config = True
env.shell = "/bin/bash -l -i -c"
env.pwd="trading_system"
env.host_string="trading"
env.repo_url="git@github.com:peekwez/trading_system.git"
env.branch="develop"


def git_clone():
    run("git clone {.repo_url}".format(env))

def git_pull():
    run("git pull origin {.branch}".format(env))

def git_push():
    local("git push origin {.branch}".format(env))

def make(target,option=''):
    run("make {0:s} {1:s}".format(target, option))


@task
def deploy(restart_servers=False):
    with settings(warn_only=True):
        git_push()
        if run("cd ~/{.pwd}".format(env)).failed:
            git_clone()
        else:
            with cd("~/{.pwd}/".format(env)):
                git_pull()

        # if restart is True, restart supervisor tasks
        if restart_servers:
            with cd("~/{.pwd}/".format(env)):
                make("stopall")
                make("processes")
