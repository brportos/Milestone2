VENV = env
BIN = $(VENV)/bin
PY = $(BIN)/python
ARGS = a_maze_ing.py config.txt

all: run

$(VENV):
	@python3 -m venv $(VENV)
	@$(BIN)/pip install --upgrade pip build flake8 mypy flake8-docstrings ./mlx-2.2-py3-none-any.whl -r requirements.txt

install: $(VENV)

run:
	@$(PY) $(ARGS)

debug:
	@$(PY) -m pdb $(ARGS)

build:
	@$(PY) -m build
	@cp dist/* .
	@rm -rf dist

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