SHELL=/bin/bash
.DEFAULT_GOAL := all

.PHONY: install
install:
	python -m pip install --upgrade setuptools pip pip-tools
	python -m piptools sync requirements.txt requirements-dev.txt docs/requirements.txt
	pre-commit install

.PHONY: update
update:
	python -m piptools sync requirements.txt requirements-dev.txt docs/requirements.txt

	pip install --upgrade pip
	pip-compile requirements.in
	pip-compile requirements-dev.in
	pip-compile docs/requirements.in

	python -m piptools sync requirements.txt requirements-dev.txt docs/requirements.txt

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: test
test:
	python -m pytest ${ARGS}

.PHONY: all
all: lint test

.PHONY: clean
clean:
	git clean -Xdf

.PHONY: docs
docs:
	mkdocs serve --config-file docs/mkdocs.yml

.PHONY: build-docs
build-docs:
	mkdocs build --config-file docs/mkdocs.yml

.PHONY: pull
pull:
	git checkout master
	git pull

.PHONY: bump-version
bump-version:
	cz bump --changelog --no-verify
	git push
	git push --tags

.PHONY: bump
bump: pull bump-version clean
