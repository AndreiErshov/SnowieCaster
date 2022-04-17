install:
	python3.8 -m pip install --upgrade pip
	python3.8 -m pip install pipenv
	pipenv install --dev --skip-lock

lint:
	pipenv run pylint SnowieCaster/

test:
	pipenv run python -m pytest --cov SnowieCaster --asyncio-mode=auto --cov-fail-under=100 --cov-report term-missing tests/

build:
	pipenv run python -m build