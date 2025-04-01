#!/usr/bin/env bash

export WOLFIT_SETTINGS=$(pwd)/test.settings
export FLASK_ENV=test
export FLASK_DEBUG=0
coverage run --source "app/" --omit "app/commands.py"  -m pytest
coverage html
open htmlcov/index.html

set -e
if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null ; then
        sensible-browser htmlcov/index.html
else
        open htmlcov/index.html
fi
