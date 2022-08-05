#!/usr/bin/env bash
PROJECT_NAME=bbclient_doc
PROJECT_DIR=$(pwd)/${PROJECT_NAME}
TARGET_MODULE=$(pwd)/bbclient
VERSION=v0.0.1
OUTPUT_DIR=$(pwd)/../docs
MY_THEME_FILE=$(pwd)/my_theme.css

#if [ -d ${PROJECT_DIR} ];then
  # rm -rf ${PROJECT_DIR}
#fi

#if [ -d ${OUTPUT_DIR} ];then
  # rm -rf ${OUTPUT_DIR}
#fi

sphinx-apidoc -F -H ${PROJECT_NAME} -V ${VERSION} -o ${PROJECT_DIR} ${TARGET_MODULE}

mkdir -p ${PROJECT_DIR}/_static/css
cp ${MY_THEME_FILE} ${PROJECT_DIR}/_static/css

#sed -i "1isys.path.insert(0, '$(pwd)')" ${PROJECT_DIR}/conf.py
#sed -i '1iimport sys' ${PROJECT_DIR}/conf.py
#sed -i '1iimport os' ${PROJECT_DIR}/conf.py
#sed -i "26i\ \ \ \ 'sphinx.ext.napoleon'," ${PROJECT_DIR}/conf.py
#sed -i "26i\ \ \ \ 'sphinx_rtd_theme'," ${PROJECT_DIR}/conf.py
#sed -i "s/alabaster/sphinx_rtd_theme/g" ${PROJECT_DIR}/conf.py
#sed -i "40ihtml_style = 'css/my_theme.css'" ${PROJECT_DIR}/conf.py

sphinx-build ${PROJECT_DIR} ${OUTPUT_DIR}

#if [ -d ${PROJECT_DIR} ];then
  #rm -rf ${PROJECT_DIR}
#fi
