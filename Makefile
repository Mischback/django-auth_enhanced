# This Makefile is just for convenience. It offers tab completion for some
# common development tasks.

.SILENT:
.PHONY: benchmark clean coverage doc doc-srv flake8 isort isort-full test \
		django migrate runserver


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

# runs only tags with a specific tag
test_tag ?= current
test-tag:
	tox -e test -- -t $(test_tag)

# runs the tests with timing information
test-time:
	tox -e test -- --time

##### wrapper for django-admin commands #####

# creates a superuser
# django-admin.py createsuperuser
createsuperuser: migrate
	$(MAKE) django django_cmd="createsuperuser"

# runs commands using the django-admin
django_cmd ?= version
django:
	tox -e django -- $(django_cmd)

# apply the migrations into the default environment
# django-admin.py migrate -v 0
migrate:
	$(MAKE) django django_cmd="migrate -v 0"

# runs the development server
# django-admin.py runserver 0:8080
host_port ?= 0:8080
runserver: migrate
	$(MAKE) django django_cmd="runserver $(host_port)"
