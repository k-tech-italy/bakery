.PHONY: help demo .build-venv

VERSION=0.1.0
BUILDDIR='.build'
PYTHONPATH:=${PWD}/tests/:${PWD}:${PYTHONPATH}
BUILDDIR?=./.build
CURRENT_BRANCH:=$(shell git rev-parse --abbrev-ref HEAD)
.DEFAULT_GOAL := help

guard-%:
	@if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
        exit 1; \
    fi

EXECUTABLES = pyenv poetry cookiecutter 
REQUIRED_EXECUTABLES := $(foreach exec,$(EXECUTABLES),\
	$(if $(shell which $(exec)),some string,$(error "Couldn't find: `$(exec)` in PATH.")))

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z0-9_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.bake-list:
	@echo "You need to specify one of the following available recipe:"
	@python -c "import os; print('\n'.join([f'PRJ={x} make bake' for x in os.listdir() if os.path.isfile(f'./{x}/cookiecutter.json')]))"

bake: ## Bake the recipe into a cookie! Prefix with PRJ=<name> for baking the project
	@if [ "${PRJ}" = "" ]; then \
		$(MAKE) --no-print-directory .bake-list ; \
	else \
	  	if [ "${VIRTUAL_ENV}" != "" ]; then \
	  	  echo "It appears you are running in virtual env. Please deactivate it or unset VIRTUAL_ENV variable before continuing" ; \
	  	  exit 1; \
	  	fi ; \
		echo "baking ${PRJ} ..." ; \
		mkdir -p ./demo-${PRJ} ; \
		rm -rf ./demo-${PRJ}/* ; \
		echo "${PRJ}" > ./demo-${PRJ}/.cookie ; \
		cd ./demo-${PRJ} && cookiecutter ../${PRJ} ; \
		cd * ; \
		cp .env.example .env ; \
		cp .envrc.example .envrc ; \
		echo "baked ${PRJ} in demo-${PRJ}/" ; \
		$(MAKE) --no-print-directory runonce ; \
	fi

