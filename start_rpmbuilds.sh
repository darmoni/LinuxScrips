#! /bin/bash

export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python;
export WORKON_HOME=$HOME/Envs;
export PROJECT_HOME=$HOME/VirtualProjects;
export VIRTUALENVWRAPPER_LOG_FILE=hook.log;
export VIRTUALENVWRAPPER_SCRIPT=/usr/local/bin/virtualenvwrapper.sh;
source $VIRTUALENVWRAPPER_SCRIPT;

workon rpmbuilds && python manage.py runserver 0.0.0.0:8010 &
