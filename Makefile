# Makefile for the chatzecobranca_python project.

# Shell to use
SHELL := /bin/bash

# Directories and files to check
SRC_DIR := src
TESTS_DIR := tests
PY_FILES := $(SRC_DIR) $(TESTS_DIR) app.py

# Use .PHONY for targets that are not files to avoid conflicts with files of the same name
.PHONY: all install format lint test check help

# Default target is 'help'
default: help

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install    Install dependencies using pipenv."
	@echo "  format     Format code with black and isort."
	@echo "  lint       Lint code with flake8 and mypy."
	@echo "  test       Run tests with pytest."
	@echo "  check      Run lint and tests."
	@echo "  all        Run format, lint, and tests."

install:
	@echo "--> Installing dependencies..."
	@pipenv install --dev
	@echo "NOTE: This project uses black, isort, and mypy. If not already installed, run:"
	@echo "pipenv install --dev black isort mypy"

format:
	@echo "--> Formatting code with black and isort..."
	@pipenv run black $(PY_FILES)
	@pipenv run isort $(PY_FILES)

lint:
	@echo "--> Linting code with flake8 and mypy..."
	@pipenv run flake8 $(PY_FILES)
	@pipenv run mypy $(PY_FILES) --ignore-missing-imports

test:
	@echo "--> Running tests with pytest..."
	@pipenv run pytest

check: lint test

all: format check

run:
	@echo "--> Running the Flask application..."
	@pipenv run python app.py