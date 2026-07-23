.PHONY: clean re all install run lint lint-strict debug help


NAME_VENV = our_a_mazing
HIS_PYTHON3 = $(NAME_VENV)/bin/python3
HIS_MYPY = $(NAME_VENV)/bin/python3 -m mypy
HIS_FLAKE8 = $(NAME_VENV)/bin/python3 -m flake8
THE_FILE = $(NAME_VENV)/.is_install


all: install

$(THE_FILE):
	python3 -m venv $(NAME_VENV)
	@$(NAME_VENV)/bin/pip install -r requirements.txt
	@$(NAME_VENV)/bin/pip install mlx-2.2-py3-none-any.whl
	@$(NAME_VENV)/bin/pip install mazegen-0.1.0-py3-none-any.whl
	@touch $(THE_FILE)

install: $(THE_FILE)

run: $(THE_FILE)
	@$(HIS_PYTHON3) a_maze_ing.py config.txt

lint: $(THE_FILE)
	@$(HIS_FLAKE8) . --exclude our_a_mazing
	@$(HIS_MYPY) .\
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	@$(HIS_FLAKE8) . --exclude our_a_mazing
	@$(HIS_MYPY) . --strict --exclude our_a_mazing

debug: $(THE_FILE)
	echo "let the debugging begin..."
	$(HIS_PYTHON3) -m pdb a_maze_ing.py config.txt

clean:
	@rm -rf maze.txt
	@rm -rf $(NAME_VENV)
	@rm -rf mazegen/generate_maze/__pycache__
	@rm -rf mazegen/generate_maze/.mypy_cache
	@rm -rf mazegen/generate_cellule/__pycache__
	@rm -rf mazegen/generate_cellule/.mypy_cache
	@rm -rf mazegen/solve_the_maze/__pycache__
	@rm -rf mazegen/solve_the_maze/.mypy_cache
	@rm -rf mazegen/__pycache__
	@rm -rf mazegen/.mypy_cache
	@rm -rf mlx/__pycache__
	@rm -rf __pycache__
	@rm -rf .mypy_cache
	@rm -rf mlx-2.2-py3-none-any

help:
	@echo "==== The HELP ==="
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo " all         : Create the virtual environment and install dependencies"
	@echo " run         : Run the maze application"
	@echo " lint        : Run flake8 and mypy"
	@echo " lint-strict : Run flake8 and mypy in strict mode"
	@echo " clean       : Remove temporary build files"
	@echo " fclean      : Remove all generated files"
	@echo " re          : Clean and rebuild"
	@echo " debug       : Run the application with pdb"
	@echo " help        : Display this help"

re: clean all
