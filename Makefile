# SPDX-License-Identifier: GPL-3.0-or-later
IMG        ?= fusion-okf-check:local
BY         ?= human:chrisfusion
REPOS_ROOT ?= $(abspath ..)
RUN = docker run --rm --user $$(id -u):$$(id -g) \
	-v $(REPOS_ROOT):/src:ro -v $(CURDIR):/src/fusion-okf \
	$(IMG)

.PHONY: image check validate index drift verify venv

image:
	docker build -t $(IMG) .

check: image     ## validate + index up to date + drift (CI entry point)
	$(RUN) check

validate: image
	$(RUN) validate

index: image     ## regenerate all index.md files
	$(RUN) index

drift: image     ## concepts whose repo:// sources changed after generated.at
	$(RUN) drift

verify: image    ## mark reviewed pages: make verify PAGES="platform/overview.md ..." [BY=human:<id>]
	$(RUN) verify $(PAGES) --by $(BY)

venv:            ## optional local run without Docker: .venv/bin/python tools/okf_check.py check
	python3.12 -m venv .venv && .venv/bin/pip install -r tools/requirements.txt
