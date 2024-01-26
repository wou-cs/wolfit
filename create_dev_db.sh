#!/bin/bash
export FLASK_ENV=development
export FLASK_DEBUG=0
export WOLFIT_SETTINGS=$(pwd)/dev.settings

set -o allexport
source $WOLFIT_SETTINGS
set +o allexport

if [ -f $BLOG_DATABASE_NAME ]; then
   echo "Development DB ($BLOG_DATABASE_NAME) already exists -- delete first if you want to re-create."
else
   flask db upgrade
fi

