#!/bin/bash

set -xe

export GIT_ROOT=$(git rev-parse --show-toplevel)

mypy $GIT_ROOT/examples
mypy $GIT_ROOT/src/pygame_zer/*.pyi
mypy $GIT_ROOT/src/pygame_zer/*.py
mypy $GIT_ROOT/tests
pytest
