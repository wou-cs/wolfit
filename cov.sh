#!/bin/bash
export WOLFIT_SETTINGS=/Users/chris/Dropbox/Briefcase/dev/cs-407/wolfit/test.settings
coverage run --source "." -m py.test
coverage html
open htmlcov/index.html
