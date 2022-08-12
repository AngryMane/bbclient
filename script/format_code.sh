#!/usr/bin/env bash
PROJECT_ROOT_DIR=$(cd $(dirname $0); cd ..; pwd)
pushd PROJECT_ROOT_DIR
find ./* -name *.py | xargs black
popd
