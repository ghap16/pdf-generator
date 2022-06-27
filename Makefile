files = `find ./src ./tests -name "*.py"`
files_tests = `find  ./tests -name "*.py"`

fmt: ## Format all project files
	## @add-trailing-comma $(files)
	@isort ${files}
	@black ${files}

lint: ## Run flake8 checks on the project.
	@poetry run isort ${files} --check-only
	@poetry run black ${files} --check
	@poetry run flake8 $(files)
	##  @poetry run pylint $(files)

test: ## Run unit testings.
	@pytest

install: ## Install project dependencies.
	@poetry install

venv: ## Create new virtual environment. Run `source venv/bin/activate` after this command to enable it.
	@poetry shell

run: ## Execute local server
	@uvicorn src.main:app