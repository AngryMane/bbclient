# BBClient
BBClient provides command interface for bitbake server. 

<!--
[![NPM Version][npm-image]][npm-url]
[![Build Status][travis-image]][travis-url]
[![Downloads Stats][npm-downloads]][npm-url]
-->

The typical use case is as follows. You can do it via shell or python easily.  

* Get recipe variable value
* Get layer info
* Get image recipes
* Get all the packages
* Start a task of packages

For example, see below.  
*Please note that before using bbclient in shell, you have to initialize env by oe-init-build-env*.  

```bash
# Please note that before using bbclient in shell, you have to initialize env by oe-init-build-env.
$ source oe-init-build-env
$ bbclient find_best_provider gcc
[null, null, null, "/PATH/TO/POKY/meta/recipes-devtools/gcc/gcc_12.1.bb"]
```

You can do the same with python.  

```python
# get recipe file path for specified package
ret: List[str] = client.find_best_provider("gcc")
target_recipe_file_path: str = ret[3]

# parse the recipe file
data_store_index: int = client.parse_recipe_file(target_recipe_file_path)

# get variable in the recipe file
ret: Any = client.data_store_connector_cmd(data_store_index, "getVar", "PN")
```

## System Requirements
* python: 3.9 or later
* yocto: scarthgap or wrynose

bbclient is tested on Ubuntu 22.04 and 24.04 with python 3.9 to 3.14.  
Since wrynose has no poky repository, bbclient uses the bitbake found in `PATH` (set by `oe-init-build-env`) when bitbake isn't in the project path.

## Installation

```
pip3 install bbclient
```

<!--
Linux:

```sh
npm install my-crazy-module --save
```
-->

## Document

> **Note**
> For using with shell, we have not documented yet. Please see `$bbclient --help`. 

* [specification](https://angrymane.github.io/bbclient/bbclient.html)  
* [use case](https://angrymane.github.io/bbclient/usecase.html)  


<!--
Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```
-->
