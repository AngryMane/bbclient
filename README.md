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

For example, see below.  

```python
# get recipe file path for specified package
ret: List[str] = client.find_best_provider("gcc")
target_recipe_file_path: str = ret[3]

# parse the recipe file
data_store_index: int = client.parse_recipe_file(target_recipe_file_path)

# get variable in the recipe file
ret: Any = client.data_store_connector_cmd(data_store_index, "getVar", "PN")
```

![](header.png)

## System Requirements
* python: 3.7 or later
* yocto: dunfell or kirkstone 

Please note that this command(and also bitbake) doesn't support dunfell with python3.10.  
This is because `collections.Iterable` has been removed, so dunfell with python3.10 will cause exception.

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

* [specification](https://angrymane.github.io/bbclient/bbclient.html)  
* [use case](https://angrymane.github.io/bbclient/usecase.html)  

## Development setup

TODO

<!--
Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```
-->
