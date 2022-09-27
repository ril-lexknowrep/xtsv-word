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

publish:
	poetry publish
.PHONY: publish