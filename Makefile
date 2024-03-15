format:
	python -m black -S --line-length 79 --preview ./resumeetl
	isort ./

type:
	python -m mypy --no-implicit-reexport --ignore-missing-imports --no-namespace-packages ./resumeetl

lint:
	flake8 ./resumeetl

ci: format type lint

parse:
	python resumeetl/main.py

reset-db:
	python3 resumeetl/schema_manager.py --reset-db