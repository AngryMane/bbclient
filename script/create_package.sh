#!/usr/bin/env bash
PROJECT_ROOT_DIR=$(cd $(dirname $0); cd ..; pwd)
pushd ${PROJECT_ROOT_DIR}

if [ -d build ]; then
    rm -rf build
fi

if [ -d dist ]; then
    rm -rf dist
fi

if [ -d bbclient.egg-info ]; then
    rm -rf bbclient.egg-info
fi

python3 setup.py sdist
python3 setup.py bdist_wheel

echo "
When uploading to testpypi: twine upload --repository testpypi dist/*
When uploading to pypi:     twine upload --repository pypi dist/*
"

popd