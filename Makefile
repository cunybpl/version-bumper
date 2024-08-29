test:
	coverage run --source=version_bumper/ -m pytest -s -v && coverage report -m --fail-under=90
	mypy version_bumper --strict