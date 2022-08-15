#!/usr/bin/env bash
PROJECT_ROOT_DIR=$(cd $(dirname $0); cd ..; pwd)
pytest ${PROJECT_ROOT_DIR}/tests -qq -c ${PROJECT_ROOT_DIR}/tests/pytest_main.ini
pytest ${PROJECT_ROOT_DIR}/tests -qq -c ${PROJECT_ROOT_DIR}/tests/pytest_kirkstone.ini
pytest ${PROJECT_ROOT_DIR}/tests -qq -c ${PROJECT_ROOT_DIR}/tests/pytest_dunfell.ini
