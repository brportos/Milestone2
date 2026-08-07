SHELL := /bin/bash
PYTHON = python3
VENV = env
BIN = $(VENV)/bin

MAIN = a_maze_ing.py 
CONFIG = config.txt

all: run

install:
	@$(PYTHON) -m venv $(VENV)
	@$(BIN)/pip install --upgrade pip build flake8 mypy
	@$(BIN)/pip install ./mlx-2.2-py3-none-any.whl
	@$(BIN)/pip install -r requirements.txt
	@$(BIN)/pip install flake8-docstrings

run:
	@source $(VENV)/bin/activate && python $(MAIN) $(CONFIG)

debug:
	@source $(VENV)/bin/activate && python -m pdb $(MAIN) $(CONFIG)

build:
	@rm -rf dist/ build/
	@$(BIN)/pip install build
	@$(BIN)/python -m build

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@rm -rf .mypy_cache .pytest_cache dist/ build/ *.egg-info
	@find . -name "*.pyc" -delete
	@rm -f output_maze.txt
	@rm -f poetry.lock 
	@rm -rf $(VENV)

lint:
	@$(BIN)/flake8 . --exclude=env
	@$(BIN)/mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	@$(BIN)/flake8 . --exclude=env
	@$(BIN)/mypy . --strict

.PHONY: all install run debug build clean lint lint-strict