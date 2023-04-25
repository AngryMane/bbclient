#!/usr/bin/env python3
""" 
This file provides common definition for ease of understanding in/out of commands
"""

import functools
from collections.abc import KeysView
from typing import Mapping, Any, List, Optional, Union, Type, Tuple, Iterator
import networkx 
from .bbclient import *

class BBProject:
    def __init__(self: "BBProject", client: BBClient):
        self.client: BBClient = client
        self.packages: List[str] = [package.package_name for package in self.client.get_recipe_packages()]
        self.layers: List[str] = [layer.path for layer in self.client.get_layer_priorities()]
        self.client.parse_files() # get_layer_priorities clears caches. So this is work around.
        self.image_packages: List[str] = self.__get_inherit_package_names("core-image.bbclass")
        self.toolchain_packages: List[str] = self.__get_inherit_package_names("populate_sdk.bbclass")

    def __get_inherit_package_names(self: "BBProject", inherit_class_name: str):
        recipe_info: List[GetRecipeInheritsResult] = self.client.get_recipe_inherits()
        ret: List[str] = []
        for package in recipe_info:
            iter: Iterator = filter(lambda path: inherit_class_name in path, package.inherit_file_paths)
            inherite_path: Optional[str] = next(iter, None)
            if not inherite_path:
                continue
            datastore_index: int = self.client.parse_recipe_file(package.recipe_file_path)
            ret.append(self.client.data_store_connector_cmd(datastore_index, "getVar", "PN"))
        return ret

