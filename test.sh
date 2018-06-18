#!/bin/bash
export WOLFIT_SETTINGS=$(pwd)/test.settings
pytest $@
