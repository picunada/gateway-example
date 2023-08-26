
OK_MSG = \x1b[32m ✔\x1b[0m
SHELL=bash

default: format lint mypy unittest

test-default: unittest
	@echo -e "All tests complete $(OK_MSG)"

format-default: .venv
	@echo -n -e "==> Checking that code is auto-formatted with black...\n"
	@.venv/bin/black --check --quiet --exclude '(.venv|vendor|test)' .
	@echo -e "$(OK_MSG)"

lint-default: .venv
	@echo -n -e "==> Running flake8...\n"
	@.venv/bin/flake8 --show-source --statistics $(CODE_LOCATIONS) --exclude=.venv,test
	@echo -e "$(OK_MSG)"

mypy-default: .venv
	@echo -n -e "==> Type checking...\n"
	@.venv/bin/mypy --no-error-summary $(CODE_LOCATIONS)
	@echo -e "$(OK_MSG)"

unittest-default: .venv
	@echo -e "==> Running tests..\n"
	@docker compose -f test.yml up -d && PYTHONPATH=. .venv/bin/pytest $(CODE_LOCATIONS) --cov-report term-missing:skip-covered --cov $(CODE_LOCATIONS) --cov-report=xml --no-cov-on-fail --cov-fail-under=$(COVERAGE_LIMIT) -W ignore::DeprecationWarning -vv && docker compose down

.venv: requirements.txt test-requirements.txt
	@echo "==> Creating virtualenv...\n"
	test -d .venv || python3 -m venv .venv
	# build wheels when developing locally
	test -z "$$CI" && .venv/bin/pip install -U pip wheel || true
	.venv/bin/pip install -r test-requirements.txt
	touch .venv

blacken-default: .venv
	.venv/bin/black --exclude='(.venv|vendor|test)' .

clean-default:
	rm -rf .venv

watch-default: .venv
	.venv/bin/watchmedo -c 'clear; make test' --drop $(CODE_LOCATIONS)

%: %-default
	@ true