class BBPackage:
    def __new__(self):
        # This is for code snippet
        self.client: BBClient = None
        self.package_name: str = ""
        self.datastore_index: int = 0
        self.summary: str = ""
        self.description: str = ""
        self.license: str = ""
        self.source_uris: List[str] = []
        self.package_epoch: str = ""
        self.package_version: str = ""
        self.package_revision: str = ""
        self.package_depends: List[str] = []
        self.package_runtime_depends: List[str] = []
        self.install_files: List[str] = []
        self.conf_files: List[str] = []
        self.bbclass_files: List[str] = []
        self.recipe_files: List[str] = []
        self.all_variable_names: List[str] = []
        self.tasks: List[str] = []
        self.package_depends_graph: networkx.DiGraph = None
        self.package_runtime_depends_graph: networkx.DiGraph = None
        self.task_depends_graph: networkx.DiGraph = None

        raise NotImplementedError('To create BBPackage instance, please use from_name method.')

    @classmethod
    def from_name(cls: Type, client: BBClient, name: str) -> "BBPackage":
        instance: BBPackage = cls.__internal_new__()
        instance.client: BBClient = client
        instance.package_name: str = name
        instance.datastore_index: int = instance.__get_datastore_index(instance.package_name)
        instance.summary: str = instance.get_var("SUMMARY")
        instance.description: str = instance.get_var("DESCRIPTION")
        instance.license: str = instance.get_var("LICENSE")
        instance.source_uris: List[str] = instance.get_var("SRC_URI").split()
        instance.package_epoch: str = instance.get_var("PE")
        instance.package_version: str = instance.get_var("PV")
        instance.package_revision: str = instance.get_var("PR")
        instance.package_depends: List[str] = instance.get_var("DEPENDS").split()
        instance.package_runtime_depends: List[str] = instance.get_var("RDEPENDS").split()
        instance.install_files: List[str] = instance.get_var("FILES").split()

        various_files: List[str] = instance.get_var("BBINCLUDED").split()
        instance.conf_files: List[str] = [file for file in various_files if file.endswith(".conf") or "/conf/" in file]
        instance.bbclass_files: List[str] = [file for file in various_files if file.endswith(".bbclass")]
        instance.recipe_files: List[str] = [file for file in various_files if not file.endswith((".conf", ".bbclass")) and not "/conf/" in file]

        instance.all_variable_names: List[str] = list(instance.client.data_store_connector_cmd(instance.datastore_index, "keys"))
        instance.tasks: List[str] = [var for var in instance.all_variable_names if instance.get_var_flag(var, "task")]
        
        depends_graph, runtime_depends_graph, task_depends_graph = instance.__generate_depends_graph()
        instance.package_depends_graph = depends_graph
        instance.package_runtime_depends_graph = runtime_depends_graph
        instance.task_depends_graph = task_depends_graph  

        return instance

    def get_var(self: "BBPackage", var_name: str) -> Any:
        return self.client.data_store_connector_cmd(self.datastore_index, "getVar", var_name)

    def get_var_flag(self: "BBPackage", var_name: str, flag: str) -> Any:
        return self.client.data_store_connector_cmd(self.datastore_index, "getVarFlag", var_name, flag)

    def run_task(self: "BBPackage", task_name: str = "build") -> None:
        self.client.build_targets([self.package_name], task_name)

    @classmethod
    def __internal_new__(cls: Type) -> "BBPackage":
        return super().__new__(cls)

    def __get_datastore_index(self: "BBPackage", name: str) -> Any:
        provider: List[str] = self.client.find_best_provider(name)
        target_recipe_file_path: str = provider[3]
        global_datastore_index: int = self.client.parse_recipe_file(target_recipe_file_path)
        global_overrides: str = self.client.data_store_connector_cmd(global_datastore_index, "getVar", "OVERRIDES")

        local_datastore_index: int = self.client.data_store_connector_cmd(global_datastore_index, "createCopy").dsindex
        self.client.data_store_connector_cmd(global_datastore_index, "setVar", "OVERRIDES", global_overrides + ":" + name) # TODO: if dunfell or older, use "_" instead of ":"
        return local_datastore_index

    def __generate_depends_graph(self: "BBPackage") -> Tuple[networkx.DiGraph, networkx.DiGraph, networkx.DiGraph]:
        depends_tree: Mapping[str, Any] = {}
        runtime_depends_tree: Mapping[str, Any] = {}
        task_depends_tree: Mapping[str, Any] = {}
        def monitor(bbclient_:BBClient, event: DepTreeGeneratedEvent):
            nonlocal depends_tree 
            nonlocal runtime_depends_tree 
            nonlocal task_depends_tree
            depends_tree = event.depgraph["depends"]                # This is corresponding to DEPENDS 
            runtime_depends_tree = event.depgraph["rdepends-pn"]    # This is maybe corresponding to RDEPENDS, but I'm not sure.
            task_depends_tree = event.depgraph["tdepends"]          # This is task depends.
        callback_index: int = self.client.register_callback(DepTreeGeneratedEvent, monitor)
        self.client.generate_dep_tree_event([self.package_name], "build")
        self.client.unregister_callback(callback_index)

        def __create_node(graph: networkx.DiGraph, depends_tree: Mapping[str, List[str]], package_name: str, cache: List[str]):
            if package_name in graph or package_name not in depends_tree:
                return 
            child_package_names: List[str] = depends_tree[package_name]
            for child_package_name in child_package_names:
                if child_package_name not in cache:
                    cache.append(child_package_name)
                    __create_node(graph, depends_tree, child_package_name, cache)
                    cache.remove(child_package_name)
                graph.add_edge(package_name, child_package_name)

        depends_tree_graph: networkx.DiGraph = networkx.DiGraph()
        __create_node(depends_tree_graph, depends_tree, self.package_name, [])
        runtime_depends_tree_root: networkx.DiGraph = networkx.DiGraph()
        __create_node(runtime_depends_tree_root, runtime_depends_tree, self.package_name, [])
        task_depends_tree_root: networkx.DiGraph = networkx.DiGraph()
        __create_node(task_depends_tree_root, task_depends_tree, self.package_name + ".do_build", [])
        
        return depends_tree_graph,  runtime_depends_tree_root, task_depends_tree_root
