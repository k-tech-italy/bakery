VERSION=0.1.0
BUILDDIR='.build'
PYTHONPATH:=${PWD}/tests/:${PWD}:${PYTHONPATH}
BUILDDIR?=./.build
CURRENT_BRANCH:=$(shell git rev-parse --abbrev-ref HEAD)
NODE_ENV?=production
.PHONY: help runonce run i18n
.DEFAULT_GOAL := help

ifeq ($(wildcard .initialized),)
    INITIALIZED = 0
else
    INITIALIZED = 1
endif

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

.mkbuilddir:
	@mkdir -p ${BUILDDIR}


static:  ## build static assets
	@rm -fr src/{{cookiecutter.project__slug}}/web/static/*
	@sass src/{{cookiecutter.project__slug}}/web/assets/tw.in.scss | postcss  --config   -o src/{{cookiecutter.project__slug}}/web/assets/tw.css
	@node_modules/.bin/webpack --mode ${NODE_ENV} --progress  --bail
	@STATIC_ROOT=src/{{cookiecutter.project__slug}}/web/static ./manage.py collectstatic_js_reverse -v 0
	@STATIC_ROOT=src/{{cookiecutter.project__slug}}/web/static ./manage.py collectstatic --no-input -v 0
	@git add src/{{cookiecutter.project__slug}}/web/static
	@echo $(shell /bin/ls -alu src/{{cookiecutter.project__slug}}/web/static/{{cookiecutter.project__slug}}/app.js)
	@echo $(shell /bin/ls -alu src/{{cookiecutter.project__slug}}/web/static/{{cookiecutter.project__slug}}/app.css)

develop:  ## configure development environment
	git config branch.autosetuprebase always
	@poetry install
	poetry run pre-commit install
	poetry run pre-commit install --hook-type pre-push
	npm install


backup_file := ~$(shell date +%Y-%m-%d).json
reset-migrations: ## reset django migrations
	./manage.py check
	find src -name '0*[1,2,3,4,5,6,7,8,9,0]*' | xargs rm -f
	rm -f *.db
	./manage.py makemigrations {{cookiecutter.project__slug}}
	./manage.py makemigrations --check
	@echo "\033[31;1m You almost there:"
	@echo "\033[37;1m  - add 'CITextExtension()' as first operations of src/{{cookiecutter.project__slug}}/migrations/0001_initial.py"
	@echo "\033[37;1m  - run ./manage.py upgrade --no-input"
	@echo "\033[37;1m  - run ./manage.py demo --no-input"


lint:  ## code lint
	pre-commit run --all-files

clean: ## clean development tree
	rm -fr ${BUILDDIR} build dist src/*.egg-info .coverage coverage.xml .eggs .pytest_cache *.egg-info
	find src -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find tests -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find src/_other_/locale -name django.mo | xargs rm -f

fullclean:
	rm -fr .tox .cache .venv node_modules
	$(MAKE) clean

test:
	pytest tests/

i18n:  ## i18n support
	git checkout develop
	git pull
	git checkout weblate
	git pull
	git merge develop -m "Mergin weblate from develop"
	cd src && django-admin makemessages --all --settings={{cookiecutter.project__slug}}.config.settings --pythonpath=../src
	cd src && django-admin compilemessages --settings={{cookiecutter.project__slug}}.config.settings --pythonpath=../src
	git add src/{{cookiecutter.project__slug}}/LOCALE
	git commit -m "Update po"
	git push
	git checkout ${CURRENT_BRANCH}
	git merge weblate -m "Getting updated translations"
	@if [ "${CURRENT_BRANCH}" != "develop" ]; then \
		echo "WARNING: Remember to rebase on develop with 'git rebase develop'" ; \
	fi

bump:   ## Bumps version
	@while :; do \
		read -r -p "bumpversion [major/minor/patch]: " PART; \
		case "$$PART" in \
			major|minor|patch) break ;; \
  		esac \
	done ; \
	bumpversion --no-commit --allow-dirty $$PART
	@grep "^version = " pyproject.toml

.zap:
	@rm -f *.db
	@npm run build
	@./manage.py migrate
	@echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'noreply@k-tech.it', 'admin')" | python manage.py shell

.runonce:
	@direnv allow
	@poetry env use `pyenv which python`
	@poetry install
	$(MAKE) .zap
	@touch .initialized

runonce:  ## Initialize and run Django for the first time.
	@if [ "${INITIALIZED}" = "1" ]; then \
		echo "Already initialized" ; \
	else \
	  echo "Initializing" ; \
	  $(MAKE) .runonce ; \
	  ./manage.py runserver ; \
	fi

run:  ## Run a Django development webserver (assumes that `runonce` was previously run).
	npm run build
	./manage.py runserver
