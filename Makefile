.PHONY: validate setup test

setup:
	python3 -m pip install -r requirements-dev.txt

validate:
	python3 scripts/validate_examples.py


test:
	python3 -m unittest discover -s tests -p "test_*.py"
