init:
	pip install pipenv
	pipenv install --dev
	pipenv run pre-commit install
	@echo && echo use "pipenv shell" to access virtual env
