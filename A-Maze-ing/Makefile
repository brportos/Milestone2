PYTHON = python3.13
VENV = env
PIP = $(VENV)/bin/pip

MAIN = a_maze_ing.py 
CONFIG = config.txt

all: run

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name __pycache__ \
	-exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	find . -name "*.pyc" -delete

lint:
	flake8 .
	mypy \
	--warn-return-any \
	--warn-unused-ignores\
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs .

lint-strict:
	flake8 .
	mypy . --strict

.PHONY:	install run debug clean lint lint-strict