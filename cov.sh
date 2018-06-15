#!/bin/bash
coverage run --source "." -m py.test
coverage html
open htmlcov/index.html