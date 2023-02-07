MODULE_NAME := snowiecaster
POETRY := $(shell command -v poetry 2> /dev/null)

.PHONY: help
help:
	@echo "Please use 'make <target>', where <target> is one of"
	@echo ""
	@echo "  install     install packages and prepare environment"
	@echo "  lint        run the code linters"
	@echo "  test        run all the tests"
	@echo "  build       build package"
	@echo "  all         install, lint, and test the project"
	@echo "  clean       remove all temporary files listed in .gitignore"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."
	@echo "Most actions are configured in 'pyproject.toml'."

.PHONY: all
all: install lint test

.PHONY: install
install: pyproject.toml poetry.lock
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) install

.PHONY: lint
lint: install
	$(POETRY) run mypy $(MODULE_NAME)
	$(POETRY) run pylint $(MODULE_NAME)

.PHONY: test
test: install
	$(POETRY) run pytest -s --cov $(MODULE_NAME) --asyncio-mode=auto --cov-fail-under=85 --profile --cov-report term-missing tests/

.PHONY: build
build: install clean
	$(POETRY) build

.PHONY: clean
clean:
	git clean -Xdf
