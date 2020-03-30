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
	pytest -v $(TEST)  --cov-report term --cov-report xml --cov=$(APP)
lint:
	pylint $(APP) || true

fmt:
	invoke fmt

check-fmt:
	invoke check --fmt --sort
