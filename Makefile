install:
	python3.8 -m pip install --upgrade pip
	python3.8 -m pip install pipenv
	pipenv install --dev --skip-lock

lint:
	pipenv run pylint SnowieCaster/

test:
	pipenv run python -m pytest -s --cov SnowieCaster --asyncio-mode=auto --cov-fail-under=100 --cov-report term-missing tests/

build:
	pipenv run python -m build

generate_docs:
	rm -r docs
	pipenv run pdoc --html SnowieCaster
	mv html/SnowieCaster docs/
	rm -r html