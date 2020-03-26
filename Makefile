#
# Makefile for coronavirus-tracker-api
# ~~~~~~~~~~~~~~~~~~~~~
#
# Combines scripts for common tasks.
#

PYTHON ?= python3

PHONY: all check test

all: test pylint

APP = app
TEST = tests

test:
	$(PYTHON) `which py.test` -s -v $(TEST)

lint:
	pylint $(APP) || true

fmt:
	isort --apply --atomic
	black . -l 120

check-fmt:
	isort -rc --check
	black . --check --diff
