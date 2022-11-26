#!/usr/bin/env python3
""" 
This file provides client class for bitbake server.
"""

__author__ = "AngryMane"
__authors__ = ["AngryMane"]
__contact__ = "regulationdango@gmail.com"
__copyright__ = "Copyright 2022"
__credits__ = ["AngryMane"]
__date__ = "2022/07/31"
__deprecated__ = False
__email__ = "regulationdango@gmail.com"
__license__ = "MIT"
__maintainer__ = "AngryMane"
__status__ = "in progress"
__version__ = "0.0.1"

import os
import sys
import time
import subprocess
from logging import Logger
from functools import wraps
from typing import Any, List, Optional, Tuple, Mapping, Callable, Iterable, Type

from .bbcommon import *
from .bbevent import *


class BBClient:
    """Client for bitbake RPC Server

    Attributes:
        project_path (str): poky directory path
        __is_server_running (bool): server is running or not
        __server_connection (bb.server.xmlrpcclient.BitBakeXMLRPCServerConnection): touch point to server
        __logger (Optional[Logger]): Logger instance for debugging. Default is None.
    """

    def logger_decorator(func: Callable): # type: ignore
        """Decorator for logging

        Args:
            func (Callable): target function

        Note:
            This is just for debuggging.
        """
        @wraps(func)
        def inner_function(self: "BBClient", *args, **kwargs):
            if self.__logger:
                self.__logger.debug(f"{func.__name__} start.")
            ret = func(self, *args, **kwargs)
            if self.__logger:
                self.__logger.debug(f"{func.__name__} end.")
            return ret
        return inner_function

    # --- setup functions ---
    def __init__(
        self: "BBClient", project_abs_path: str, init_script_path: str = ":", logger: Optional[Logger] = None
    ) -> None:
        """Initialize BBClient instance

        Args:
            self (BBClient): none
            project_abs_path (str): abslute path to bitbake project, basically poky dir.
            init_script_path (str): initialize bitbake proejct command running at project_abs_path. This is maybe ". oe-init-build-env". if you already executed initialize command, you don't need to input this.
            logger (Logger): logger instance for debuggind. Default is None.
        """
        self.project_path: str = project_abs_path
        self.__is_server_running: bool = False
        self.__logger: Optional[Logger] = logger
        pipe: subprocess.Popen = subprocess.Popen(
            f"{init_script_path} > /dev/null; env",
            stdout=subprocess.PIPE,
            shell=True,
            cwd=self.project_path,
            executable="/bin/bash",
            text=True,
        )
        output, _ = pipe.communicate()
        env = dict((line.split("=", 1) for line in output.splitlines()))
        os.environ.update(env)

    def __del__(self: "BBClient") -> None:
        """Finalize BBClient instance

        Args:
            self (BBClient): none
        """
        self.stop_server()

    @logger_decorator
    def start_server(self: "BBClient", server_adder: str, server_port: int) -> None:
        """Start bitbake XML RPC server

        Args:
            self (BBClient): none
            server_adder (str): server address you want to use.
            server_port (int): server port you want to use.

        Note:
            At this point, BBClient doesn't support remote host(=you can only use localhost).
        """
        server_adder_with_port: str = server_adder + ":" + str(server_port)

        pipe: subprocess.Popen = subprocess.Popen(
            f"bitbake --server-only --bind {server_adder_with_port}",
            stdout=subprocess.PIPE,
            shell=True,
            cwd=self.project_path,
            executable="/bin/bash",
            text=True,
        )
        output, _ = pipe.communicate()
        connection, _ = self.__connect_server(
            server_adder_with_port, self.project_path
        )
        self.__server_connection = connection
        self.__is_server_running = True

    @logger_decorator
    def stop_server(self: "BBClient") -> None:
        """Stop bitbake XML RPC server

        Args:
            self (BBClient): none
        """
        if not self.__is_server_running:
            return
        self.state_shutdown()
        time.sleep(1)
        self.state_force_shutdown()
        time.sleep(2)
        self.__server_connection.connection.terminateServer()
        self.__server_connection.terminate()
        self.__is_server_running = False

    # --- utility functions ---
    @logger_decorator
    def wait_done_async(self: "BBClient", timeout: Optional[float] = None) -> Optional[BBEventBase]:
        """Wait CommandCompletedEvent, CommandExitEvent, CommandFailedEvent event

        Args:
            self (BBClient): none
            timeout (Optional[float], optional): timeout. (seconds)

        Returns:
            Optional[BBEventBase]: target event or None
        """
        return self.wait_event([CommandCompletedEvent, CommandExitEvent, CommandFailedEvent], timeout) # type: ignore

    @logger_decorator
    def wait_event(self: "BBClient", event_types: List[Type[BBEventBase]], timeout: Optional[float] = None) -> Optional[BBEventBase]:
        """Wait specific event

        Args:
            self (BBClient): none
            event_types (List[Type[BBEventBase]]): event types you wait for. BBEventBase and its inherits types is defined in bbcommon.py.
            timeout (float): timeout. (seconds)

        Returns:
            Optional[BBEventBase]: The event you wait for or None
        
        Note:
            | This function will pop events from event queue. This event queue is reused between many commands, so this queue may have events from previous commands.
            | When you wait bb.command.CommandCompleted event, please confirm there is no left bb.command.CommandCompleted event from previous command.
        """
        # f"<class '{event_name}'>" -> event_name
        start_time: float = time.perf_counter()
        ret: Optional[BBEventBase] = None
        while True:
            cur_event: Optional[BBEventBase] = self.get_event(0.01)
            find_matched_type: Optional[Type[BBEventBase]] = next(filter(lambda x: isinstance(cur_event, x), event_types), None) # type: ignore
            is_instance_of_target: bool = True if find_matched_type else False
            if is_instance_of_target:
                ret = cur_event
                break
            execution_time: float = time.perf_counter() - start_time
            if timeout and timeout < execution_time:
                if self.__logger:
                    self.__logger.warning(f"Timeout occurred because {execution_time} second has elapsed")
                break
        return ret

    def get_event(self: "BBClient", timeout: Optional[float] = None) -> Optional[BBEventBase]:
        """Get oldest event

        Args:
            self (BBClient): none
            timeout (Optional[float]): timeout. if timeout, return None

        Returns:
            Optional[BBEventBase]: event notification objects. See bbcommon.py
        """
        cur_event: Any = self.__server_connection.events.waitEvent(timeout)
        if not cur_event:
            return None
        cur_event_name: str = str(type(cur_event))[8:-2]
        itr: Iterable = filter(lambda x: x.is_target(cur_event_name), ALL_BB_EVENTS)
        event_class: Optional[Type[BBEventBase]] = next(itr, None) # type: ignore
        ret: BBEventBase = event_class(cur_event.__dict__) if event_class else UnknownEvent(cur_event_name, cur_event.__dict__)
        if not isinstance(ret, UnknownEvent) and self.__logger:
            self.__logger.debug(f"get {cur_event_name}: {ret.__dict__}")
        if isinstance(ret, UnknownEvent) and self.__logger:
            self.__logger.debug(f"get Unknow event {cur_event_name}: {ret.__dict__}")
        return ret
        

    # --- bitbake server sync functions  ---
    @logger_decorator
    def state_shutdown(self: "BBClient") -> None:
        """Terminate tasks

        Args:
            self (BBClient): none

        Note:
            Terminate tasks defined in recipes. If there are running tasks, wait for them to exit.
        """
        self.__run_command(self.__server_connection, "stateShutdown", logger=self.__logger)

    @logger_decorator
    def state_force_shutdown(self: "BBClient") -> None:
        """Terminate tasks

        Args:
            self (BBClient): none

        Note:
            Terminate tasks defined in recipes. If there are running tasks, terminate them.
        """
        self.__run_command(self.__server_connection, "stateForceShutdown", logger=self.__logger)

    @logger_decorator
    def get_all_keys_with_flags(
        self: "BBClient", flag_list: List[str]
    ) -> List[getAllKeysWithFlagsResult]:
        """Get value, history and specified flags of all global variables.

        Args:
            self (BBClient): none
            flag_list(List[str]): Target flags. If flags are unnecessary, please set [].

        Returns:
            List[getAllKeysWithFlagsResult]: See getAllKeysWithFlagsResult.

        Note:
            If you want to get variables defined at any recipes, please use `parse_recipe_file` and `data_store_connector_cmd`.
        """
        ret: Mapping = self.__run_command(  # type: ignore
            self.__server_connection, "getAllKeysWithFlags", flag_list, logger=self.__logger
        )
        return [getAllKeysWithFlagsResult(key, value) for key, value in ret.items()]

    @logger_decorator
    def get_variable(self: "BBClient", name: str, expand: bool = True) -> str:
        """Get variable value

        Args:
            self (BBClient): none
            name (str): variable name
            expand (bool, optional): Whether to expand references to other variables. Defaults to True.

        Returns:
            str: variable value
        """
        expand_str: str = "True" if expand else "False" # bitbake decide whether or not to expand variable by expand == "True" 
        return self.__run_command(self.__server_connection, "getVariable", name, expand_str, logger=self.__logger)  # type: ignore

    @logger_decorator
    def set_variable(self: "BBClient", name: str, value: str) -> None:
        """Set vaiable value

        Args:
            self (BBClient): none
            name (str): variable name
            value (str): variable value you want to set

        """
        self.__run_command(self.__server_connection, "setVariable", name, value, logger=self.__logger)

    @logger_decorator
    def get_set_variable(self: "BBClient", name: str, expand: bool = True) -> str:
        """Get variable from cache and set it into cache

        Args:
            self (BBClient): none
            name (str): variable name
            expand (bool, optional): Whether to expand references to other variables. Defaults to True.

        Returns:
            str: variable value

        Note:
            This is maybe for expand variable value in cache.
        """
        expand_str: str = "True" if expand else "False" # bitbake decide whether or not to expand variable by expand == "True" 
        return self.__run_command(  # type: ignore
            self.__server_connection, "getSetVariable", name, expand_str, logger=self.__logger
        )

    @logger_decorator
    def set_config(self: "BBClient", name: str, value: str) -> None:
        """Set CookerConfigcation properties

        Args:
            self (BBClient): none
            name (str): property name
            value (str): property value

        Note:
            | If you want to know all CookerConfigcation properties, see poky/bitbake/lib/bb/cookerdata.py. But I don't know the detail and how to use it...
        """
        self.__run_command(self.__server_connection, "setConfig", name, value, logger=self.__logger)

    @logger_decorator
    def enable_data_tracking(self: "BBClient") -> None:
        """Enable data tracking

        Args:
            self (BBClient): none

        Note:
            | If enable, cooker cacheata(VariableHistory class) logs the history of changin value. You can see the log by dataStoreConnectorVarHistCmdEmit command.
        """
        self.__run_command(self.__server_connection, "enableDataTracking", logger=self.__logger)

    @logger_decorator
    def disable_data_tracking(self: "BBClient") -> None:
        """Disable data tracking

        Args:
            self (BBClient): none

        Note:
            Please see enable_data_tracking command
        """
        self.__run_command(self.__server_connection, "disableDataTracking", logger=self.__logger)

    @logger_decorator
    def set_pre_post_conf_files(
        self: "BBClient", pre_files: str, post_files: str
    ) -> None:
        """Set pre-load files and post-load files of bitbake.conf at parse_configuration_files command

        Args:
            self (BBClient): none
            pre_files (str): files loaded before bitbake.conf
            post_files (str): files loaded after bitbake.conf

        Note:
            When parse_configuration_files command, pre_files will load before bitbake.conf and post_files will load after bitbake.conf.
        """
        self.__run_command(
            self.__server_connection, "setPrePostConfFiles", pre_files, post_files, logger=self.__logger
        )

    @logger_decorator
    def match_file(
        self: "BBClient", file_path_regex: str, mutli_conf_name: str = ""
    ) -> str:
        """Search file by regex

        Args:
            self (BBClient): none
            file_path_regex (str): search regex pattern
            mutli_conf_name (str): target multi-config. Defaults to ''.

        Returns:
            str: matched file path

        WARNING:
            This command will fail because the second parameter and the first one mixed up in the command.

        Note:
            | This command can extract only one file. If you input the regex matching to many file, this command will fail. 
        """

        return self.__run_command(  # type: ignore
            self.__server_connection, "matchFile", file_path_regex, mutli_conf_name, logger=self.__logger
        )

    @logger_decorator
    def get_uihandler_num(self: "BBClient") -> int:
        """Get ui handler num.

        Args:
            self (BBClient): none

        Returns:
            int: ui hanlder num
        """
        return self.__run_command(self.__server_connection, "getUIHandlerNum", logger=self.__logger)  # type: ignore

    @logger_decorator
    def set_event_mask(
        self: "BBClient",
        handler_num: int,
        log_level: int,
        debug_domains: Mapping[str, int],
        mask: List[str],
    ) -> bool:
        """Set log filter for specified ui handler

        Args:
            self (BBClient): none
            handler_num (int): target ui handler
            log_level (int): logging.DEBUG, logging.INFO, etc...
            debug_domains (Mapping[str, int]): logger name.
            mask (List[str]): target event name. If you don't want to filter by event name, put [ "*" ].

        Returns:
            bool: if handler_num is invalid, return False, otherwise True.

        Note:
            | debug_domains is a little bit complex. If you want to extract logging.getLogger("NAME"), put { "NAME": logging.INFO }. 
            | debug_domains value filters log level like log_level arg. log_level arg and debug_domains value are `or conditoin`.
            |
            | mask is also a little bit difficult. This args filters log by event class name like bb.event.BuildStarted, bb.command.CommandCompleted, etc..
            | It is unclear what type of logs are available.
        """
        # TODO: investigate how to use
        # log level : logging.DEBUG, logging.INFO, etc...
        return self.__run_command(  # type: ignore
            self.__server_connection,
            "setEventMask",
            handler_num,
            log_level,
            debug_domains,
            mask, 
            logger=self.__logger
        )

    @logger_decorator
    def set_features(self: "BBClient", features: List[BBFeature]) -> None:
        """Set feature(Enable feature)

        Args:
            self (BBClient): none
            features (List[BBFeature]): list of HOB_EXTRA_CACHES, BASEDATASTORE_TRACKING and SEND_SANITYEVENTS.

        Note:
            | if enable HOB_EXTRA_CACHES, recipecheces has extra-info like SUMMARY, LICENSE, DESCRIPTION, etc...
            | if enable BASEDATASTORE_TRACKING, enable_data_tracking. See enable_data_tracking command.
            | if enable SEND_SANITYEVENTS, this feature has not been implemented and is currently meaningless.
        """
        self.__run_command(
            self.__server_connection,
            "setFeatures",
            [feature.value for feature in features],
            logger=self.__logger
        )

    @logger_decorator
    def update_config(
        self: "BBClient",
        options: Mapping[str, Any],
        environment: Mapping[str, str],
        command_line: str,
    ) -> None:
        """Update config

        Args:
            self (BBClient): none
            options (Mapping[str, Any]): dict of prefile and postfile
            environment (Mapping[str, str]): environment variables
            command_line (str): will set to BB_CMDLINE

        Note:
            | options will set like {"prefile": ["FILE_NAME", "FILE_NAME"], "postfile": ["FILE_NAME", "FILE_NAME"]}
            | They are prefiles and postfiles settings. See set_pre_post_conf_files command. if you change prefiles or postfiles, bitbake will reset their cache.
            | environment is environment variables, like {"KEY": "VALUE", "KEY": "VALUE"}. if you add/change/delete any environemt variable, bitbake will reset their cache.
            | command_line will set to BB_CMDLINE variable. BB_CMDLINE seems not to be used at all.
        """
        self.__run_command(
            self.__server_connection, "updateConfig", options, environment, command_line, logger=self.__logger
        )

    @logger_decorator
    def parse_configuration(self: "BBClient") -> None:
        """Parse configuration

        Note:
            This command clears caches and re-builds them.
        """
        self.__run_command(self.__server_connection, "parseConfiguration", logger=self.__logger)

    @logger_decorator
    def get_layer_priorities(self: "BBClient") -> List[GetLayerPrioritiesResult]:
        """Get name, path, priority of all layers

        Args:
            self (BBClient): none

        Returns:
            List[GetLayerPrioritiesResult]: See GetLayerPrioritiesResult.

        WARNING:
            This command deletes caches(bug?).
        """
        ret: List[List[Any]] = self.__run_command(self.__server_connection, "getLayerPriorities", logger=self.__logger)  # type: ignore
        return [GetLayerPrioritiesResult(layer) for layer in ret]

    @logger_decorator
    def get_recipes(self: "BBClient", multi_config: str = "") -> List[GetRecipesResult]:
        """Get all package name from cache

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetRecipesResult]: See GetRecipesResult.
        """
        ret: List[List[Any]] = self.__run_command(self.__server_connection, "getRecipes", multi_config, logger=self.__logger)  # type: ignore
        return [GetRecipesResult(recipe) for recipe in ret]

    @logger_decorator
    def get_recipe_depends(
        self: "BBClient", multi_config: str = ""
    ) -> List[GetRecipeDependsResult]:
        """Get recipe depends

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetRecipeDependsResult]: See GetRecipeDependsResult.
        """
        ret: List[List[Any]] = self.__run_command(  # type: ignore
            self.__server_connection, "getRecipeDepends", multi_config, logger=self.__logger
        )
        return [GetRecipeDependsResult(recipe_file) for recipe_file in ret]

    @logger_decorator
    def get_recipe_versions(
        self: "BBClient", multi_config: str = ""
    ) -> List[GetRecipeVersionsResult]:
        """Get all recipe versions

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetRecipeVersions]: See GetRecipeVersions.
        """
        ret: Mapping[str, List[str]] = self.__run_command(  # type: ignore
            self.__server_connection, "getRecipeVersions", multi_config, logger=self.__logger
        )
        return [GetRecipeVersionsResult(value, key) for key, value in ret.items()]

    @logger_decorator
    def get_recipe_provides(
        self: "BBClient", multi_config: str = ""
    ) -> List[GetRecipeProvidesResult]:
        """Get all recipe files and its packages

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetRecipeProvidesResult]: See GetRecipeProvidesResult
        """
        ret: Mapping[str, List[str]] = self.__run_command(  # type: ignore
            self.__server_connection, "getRecipeProvides", multi_config, logger=self.__logger
        )
        return [GetRecipeProvidesResult(key, value) for key, value in ret.items()]

    @logger_decorator
    def get_recipe_packages(
        self: "BBClient", multi_config: str = ""
    ) -> List[GetRecipePackagesResult]:
        """Get all recipe files and its recipe files

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetRecipePackagesResult]: See GetRecipePackagesResult.

        WARNING:
            | This command doesn't work beacuase of bitbake bug. bitbake XML RPC server try to return collections.defaultdict type, but XMLRPC server can't support this type.
        """
        ret: Mapping[str, List[str]] = self.__run_command(  # type: ignore
            self.__server_connection, "getRecipePackages", multi_config, logger=self.__logger
        )
        return [GetRecipePackagesResult(key, value) for key, value in ret.items()]

    @logger_decorator
    def get_recipe_packages_dynamic(
        self: "BBClient", multi_config: str = ""
    ) -> List[GetRecipePackagesDynamicResult]:
        """Get all recipe files that provides PACKAGE_DYNAMIC and its PACKAGE_DYNAMIC

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetRecipePackagesDynamicResult]: See GetRecipePackagesDynamicResult

        WARNING:
            | This command doesn't work beacuase of bitbake bug. bitbake XML RPC server try to return collections.defaultdict type, but XMLRPC server can't support this type.
        """
        ret: Mapping[str, List[str]] = self.__run_command(  # type: ignore
            self.__server_connection, "getRecipePackagesDynamic", multi_config, logger=self.__logger
        )
        return [
            GetRecipePackagesDynamicResult(key, value) for key, value in ret.items()
        ]

    @logger_decorator
    def get_r_providers(
        self: "BBClient", multi_config: str = ""
    ) -> List[GetRProvidersResult]:
        """Get alias of PN and its recipe files

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetRProvidersResult]: See GetRProvidersResult

        WARNING:
            | This command doesn't work beacuase of bitbake bug. bitbake XML RPC server try to return collections.defaultdict type, but XMLRPC server can't support this type.

        Note:
            | If you want to know the detail of alias of PN, See `here <https://docs.yoctoproject.org/ref-manual/variables.html?highlight=rprovide#term-RPROVIDES>`_
        """
        ret: Mapping[str, List[str]] = self.__run_command(  # type: ignore
            self.__server_connection, "getRProviders", multi_config, logger=self.__logger
        )
        return [GetRProvidersResult(key, value) for key, value in ret.items()]

    @logger_decorator
    def get_runtime_depends(
        self: "BBClient", multi_config: str = ""
    ) -> List[GetRuntimeDependsResult]:
        """Get all runtime dependency by all recipe files

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetRuntimeDependsResult]: See GetRuntimeDependsResult
        """
        ret: List[str, Mapping[str, List[str]]] = self.__run_command(  # type: ignore
            self.__server_connection, "getRuntimeDepends", multi_config, logger=self.__logger
        )
        return [GetRuntimeDependsResult(*data) for data in ret]

    @logger_decorator
    def get_runtime_recommends(
        self: "BBClient", multi_config: str = ""
    ) -> List[GetRuntimeRecommendsResult]:
        """Get all runtime recoomends(=weak depends) by all recipe files

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetRuntimeRecommendsResult]: See GetRuntimeRecommendsResult
        """
        ret: List[str, Mapping[str, List[str]]] = self.__run_command(  # type: ignore
            self.__server_connection, "getRuntimeRecommends", multi_config, logger=self.__logger
        )
        return [GetRuntimeRecommendsResult(*data) for data in ret]

    @logger_decorator
    def get_recipe_inherits(
        self: "BBClient", multi_config: str = ""
    ) -> List[GetRecipeInheritsResult]:
        """Get recipes and its inherit recipes

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetRecipeInheritsResult]: See GetRecipeInheritsResult
        """
        ret: Mapping[str, List[str]] = self.__run_command(  # type: ignore
            self.__server_connection, "getRecipeInherits", multi_config, logger=self.__logger
        )
        return [GetRecipeInheritsResult(key, value) for key, value in ret.items()]

    @logger_decorator
    def get_bb_file_priority(
        self: "BBClient", multi_config: str = ""
    ) -> List[GetBbFilePriorityResult]:
        """Get recipe files and its priority.

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetBbFilePriorityResult]: See GetBbFilePriorityResult
        """
        ret: Mapping[str, int] = self.__run_command(  # type: ignore
            self.__server_connection, "getBbFilePriority", multi_config, logger=self.__logger
        )
        return [GetBbFilePriorityResult(key, value) for key, value in ret.items()]

    @logger_decorator
    def get_default_preference(
        self: "BBClient", multi_config: str = ""
    ) -> List[GetDefaultPreferenceResult]:
        """Get recipes and default preference.

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetDefaultPreference]: See GetDefaultPreference
        """
        ret: Mapping[str, int] = self.__run_command(  # type: ignore
            self.__server_connection, "getDefaultPreference", multi_config, logger=self.__logger
        )
        return [GetDefaultPreferenceResult(key, value) for key, value in ret.items()]

    @logger_decorator
    def get_skipped_recipes(self: "BBClient") -> List[GetSkippedRecipesResult]:
        """Get skipped recipes and its reasons, provides, alias

        Args:
            self (BBClient): none

        Returns:
            List[GetSkippedRecipesResult]: See GetSkippedRecipesResult
        """
        ret: List[List[Any]] = self.__run_command(self.__server_connection, "getSkippedRecipes", logger=self.__logger)  # type: ignore
        return [GetSkippedRecipesResult(*i) for i in ret]

    @logger_decorator
    def get_overlayed_recipes(self: "BBClient", multi_config: str = ""):
        return self.__run_command(
            self.__server_connection, "getOverlayedRecipes", multi_config, logger=self.__logger
        )

    @logger_decorator
    def get_file_appends(
        self: "BBClient", file_path: str, multi_config: str = ""
    ) -> List[str]:
        """Get append files

        Args:
            self (BBClient): none
            file_path (str): recipe file path
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[str]: append files
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getFileAppends", file_path, multi_config, logger=self.__logger
        )

    @logger_decorator
    def get_all_appends(
        self: "BBClient", multi_config: str = ""
    ) -> List[GetAllAppendsResult]:
        """Get all append recipes

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[GetAllAppendsResult]: See GetAllAppendsResult
        """
        ret: List[List[str]] = self.__run_command(  # type: ignore
            self.__server_connection, "getAllAppends", multi_config, logger=self.__logger
        )
        return [GetAllAppendsResult(*i) for i in ret]

    @logger_decorator
    def find_providers(
        self: "BBClient", multi_config: str = ""
    ) -> List[FindProvidersResult]:
        """Get latest packages versions, prefered package versions, and whether there is an REQUIRED_VERSION

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[FindProvidersResult]: See FindProvidersResult
        """
        result: Any = self.__run_command(  # type: ignore
            self.__server_connection, "findProviders", multi_config, logger=self.__logger
        )
        ret: List[FindProvidersResult] = []
        for package in result[0].keys():
            ret.append(
                FindProvidersResult(
                    # yocto dunfell doesn't support result[3](required or not), so checking len(result) == 3
                    package, result[0][package], result[1][package], result[2][package] if len(result) == 3 else None 
                )
            )
        return ret

    @logger_decorator
    def find_best_provider(
        self: "BBClient", package_name: str, multi_config: str = ""
    ) -> List[str]:
        """Get best provider infos

        Args:
            self (BBClient): none
            package_name (str): a package name you want to know the detail of best provider
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[str]: Now under investigation.

        Note:
            | Return value is like [None, None, None, '/PATH/TO/RECIPE/gcc_11.3.bb']. Now under investigation.
        """
        # if you want to know the detail of this line, see bb.runqueue.split_mc.
        package_name = (
            "mc:" + multi_config + ":" + package_name if multi_config else package_name
        )
        return self.__run_command(  # type: ignore
            self.__server_connection, "findBestProvider", package_name, logger=self.__logger
        )

    @logger_decorator
    def all_providers(
        self: "BBClient", multi_config: str = ""
    ) -> List[AllProvidersResult]:
        """Get all providers versions and recipe file path

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See `here <https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations>`_

        Returns:
            List[AllProvidersResult]: See AllProvidersResult

        Note:
            | Return value is like below.
            | [
            |   ['nativesdk-go', [[['', '1.17.10', 'r0'], '/PATH/TO/RECIPE/go_1.17.10.bb']]],  # PN, [PE, PV, PR], recipe file path
            |   ['go', [[['', '1.17.10', 'r0'], '/PATH/TO/RECIPE/go_1.17.10.bb']]],
            | ]
        """
        ret: List[List[Any]] = self.__run_command(  # type: ignore
            self.__server_connection, "allProviders", multi_config, logger=self.__logger
        )
        return [AllProvidersResult(*i) for i in ret]

    @logger_decorator
    def get_runtime_providers(
        self: "BBClient", runtime_providers: List[str], multi_config: str = ""
    ):
        # TODO: What is runtime_provider
        return self.__run_command(
            self.__server_connection,
            "getRuntimeProviders",
            runtime_providers,
            multi_config,
            logger=self.__logger
        )

    @logger_decorator
    def data_store_connector_cmd(
        self: "BBClient", datastore_index: int, command: str, *args, **kwargs
    ) -> Any:
        """Data store management function

        Args:
            self (BBClient): none
            datastore_index (int): specify datastore_index. user can get this value by parse_recipe_file command.
            command (str): the method name of bb.data_smart.DataSmart
            args (Any): depends on command
            kwargs (Any): depends on command

        Returns:
            Any: command return

        Note:
            | User can input following commands. If you want to know detail of these, please see bb.data_smart.DataSmart.

            * createCopy
            * createCopy
            * delVar
            * delVarFlag
            * delVarFlags
            * disableTracking
            * enableTracking
            * expand
            * expandVarref
            * expandWithRefs
            * finalize
            * get
            * getVar
            * getVarFlag
            * getVarFlags
            * get_hash
            * hasOverrides
            * initVar
            * internal_finalize
            * items
            * keys
            * localkeys
            * need_overrides
            * pop
            * popitem
            * prependVar
            * prependVarFlag
            * renameVar
            * setVar
            * setVarFlag
            * setVarFlags
            * setdefault
            * update
            * values
        """
        return self.__run_command(
            self.__server_connection,
            "dataStoreConnectorCmd",
            datastore_index,
            command,
            args,
            kwargs,
            logger=self.__logger
        )

    @logger_decorator
    def data_store_connector_varhist_cmd(
        self: "BBClient", datastore_index: int, command: str, *args, **kwargs
    ) -> Any:
        """Data store variable history function

        Args:
            self (BBClient): none
            datastore_index (int): specify datastore_index. user can get this value by parse_recipe_file command.
            command (str): the method name of bb.data_smart.VariableHistory
            args (Any): depends on command
            kwargs (Any): depends on command

        Returns:
            Any: command return

        Note:
            | User can input following commands. If you want to know detail of these, please see bb.data_smart.VariableHistory.

            * copy
            * del_var_history
            * emit
            * get_variable_files
            * get_variable_items_files
            * get_variable_lines
            * get_variable_refs
            * record
            * rename_variable_hist
            * variable
        """
        return self.__run_command(
            self.__server_connection,
            "dataStoreConnectorVarHistCmd",
            datastore_index,
            command,
            args,
            kwargs,
            logger=self.__logger
        )

    @logger_decorator
    def data_store_connector_var_hist_cmd_emit(
        self: "BBClient",
        datastore_index: int,
        variable: str,
        comment: str,
        val: str,
        override_datastore_index: int,
    ) -> str:
        """Update variable in datastore by variable inoverride datastore

        Args:
            self (BBClient): none
            datastore_index (int): specify datastore_index. user can get this value by parse_recipe_file command.
            variable (str): varibale name
            comment (str): comment for update log()
            override_datastore_index (int): specify datastore_index. user can get this value by parse_recipe_file command.

        Returns:
            str: update log

        Note:
            To be investigate.
        """
        return self.__run_command(  # type: ignore
            self.__server_connection,
            "dataStoreConnectorVarHistCmdEmit",
            datastore_index,
            variable,
            comment,
            "",  # this parameter is not used at all, but accessed, so we have to set a value. If not so, then exception will occur.
            override_datastore_index,
            logger=self.__logger
        )

    @logger_decorator
    def data_store_connector_inc_hist_cmd(
        self: "BBClient", datastore_index: int, command: str, *args, **kwargs
    ) -> Any:
        """Data store include history function

        Args:
            self (BBClient): none
            datastore_index (int): specify datastore_index. user can get this value by parse_recipe_file command.
            command (str): the method name of bb.data_smart.IncludeHistory
            args (Any): depends on command
            kwargs (Any): depends on command

        Returns:
            Any: command return

        Note:
            | User can input following commands. If you want to know detail of these, please see bb.data_smart.IncludeHistory.

            * copy
            * include
            * emit
        """
        return self.__run_command(
            self.__server_connection,
            "dataStoreConnectorIncHistCmd",
            datastore_index,
            command,
            args,
            kwargs,
            logger=self.__logger
        )

    @logger_decorator
    def data_store_connector_release(self: "BBClient", datastore_index: int) -> None:
        """Discard data store

        Args:
            self (BBClient): none
            datastore_index (int): specify datastore_index. user can get this value by parse_recipe_file command.
        """
        self.__run_command(
            self.__server_connection, "dataStoreConnectorRelease", datastore_index, logger=self.__logger
        )

    @logger_decorator
    def parse_recipe_file(
        self: "BBClient",
        file_path: str,
        append: bool = True,
        append_list: Optional[str] = None,
        datastore_index: Optional[int] = None,
    ) -> Optional[int]:
        """Parse recipe file

        Args:
            self (BBClient): none
            file_path (str): recipe file path
            append (bool, optional): whether to append. Defaults to True.
            append_list (Optional[str], optional): Append file list. Defaults to None. If None, bitbake loads append files automatically.
            datastore_index (int): specify datastore_index. user can get this value by parse_recipe_file command.

        Returns:
            Optional[int]: data store index

        Note:
            | This commands parses recipe file and store result into datastore. User can access the result by data store index. It's not clear how the fifth parameter(datastore_index) works.
        """
        ret: Mapping[str, int] = (
            self.__run_command(  # type: ignore
                self.__server_connection,
                "parseRecipeFile",
                file_path,
                append,
                append_list,
                datastore_index,
                logger=self.__logger
            )
            if datastore_index
            else self.__run_command(
                self.__server_connection,
                "parseRecipeFile",
                file_path,
                append,
                append_list,
                logger=self.__logger
            )
        )
        return ret["dsindex"] if ret else None

    # --- bitbake server async functions  ---
    @logger_decorator
    def build_file(
        self: "BBClient", file_path: str, task_name: str, internal: bool = False
    ) -> None:
        """Build recipe file

        This command will send following events. If you want to wait done, please use wait_done_async.


        * bb.event.BuildInit
        * bb.event.RecipePreFinalise
        * bb.event.RecipePostKeyExpansion
        * bb.event.RecipeTaskPreProcess
        * bb.event.RecipeParsed
        * bb.event.BuildStarted
        * bb.event.ProcessStarted
        * bb.event.ProcessProgress
        * bb.event.ProcessFinished
        * bb.runqueue.runQueueTaskStarted
        * bb.runqueue.runQueueTaskCompleted
        * bb.event.BuildCompleted
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
            file_path (str): target recipe file path
            task_name (str): task name which will run
            internal (bool, optional): If True, bitbake will fire events that notify BuildStarted and BuildCompleted. Defaults to False.

        Note:
            | If you want to monitor BuildStarted and BuildCompleted event, use get_event.
        """
        self.__run_command(
            self.__server_connection, "buildFile", file_path, task_name, internal, logger=self.__logger
        )

    @logger_decorator
    def build_targets(
        self: "BBClient",
        targets: List[str],
        task_name: str,
    ) -> None:
        """Build package

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.runqueue.runQueueTaskStarted
        * bb.build.TaskStarted
        * bb.build.TaskProgress
        * bb.build.TaskSucceeded
        * bb.event.ProcessStarted
        * bb.event.ProcessProgress
        * bb.event.ProcessFinished
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
            targets (List[str]): see Note section
            task_name (str): task name which will run

        Note:
            | User can input targets as follows. Please note that if you want to specify task by targets, you have to write do_xxx, not only xxx.
            | [
            |   "gcc",                              # only package name
            |   "mc:xxx_config:alsa",               # multiconfig and package name
            |   "multiconfig:yyy_config:vim",       # multiconfig and package name
            |   "mc:\*:clang"                       # all multiconfig and package name
            |   "mc:yyy_config:python:do_patch",    # multiconfig, package name and task name
            | ]
        """

        self.__run_command(self.__server_connection, "buildTargets", targets, task_name, logger=self.__logger)

    @logger_decorator
    def generate_dep_tree_event(
        self: "BBClient", targets: List[str], task_name: str
    ) -> None:
        """Request dependency tree information

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.event.TreeDataPreparationStarted
        * bb.event.TreeDataPreparationProgress
        * bb.event.TreeDataPreparationCompleted
        * bb.event.DepTreeGenerated
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
            targets(List[str]): targets info. see Note section.
            task_name (str): task name. e.g.) do_build, do_fetch, etc...

        Note:
            | User can input targets as follows.
            | [
            |   "gcc",                              # only package name
            |   "mc:xxx_config:alsa",               # multiconfig and package name
            |   "multiconfig:yyy_config:vim",       # multiconfig and package name
            |   "mc:\*:clang"                        # all multiconfig and package name
            |   "mc:yyy_config:python:do_patch",    # multiconfig, package name and task name
            | ]
        """
        self.__run_command(
            self.__server_connection,
            "generateDepTreeEvent",
            targets,
            task_name,
            logger=self.__logger
        )

    @logger_decorator
    def generate_dot_graph(
        self: "BBClient", targets: List[str], task_name: str
    ) -> None:
        """Generate task dependency graph(task-depends.dot)

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.event.TreeDataPreparationStarted
        * bb.event.TreeDataPreparationProgress
        * bb.event.TreeDataPreparationCompleted
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
            targets (List[str]): targets info. see Note section.
            task_name (str): task name. e.g.) do_build, do_fetch, etc...

        Note:
            | User can input targets as follows.
            | [
            |   "gcc",                              # only package name
            |   "mc:xxx_config:alsa",               # multiconfig and package name
            |   "multiconfig:yyy_config:vim",       # multiconfig and package name
            |   "mc:\*:clang"                        # all multiconfig and package name
            |   "mc:yyy_config:python:do_patch",    # multiconfig, package name and task name
            | ]
        """
        self.__run_command(
            self.__server_connection,
            "generateDotGraph",
            targets,
            task_name,
            logger=self.__logger
        )

    @logger_decorator
    def generate_targets_tree(
        self: "BBClient", bb_klass_file_path: str, package_names: List[str]
    ) -> None:
        """Generate target tree

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.event.TreeDataPreparationStarted
        * bb.event.TreeDataPreparationProgress
        * bb.event.TreeDataPreparationCompleted
        * bb.event.TargetsTreeGenerated
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
            bb_klass_file_path (str): bbclass file path
            package_names (List[str]): target package names

        Note:
            | Use can receive result by bb.event.TargetsTreeGenerated event.
            | If you specify bb_klass_file_path, bitbake will add the packages that inherits bb_klass_file_path to package_names. If you don't want to do it, please input None to bb_klass_file_path.
        """
        self.__run_command(
            self.__server_connection,
            "generateTargetsTree",
            bb_klass_file_path,
            package_names,
            logger=self.__logger
        )

    @logger_decorator
    def find_config_files(self: "BBClient", variable_name: str) -> None:
        """Find Config files that define specified variable.

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.event.ConfigFilesFound
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
            variable_name (str): _description_

        Note:
            | User can receive result by bb.event.ConfigFilesFound event.
        """
        self.__run_command(self.__server_connection, "findConfigFiles", variable_name, logger=self.__logger)

    @logger_decorator
    def find_files_matching_in_dir(
        self: "BBClient", target_file_name_substring: str, directory: str
    ) -> None:
        """Find files that matches the regex_pattern from the directory.

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.event.FilesMatchingFound
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
            target_file_name_substring (str): Substrings of target file name. e.g.) ".conf", "xxx.bbappe", etc...
            directory (str): Target directory. Base directory is ${BBPATH}.

        Note:
            | Use can receive result by bb.event.FilesMatchingFound event.
        """
        self.__run_command(
            self.__server_connection,
            "findFilesMatchingInDir",
            target_file_name_substring,
            directory,
            logger=self.__logger
        )

    @logger_decorator
    def test_cooker_command_event(self: "BBClient", pattern: str) -> None:
        """Dummy command

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.event.FilesMatchingFound
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
            pattern (str): dummy param
        """
        self.__run_command(self.__server_connection, "testCookerCommandEvent", pattern, logger=self.__logger)

    @logger_decorator
    def find_config_file_path(self: "BBClient", config_file_name: str) -> None:
        """Find config file path

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.event.ConfigFilePathFound
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
            config_file_name (str): target config file name

        Note:
            | Use can receive result by bb.event.ConfigFilePathFound event.
        """
        self.__run_command(
            self.__server_connection, "findConfigFilePath", config_file_name, logger=self.__logger
        )

    @logger_decorator
    def show_versions(self: "BBClient") -> None:
        """Show all packages versions

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none

        Note:
            | bbclient doesn't display any information. If you want to use this feature, please use bitbake-layers.
        """
        self.__run_command(self.__server_connection, "showVersions", logger=self.__logger)

    @logger_decorator
    def show_environment_target(self: "BBClient", package_name: str = "") -> None:
        """Show variables for specified package

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.event.ConfigParsed
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
            package_name (str): target package name

        Note:
            | bbclient doesn't display any information. If you want to use this feature, please use bitbake-gervar or bitbake -e.
        """
        self.__run_command(
            self.__server_connection, "showEnvironmentTarget", package_name, logger=self.__logger
        )

    @logger_decorator
    def show_environment(self: "BBClient", bb_file_path: str) -> None:
        """Show variables for specified recipe

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.event.ConfigParsed
        * bb.event.CacheLoadStarted
        * bb.event.CacheLoadProgress
        * bb.event.CacheLoadCompleted
        * bb.event.RecipePreFinalise
        * bb.event.RecipePostKeyExpansion
        * bb.event.RecipeTaskPreProcess
        * bb.event.RecipeParsed
        * bb.event.ConfigParsed
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
            bb_file_path (str): target recipe path

        Note:
            | bbclient doesn't display any information. If you want to use this feature, please use bitbake-gervar or bitbake -e.
        """
        self.__run_command(self.__server_connection, "showEnvironment", bb_file_path, logger=self.__logger)

    @logger_decorator
    def parse_files(self: "BBClient") -> None:
        """Parse all bb files.

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.event.ReachableStamps
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
        """
        self.__run_command(self.__server_connection, "parseFiles", logger=self.__logger)

    @logger_decorator
    def compare_revisions(self: "BBClient") -> None:
        """Exit async command

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none

        Note:
            | TODO: investigate the detail.
            | This determines if the cache is out of date, and if so, this terminates asynchronous processing.
        """
        self.__run_command(self.__server_connection, "compareRevisions", logger=self.__logger)

    @logger_decorator
    def trigger_event(self: "BBClient", evene_name: str) -> None:
        """Send event

        Args:
            self (BBClient): none
            evene_name (str): event class name.

        Note:
            | Send evene_name event. User can receive this event by get_event.
        """
        self.__run_command(self.__server_connection, "triggerEvent", evene_name, logger=self.__logger)

    @logger_decorator
    def reset_cooker(self: "BBClient") -> None:
        """Reset cooker state and caches.

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.event.ConfigParsed
        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none

        Note:
            | TODO: investigate the detail.
        """
        self.__run_command(self.__server_connection, "resetCooker", logger=self.__logger)

    @logger_decorator
    def client_complete(self: "BBClient") -> None:
        """Notify client will be close

        This command will send following events. If you want to wait done, please use wait_done_async.

        * bb.command.CommandCompleted
        * bb.command.CommandFailed
        * bb.command.CommandExit

        Args:
            self (BBClient): none
        """
        self.__run_command(self.__server_connection, "clientComplete", logger=self.__logger)

    @logger_decorator
    def find_sigInfo(
        self: "BBClient",
        package_name_with_multi_config: str,
        task_name: str,
        sigs: List[str],
    ) -> None:
        """Find signature info files via the signature generator(?)

        Args:
            self (BBClient): none
            package_name_with_multi_config (str): TODO
            task_name (str): TODO
            sigs (List[str]): TODO

        Note:
            | Use can receive result by bb.event.FindSigInfoResult event.
        """
        self.__run_command(
            self.__server_connection,
            "findSigInfo",
            package_name_with_multi_config,
            task_name,
            sigs,
            logger=self.__logger
        )

    # --- private functions ---

    @staticmethod
    def __connect_server(
        server_adder: str, project_path: str
    ) -> Tuple["bb.server.xmlrpcclient.BitBakeXMLRPCServerConnection", "module"]:  # type: ignore
        """Connect to server

        Returns:
            _type_: ("bb.server.xmlrpcclient.BitBakeXMLRPCServerConnection", "module")
        """
        # TODO: use shell not to be depends on bb modules
        sys.path.append(f"{project_path}/bitbake/lib")
        from bb.main import setup_bitbake, BitBakeConfigParameters  # type: ignore
        from bb.tinfoil import TinfoilConfigParameters  # type: ignore

        config_params: TinfoilConfigParameters = TinfoilConfigParameters(
            config_only=False, quiet=4
        )
        config_params.remote_server: str = server_adder  # type: ignore
        server_connection, ui_module = setup_bitbake(config_params, [])
        ui_module.main(
            server_connection.connection, server_connection.events, config_params
        )
        return server_connection, ui_module

    @staticmethod
    def __run_command(server_connection, command: str, *params: Any, logger: Optional[Logger]) -> Optional[Any]:
        """Run command

        Args:
            server_connection (_type_): use return value of __connect_server()
            command (str): commands bitbake defined
            params (Any): paramters for command
            logger (Optional[Logger]): logger for debugging

        Returns:
            Optional[Any]: command return
        """
        commandline: List[str] = [command]
        commandline.extend(params if params else [])
        try:
            result = server_connection.connection.runCommand(commandline)
        except:
            if logger:
                logger.error(f"{command} failed beacuse {result}.")
            return None
        return result[0]
