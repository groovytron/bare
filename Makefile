.PHONY:test
test:
	@poetry run python -m unittest discover tests

.PHONY:lint
lint:
	@poetry run black --check . && \
	poetry run flake8 .

.PHONY:format
format:
	@poetry run isort . && \
	poetry run black .
