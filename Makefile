# This Makefile is just for convenience. It offers tab completion for some
# common development tasks.

.SILENT:
.PHONY: benchmark clean coverage doc doc-srv flake8 isort isort-full test \
		check createsuperuser django migrate runserver


# counts LoCs
benchmark:
	tox -q -e flake8 -- --benchmark

# deletes temporary files created by running Django
clean:
	- tox -q -e coverage-report -- coverage erase
	find . -iname "*.pyc" -delete
	find . -iname "__pycache__" -delete
	find . -iname ".coverage.*" -delete
	rm -rf htmlcov
	rm -rf docs/build/

# runs the tests and measures code coverage
coverage: clean test
	tox -q -e coverage-report

# builds the documentation using 'Sphinx'
doc:
	tox -q -e doc

# serves the documentation (and automatically builds it!)
doc-srv: doc
	tox -q -e doc-srv

# runs 'flake8'
flake8:
	tox -q -e flake8

# runs 'isort' in diff-mode, only showing proposed changes
isort:
	tox -q -e isort -- --diff

# actually executes 'isort' to re-order the imports
isort-full:
	tox -q -e isort

# runs the tests in the default environment
test_cmd ?= ""
test:
	tox -q -e test -- $(test_cmd)

# runs only tags with a specific tag
test_tag ?= current
test-tag:
	$(MAKE) test test_cmd="-t $(test_tag)"

# runs the tests with timing information
test-time:
	$(MAKE) test test_cmd="--time"

##### wrapper for django-admin commands #####

# runs the check framework
# django-admin.py check
check:
	$(MAKE) django django_cmd="check"

# creates a superuser
# django-admin.py createsuperuser
createsuperuser: migrate
	$(MAKE) django django_cmd="createsuperuser"

# runs commands using the django-admin
django_cmd ?= shell
django:
	tox -q -e django -- $(django_cmd)

# apply the migrations into the default environment
# django-admin.py migrate -v 0
migrate:
	$(MAKE) django django_cmd="migrate -v 0"

# runs the development server
# django-admin.py runserver 0:8080
host_port ?= 0:8080
runserver: migrate
	$(MAKE) django django_cmd="runserver $(host_port)"
