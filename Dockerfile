# SPDX-License-Identifier: GPL-3.0-or-later
# Runs tools/okf_check.py. The sibling fusion-* repos are mounted at /src (read-only),
# this repo at /src/fusion-okf - see Makefile.
FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/* \
 && git config --system --add safe.directory '*'

COPY tools/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /src/fusion-okf
ENTRYPOINT ["python", "-I", "tools/okf_check.py"]
CMD ["check"]
