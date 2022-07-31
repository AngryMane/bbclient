# BBClient
BBClient provides command interface for bitbake server. 

<!--
[![NPM Version][npm-image]][npm-url]
[![Build Status][travis-image]][travis-url]
[![Downloads Stats][npm-downloads]][npm-url]
-->

The typical use case is as follows. You can do it via python easily.  

* Get recipe variable value
* Get layer info
* Get image recipes
* Get all the packages
* Start a task of packages

![](header.png)

## Installation
At this point, please git clone and import this in your python code.  
TODO: Enable to install by pip  

<!--
Linux:

```sh
npm install my-crazy-module --save
```
-->

## Usage example

Typical use case is as follows.   
If you want to know all supported features, see bbclient.py at this point. (I'll make some documents sooner or later)

#### start server
```python
server_port = 8080
client: BBClient = BBClient("/PATH/TO/poky", ". oe-init-build-env")
# address and port. Please note that BBClient supports only localhost at this point.
client.start_server("localhost", 8080) 
```

#### stop server
```python
client.stop_server()
```

#### get global variable
```python
ret: str = client.get_variable("MACHINE")
print(ret)
# qemux86-64
```

#### get recipe varible
```python
data_store_index: int = client.parse_recipe_file("/PATH/TO/busybox_1.35.0.bb")
src_uri: str = client.data_store_connector_cmd(data_store_index, "getVar", "SRC_URI")
print(src_uri)
# https://busybox.net/downloads/busybox-1.35.0.tar.bz2;name=tarball
# file://0001-depmod-Ignore-.debug-directories.patch
# file://busybox-udhcpc-no_deconfig.patch
# file://find-touchscreen.sh
# file://busybox-cron
# ...
```

#### get all inherit files of all recipes
```python
ret: Mapping[str, List] = client.get_recipe_inherits()
print(ret) 
# {
#   '/PATH/TO/RECIPE/build-appliance-image_15.0.0.bb': [
#       '/PATH/TO/RECIPE/base.bbclass',
#       '/PATH/TO/RECIPE/patch.bbclass',
#       '/PATH/TO/RECIPE/staging.bbclass',
#       '/PATH/TO/RECIPE/mirrors.bbclass',
#       '/PATH/TO/RECIPE/utils.bbclass',
#       '/PATH/TO/RECIPE/utility-tasks.bbclass',
#       '/PATH/TO/RECIPE/metadata_scm.bbclass',
#       '/PATH/TO/RECIPE/logging.bbclass',
#   ],
#   '/PATH/TO/RECIPE/xxx.bb': [
#       '/PATH/TO/RECIPE/yyy.bbclass',
#       '/PATH/TO/RECIPE/zzz.bbclass',
#   ],
#   ...
# }
```

#### get append files
```python
ret: List[str] = client.get_file_appends("/PATH/TO/busybox_1.35.0.bb")
print(ret) 
# [
#   '/PATH/TO/APPEND/xxx.bbappend',
#   '/PATH/TO/APPEND/yyy.bbappend',
#   ...
# ]
```

## Development setup

TODO

<!--
Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```
-->
