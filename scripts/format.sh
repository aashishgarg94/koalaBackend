#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place koala tests scripts --exclude=__init__.py
black koala tests scripts
isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --recursive --thirdparty koala --thirdparty pydantic --thirdparty starlette --apply koala tests scripts