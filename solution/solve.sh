#!/bin/bash
set -euo pipefail

cd /app/pandas/pandas_parent

patch -p1 -f -N -i /solution/folder.patch

pip install -e . --no-build-isolation -q
