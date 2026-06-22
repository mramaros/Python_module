NAME = a_maze_ing
REQUIREMENTS = mypy pytest pytest-cov

all: run

$(NAME):
	python3 a_maze_ing.py config.txt

install:
	python3 -m venv venv
	#venv/bin/pip install $(REQUIREMENTS)

run: install
	python3 a_maze_ing.py config.txt

clean:
	rm -rf venv
	rm -rf mazegen/generate_maze/__pycache__
	rm -rf mazegen/generate_cellule/__pycache__
	rm -rf mazegen/__pycache__
	rm -rf mlx/__pycache__

re: clean all