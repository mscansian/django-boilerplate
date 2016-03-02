# Project settings
SHELL := /bin/bash
WD := $(shell pwd)
PROJECT_DIR := $(WD)/src
VENV := $(WD)/venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
DJANGO_ADMIN := $(VENV)/bin/django-admin.py
DJANGO_MANAGE := $(PROJECT_DIR)/manage.py
PROJECT_NAME = `cat $(WD)/etc/project-name`

# make all - Install and test
.PHONY: all
all: install test

# make help - Display callable targets
.PHONY: help
help:
	@echo "Project Name: $(PROJECT_NAME)"
	@egrep "^# make " [Mm]akefile

# make clean - Clean JS, CSS and .pyc
.PHONY: clean
clean: cssclean jsclean
	cd $(PROJECT_DIR); \
	find . -name "*.pyc" -type f -delete; \
	find . -name "*.pyo" -type f -delete; \
	find . -name "*~" -type f -delete;

# make distclean - Delete installation
.PHONY: distclean
distclean: clean
	rm -rf $(WD)/venv/
	rm -rf $(WD)/gunicorn/
	rm -f $(WD)/etc/.apt

# make test - Run django unittest
.PHONY: test
test: install
ifndef APP
	cd $(PROJECT_DIR); \
	$(PY) $(DJANGO_MANAGE) test
else
	cd django; \
	$(PY) $(DJANGO_MANAGE) test $(APP)
endif

# make debug - Run debug server
.PHONY: debug
debug: install
ifndef PORT
	cd $(PROJECT_DIR); \
	$(PY) $(DJANGO_MANAGE) runserver 0.0.0.0:8000
else
	cd $(PROJECT_DIR); \
	$(PY) $(DJANGO_MANAGE) runserver $(PORT)
endif

## INSTALL

# make install - Install requirements and dependencies
.PHONY: install
install: etc/.apt venv

# make force-install - Reset installed status
.PHONY: force-install
force-install:
	touch $(WD)/etc/dependencies.apt
	touch $(WD)/etc/requirements.txt
	@echo "Now run 'make install' to do the actual installation"

etc/.apt: etc/dependencies.apt
	sudo $(WD)/etc/dependencies.apt
	touch $(WD)/etc/.apt

venv: venv/bin/activate
venv/bin/activate: etc/requirements.txt
	test -d venv || virtualenv venv
	$(PIP) install -Ur $(WD)/etc/requirements.txt
	touch $(VENV)/bin/activate

## DJANGO

# make django-migrate [APP] [MMOPTIONS] - Make migrations and migrate database
.PHONY: django-migrate
django-migrate: install
ifndef APP
	cd $(PROJECT_DIR); \
	$(PY) $(DJANGO_MANAGE) makemigrations $(MMOPTIONS); \
	$(PY) $(DJANGO_MANAGE) migrate $(MOPTIONS);
else
	cd $(PROJECT_DIR); \
	$(PY) $(DJANGO_MANAGE) makemigrations $(APP) $(MMOPTIONS); \
	$(PY) $(DJANGO_MANAGE) migrate $(APP) $(MOPTIONS);
endif

# make django-static - Collect static
.PHONY: django-static
django-static: install
	cd $(PROJECT_DIR); \
	$(PY) $(DJANGO_MANAGE) collectstatic --no-input;

# make django-manage COMMAND - Run manage.py command
.PHONY: django-manage
django-manage: install
ifdef COMMAND
	cd $(PROJECT_DIR); \
	$(PY) $(DJANGO_MANAGE) $(COMMAND);
else
	@echo "You need to provide COMMAND variable"
endif

# make django-localization [LOCALE] [OPTIONS] - Make localization messages
.PHONY: django-localization
django-localization:
ifdef LOCALE
	cd $(PROJECT_DIR); \
	$(PY) $(DJANGO_ADMIN) makemessages -e dtl,html --l $(LOCALE) $(OPTIONS)
else
	cd $(PROJECT_DIR); \
	$(PY) $(DJANGO_ADMIN) makemessages -e dtl,html --all $(OPTIONS)
endif

# make django-localization-compile [LOCALE] [OPTIONS] - Compile localization messages
.PHONY: django-localization-compile
django-localization-compile:
ifdef LOCALE
	cd $(PROJECT_DIR); \
	$(PY) $(DJANGO_ADMIN) compilemessages --l $(LOCALE) $(OPTIONS)
else
	cd $(PROJECT_DIR); \
	$(PY) $(DJANGO_ADMIN) compilemessages $(OPTIONS)
endif

## SERVER CONFIGURATION

# make gunicorn - Build gunicorn/supervisor configuration
.PHONY: gunicorn
gunicorn: install
	$(PY) $(WD)/scripts/gunicorn.py $(PROJECT_NAME);

## CSS

# make css - Compile minified less files
.PHONY: css
css:
	$(WD)/scripts/build-css.sh $(PROJECT_DIR)

# make pretty-css - Compile less files
.PHONY: pretty-css
pretty-css:
	$(WD)/scripts/build-css.sh $(PROJECT_DIR) --pretty

# make cssclean - Clean compiled css
.PHONY: cssclean
cssclean:
	$(WD)/scripts/build-css.sh $(PROJECT_DIR) --clean

## JS

# make js - Compile minified JS files
.PHONY: js
js:
	$(WD)/scripts/build-js.sh $(PROJECT_DIR)

# make jsclean - Clean minified JS
.PHONY: jsclean
jsclean:
	$(WD)/scripts/build-js.sh $(PROJECT_DIR) --clean
