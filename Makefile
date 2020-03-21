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

# building and running container (if somebody decides to deploy this one)
.PHONY: build
build:
	docker build -t covid-api . && docker run --name covid-api -p 5000:5000 covid-api

.PHONY: clean
clean:
	docker stop covid-api
	docker rm -f covid-api
	docker rmi -f covid-api
