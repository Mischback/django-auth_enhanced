# This Makefile is just for convenience. It offers tab completion for some
# common development tasks.

.SILENT:
.PHONY: benchmark clean coverage doc doc-srv flake8 isort isort-full test


# counts LoCs
benchmark:
	tox -e flake8 -- --benchmark

# deletes temporary files created by running Django
clean:
	- tox -e coverage-report -- coverage erase
	find . -iname "*.pyc" -delete
	find . -iname "__pycache__" -delete
	find . -iname ".coverage.*" -delete
	rm -rf htmlcov
	rm -rf docs/build/

# runs the tests and measures code coverage
coverage: clean test
	tox -e coverage-report

# builds the documentation using 'Sphinx'
doc:
	tox -e doc

# serves the documentation (and automatically builds it!)
doc-srv: doc
	tox -e doc-srv

# runs 'flake8'
flake8:
	tox -e flake8

# runs 'isort' in diff-mode, only showing proposed changes
isort:
	tox -e isort -- --diff

# actually executes 'isort' to re-order the imports
isort-full:
	tox -e isort

# runs the tests in the default environment
test:
	tox -e test
