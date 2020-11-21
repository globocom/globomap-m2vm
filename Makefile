.PHONY: help clean pep8 coverage tests run

PROJECT_HOME = "`pwd`"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean:  ## Clear *.pyc and unnecessary files
	@find . -name "*.pyc" -delete
	@find . -name "*.~" -delete
	@find . -name "__pycache__" -delete

coverage:  ## Code coverage report
	@coverage report -m --rcfile=.coveragerc

pycodestyle:  ## Check source-code for PEP8 compliance
	@-pycodestyle $(PROJECT_HOME) --ignore=E501,E126,E127,E128,W605

tests: clean pycodestyle  ## Run pycodestyle and all tests with coverage
	@py.test --cov-config .coveragerc --cov $(PROJECT_HOME) --cov-report term-missing

run:  ## Start a development web server
	@PYTHONPATH=`pwd`:$PYTHONPATH python m2vm/run.py
