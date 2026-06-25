REQUIREMENTS = flake8 mypy Pillow

NAME_VENV = our_a_mazing
HIS_PYTHON = $(NAME_VENV)/bin/python
HIS_MYPY = $(NAME_VENV)/bin/python -m mypy
HIS_FLACK8 = $(NAME_VENV)/bin/python -m flake8

all: install

install:
	python3 -m venv $(NAME_VENV)
	@$(NAME_VENV)/bin/pip install $(REQUIREMENTS)

run:
	@if [ -x our_a_mazing/bin/python ]; then \
		$(HIS_PYTHON) a_maze_ing.py config.txt; \
	else \
		echo "Please launch 'make' on your terminal first"; \
	fi

clean:
	@rm -rf $(NAME_VENV)
	@rm -rf mazegen/generate_maze/__pycache__
	@rm -rf mazegen/generate_cellule/__pycache__
	@rm -rf mazegen/solve_the_maze/__pycache__
	@rm -rf mazegen/__pycache__
	@rm -rf mlx/__pycache__
	@rm -rf __pycache__
	@rm -rf .venv

re: clean all


