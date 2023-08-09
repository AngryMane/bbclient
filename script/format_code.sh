#!/usr/bin/env bash
PROJECT_ROOT_DIR=$(cd $(dirname $0); cd ..; pwd)
pushd ${PROJECT_ROOT_DIR}
find ./bbclient* -name "*.py" | xargs black
find ./sample* -name "*.py" | xargs black
popd
