#!/usr/bin/env python3
""" 
This file provides common definition for ease of using bitbake
"""

from typing import Mapping, Any, List, Optional, Tuple, Iterator, Type
import networkx
from .bbclient import *
from .bbcommon import *


class _FileParams:
    CONF_SUFFIX: str = ".conf"
    BBCLASS_SUFFIX: str = ".bbclass"
    BBCLASS_IMAGE_BASE: str = "core-image.bbclas"
    BBCLASS_POPULATE_SDK: str = "populate_sdk.bbclass"


class _FrequentlyUsedVarNames:
    FILES: str = "FILES"
    LICENSE: str = "LICENSE"
    SRC_URI: str = "SRC_URI"
    SUMMARY: str = "SUMMARY"
    DEPENDS: str = "DEPENDS"
    RDEPENDS: str = "RDEPENDS"
    OVERRIDES: str = "OVERRIDES"
    BBINCLUDED: str = "BBINCLUDED"
    DESCRIPTION: str = "DESCRIPTION"
    PACKAGE_NAME: str = "PN"
    PACKAGE_EPOCH: str = "PE"
    PACKAGE_VERSION: str = "PV"
    PACKAGE_REVISION: str = "PR"
    FLAG_TASK: str = "task"
    FLAG_DEPENDS: str = "depends"
    FLAG_RDEPENDS_PN: str = "rdepends-pn"
    FLAG_TASK_DEPENDS: str = "tdepends"


class BBProject:
    """Helper class to use bitbake project"""

    def __init__(self: "BBProject", client: BBClient) -> None:
        """Initialze

        Args:
            self (BBProject): BBProject instance
            client (BBClient): bbclient instance
        """
        self.client: BBClient = client
        """client (str): bbclient instance"""
        self.packages: List[str] = [
            package.package_name for package in self.client.get_recipe_packages()
        ]
        """packages (List[str]): all package names in the project"""
        self.layers: List[str] = [
            layer.path for layer in self.client.get_layer_priorities()
        ]
        """layers (List[str]): all layer names in the project"""
        self.client.parse_files()  # get_layer_priorities clears caches. So this is work around.
        self.image_packages: List[str] = BBProject.__get_inherit_package_names(
            self.client, _FileParams.BBCLASS_IMAGE_BASE
        )
        """image_packages (List[str]): all image package names in the project"""
        self.toolchain_packages: List[str] = self.__get_inherit_package_names(
            self.client, _FileParams.BBCLASS_POPULATE_SDK
        )
        """toolchain_packages (List[str]): all toolchain package names in the project"""

    @staticmethod
    def __get_inherit_package_names(
        client: BBClient, inherit_class_name: str
    ) -> List[str]:
        """Get all package names that inherits specific bbclass

        Args:
            self (BBProject): BBProject instance
            client (BBClient): bbclient instance
        """
        recipe_info: List[GetRecipeInheritsResult] = client.get_recipe_inherits()
        ret: List[str] = []
        for package in recipe_info:
            iter: Iterator = filter(
                lambda path: inherit_class_name in path, package.inherit_file_paths
            )
            inherite_path: Optional[str] = next(iter, None)
            if not inherite_path:
                continue
            datastore_index: int = client.parse_recipe_file(package.recipe_file_path)
            ret.append(
                client.data_store_connector_cmd(
                    datastore_index,
                    DataStoreFunctions.GET_VAR,
                    _FrequentlyUsedVarNames.PACKAGE_NAME,
                )
            )
        return ret


