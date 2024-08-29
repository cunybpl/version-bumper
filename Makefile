test:
	coverage run --source=version_bumper/ -m pytest -s -v && coverage report -m
	mypy version_bumper --strict