# Project configuration.
PROJECT_NAME = datasets

# Makefile variables.
SHELL = /bin/bash

# Misc.
TOPDIR = $(shell git rev-parse --show-toplevel)
YAPF_EXCLUDE=*.eggs/*,*.tox/*,*venv/*

default: setup

.PHONY: help
help: # Display help
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
		}' $(MAKEFILE_LIST) | sort

setup: venv ## Setup the full environment (default)

venv: venv/bin/activate ## Setup local venv

venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv
	. venv/bin/activate \
		&& pip install --upgrade pip setuptools \
		&& pip install -r requirements.txt \
		&& pip install -r requirements-dev.txt