class BBPackage:
    def __new__(self):
        """__new__

        Note:
            DO NOT USE. Please use from_name method.
        """

        # This is for code snippet
        self.client: BBClient = None
        """BBClient : bbclient instance."""
        self.package_name: str = ""
        """str: the package name."""
        self.datastore_index: int = 0
        """int: The index for datastore in bitbake."""
        self.summary: str = ""
        """str: SUMMARY variable of the package."""
        self.description: str = ""
        """str: DESCRIPTION variable of the package."""
        self.license: str = ""
        """str: LICENSE variable of the package."""
        self.source_uris: List[str] = []
        """List[str]: SRC_URI variable of the package."""
        self.package_epoch: str = ""
        """str: PE variable of the package."""
        self.package_version: str = ""
        """str: PV variable of the package."""
        self.package_revision: str = ""
        """str: PR variable of the package."""
        self.package_depends: List[str] = []
        """List[str]: DEPENDS variable of the package."""
        self.package_runtime_depends: List[str] = []
        """List[str]: RDEPENDS variable of the package."""
        self.install_files: List[str] = []
        """List[str]: FILES variable of the package."""
        self.conf_files: List[str] = []
        """List[str]: .conf files related to the package."""
        self.bbclass_files: List[str] = []
        """List[str]: .bbclass files related to the package."""
        self.recipe_files: List[str] = []
        """List[str]: .bb and other recipe files related to the package."""
        self.all_variable_names: List[str] = []
        """List[str]: all variable names in the recipe for the package."""
        self.tasks: List[str] = []
        """List[str]: all tasks in the recipe for the package."""
        self.package_depends_graph: networkx.DiGraph = None
        """networkx.DiGraph: The package dependency graph. The root node is ${self.package_name}"""
        self.package_runtime_depends_graph: networkx.DiGraph = None
        """networkx.DiGraph: The package runtime dependency graph. The root node is ${self.package_name}"""
        self.task_depends_graph: networkx.DiGraph = None
        """networkx.DiGraph: The task dependency graph. The root node is ${self.package_name}.do_build"""

        raise NotImplementedError(
            "To create BBPackage instance, please use from_name method."
        )

    @classmethod
    def from_name(cls: Type, client: BBClient, name: str) -> "BBPackage":
        """Create BBPackage from package name

        Attributes:
            cls (Type): trigger event type for callback function
            client (BBClient): callback function
            name (str): callback function
        Note:
            BBPackage.from_name(client, "python3")
        """
        instance: BBPackage = cls.__internal_new__()
        instance.client: BBClient = client
        instance.package_name: str = name
        instance.__datastore_index: int = BBPackage.__get_datastore_index(
            instance.client, instance.package_name
        )
        instance.summary: str = instance.get_var(_FrequentlyUsedVarNames.SUMMARY)
        instance.description: str = instance.get_var(
            _FrequentlyUsedVarNames.DESCRIPTION
        )
        instance.license: str = instance.get_var(_FrequentlyUsedVarNames.LICENSE)
        instance.source_uris: List[str] = instance.get_var(
            _FrequentlyUsedVarNames.SRC_URI
        ).split()
        instance.package_epoch: str = instance.get_var(
            _FrequentlyUsedVarNames.PACKAGE_EPOCH
        )
        instance.package_version: str = instance.get_var(
            _FrequentlyUsedVarNames.PACKAGE_VERSION
        )
        instance.package_revision: str = instance.get_var(
            _FrequentlyUsedVarNames.PACKAGE_REVISION
        )
        instance.package_depends: List[str] = instance.get_var(
            _FrequentlyUsedVarNames.DEPENDS
        ).split()
        instance.package_runtime_depends: List[str] = instance.get_var(
            _FrequentlyUsedVarNames.RDEPENDS
        ).split()
        instance.install_files: List[str] = instance.get_var(
            _FrequentlyUsedVarNames.FILES
        ).split()

        various_files: List[str] = instance.get_var(
            _FrequentlyUsedVarNames.BBINCLUDED
        ).split()
        instance.conf_files: List[str] = [
            file
            for file in various_files
            if file.endswith(_FileParams.CONF_SUFFIX) or "/conf/" in file
        ]
        instance.bbclass_files: List[str] = [
            file for file in various_files if file.endswith(_FileParams.BBCLASS_SUFFIX)
        ]
        instance.recipe_files: List[str] = [
            file
            for file in various_files
            if not file.endswith((_FileParams.CONF_SUFFIX, _FileParams.BBCLASS_SUFFIX))
            and not "/conf/" in file
        ]

        instance.all_variable_names: List[str] = list(
            instance.client.data_store_connector_cmd(
                instance.__datastore_index, DataStoreFunctions.KEYS
            )
        )
        instance.tasks: List[str] = [
            var
            for var in instance.all_variable_names
            if instance.get_var_flag(var, _FrequentlyUsedVarNames.FLAG_TASK)
        ]

        (
            depends_graph,
            runtime_depends_graph,
            task_depends_graph,
        ) = BBPackage.__generate_depends_graph(instance.package_name, instance.client)
        instance.package_depends_graph = depends_graph
        instance.package_runtime_depends_graph = runtime_depends_graph
        instance.task_depends_graph = task_depends_graph

        return instance

    def get_var(self: "BBPackage", var_name: str) -> Any:
        """Get variable value

        Attributes:
            self (BBPackage): none
            var_name (str): variable name in the recipe for the package

        Returns:
            Any: variable value

        Note:
            User can get variable name from all_variable_names.
        """
        return self.client.data_store_connector_cmd(
            self.datastore_index, "getVar", var_name
        )

    def get_var_flag(self: "BBPackage", var_name: str, flag: str) -> Any:
        """Get the value of the variable flag

        Args:
            self (BBPackage): BBClient instance
            var_name (str): the target variable name
            flag (str): the target flag name

        Returns:
            Any: the target variable flag value
        """
        return self.client.data_store_connector_cmd(
            self.__datastore_index, DataStoreFunctions.GET_VAR_FLAG, var_name, flag
        )

    def run_task(self: "BBPackage", task_name: str = "build") -> None:
        """Run a task

        Args:
            self (BBPackage): BBClient instance
            task_name (str, optional): the target task name. The default value is 'build'.
        """
        self.client.build_targets([self.package_name], task_name)

    @classmethod
    def __internal_new__(cls: Type) -> "BBPackage":
        """Create uninitialized BBPackage instance.

        Args:
            cls (Type): BBPackage

        Returns:
            BBPackage: uninitialized BBPackage instance
        """
        return super().__new__(cls)

    @staticmethod
    def __get_datastore_index(client: BBClient, name: str) -> Any:
        """Get datastore index fot the package

        Args:
            client (BBClient): BBClient instance
            name (str): the package name

        Returns:
            Any: datastore index
        """
        provider: List[str] = client.find_best_provider(name)
        target_recipe_file_path: str = provider[3]
        global_datastore_index: int = client.parse_recipe_file(target_recipe_file_path)
        global_overrides: str = client.data_store_connector_cmd(
            global_datastore_index,
            DataStoreFunctions.GET_VAR,
            _FrequentlyUsedVarNames.OVERRIDES,
        )

        local_datastore_index: int = client.data_store_connector_cmd(
            global_datastore_index, DataStoreFunctions.CREATE_COPY
        ).dsindex
        client.data_store_connector_cmd(
            global_datastore_index,
            DataStoreFunctions.SET_VAR,
            _FrequentlyUsedVarNames.OVERRIDES,
            global_overrides + ":" + name,
        )  # TODO: if dunfell or older, use "_" instead of ":"
        return local_datastore_index

    @staticmethod
    def __generate_depends_graph(
        package_name: str, client: BBClient
    ) -> Tuple[networkx.DiGraph, networkx.DiGraph, networkx.DiGraph]:
        """Generate dependency graph

        Args:
            package_name (str): the package name
            client (BBClient): BBClient instance

        Returns:
            Tuple[networkx.DiGraph, networkx.DiGraph, networkx.DiGraph]: package dependency, package runtime dependency, task dependency
        """
        depends_tree: Mapping[str, Any] = {}
        runtime_depends_tree: Mapping[str, Any] = {}
        task_depends_tree: Mapping[str, Any] = {}

        def monitor(bbclient_: BBClient, event: DepTreeGeneratedEvent):
            nonlocal depends_tree
            nonlocal runtime_depends_tree
            nonlocal task_depends_tree
            depends_tree = event.depgraph[
                _FrequentlyUsedVarNames.FLAG_DEPENDS
            ]  # This is corresponding to DEPENDS
            runtime_depends_tree = event.depgraph[
                _FrequentlyUsedVarNames.FLAG_RDEPENDS_PN
            ]  # This is maybe corresponding to RDEPENDS, but I'm not sure.
            task_depends_tree = event.depgraph[
                _FrequentlyUsedVarNames.FLAG_TASK_DEPENDS
            ]  # This is task depends.

        callback_index: int = client.register_callback(DepTreeGeneratedEvent, monitor)
        client.generate_dep_tree_event([package_name], "build")
        client.unregister_callback(callback_index)

        depends_tree_graph: networkx.DiGraph = networkx.DiGraph()
        BBPackage.__create_node(depends_tree_graph, depends_tree, package_name, [])
        runtime_depends_tree_root: networkx.DiGraph = networkx.DiGraph()
        BBPackage.__create_node(
            runtime_depends_tree_root, runtime_depends_tree, package_name, []
        )
        task_depends_tree_root: networkx.DiGraph = networkx.DiGraph()
        BBPackage.__create_node(
            task_depends_tree_root, task_depends_tree, package_name + ".do_build", []
        )

        return depends_tree_graph, runtime_depends_tree_root, task_depends_tree_root

    @staticmethod
    def __create_node(
        graph: networkx.DiGraph,
        depends_tree: Mapping[str, List[str]],
        package_name: str,
        cache: List[str],
    ):
        """Create graphc recursively

        Args:
            graph (networkx.DiGraph): dependency graph
            depends_tree (Mapping[str, List[str]]): depends info from bitbake
            package_name (str): the package name
            cache (List[str]): cache to avoid cyclic references
        """
        if package_name in graph or package_name not in depends_tree:
            return
        child_package_names: List[str] = depends_tree[package_name]
        for child_package_name in child_package_names:
            if child_package_name not in cache:
                cache.append(child_package_name)
                BBPackage.__create_node(graph, depends_tree, child_package_name, cache)
                cache.remove(child_package_name)
            graph.add_edge(package_name, child_package_name)
