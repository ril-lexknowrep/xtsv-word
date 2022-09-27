all: build install test
.PHONY: all

build:
	poetry build
.PHONY: build

install:
	poetry install
.PHONY: install

test:
	poetry run pytest
.PHONY: test

PYPI_USER=gpetho
publish:
	poetry config http-basic.pypi $(PYPI_USER)
	poetry publish
.PHONY: publish
