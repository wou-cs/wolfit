#!/bin/bash
export WOLFIT_SETTINGS=$(pwd)/test.settings
coverage run --source "." -m py.test
coverage html
open htmlcov/index.html
