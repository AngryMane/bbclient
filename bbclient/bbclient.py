import os
import sys
import subprocess
from typing import Any, List, Optional, Tuple, Mapping


class BBClient:

    # --- setup functions ---
    def __init__(
        self: "BBClient", project_abs_path: str, init_script_path: str
    ) -> None:
        """Initialize BBClient instance

        Args:
            self (BBClient): none
            project_abs_path (str): abslute path to bitbake project, basically poky dir.
            init_script_path (str): initialize bitbake proejct command running at project_abs_path. This is maybe ". oe-init-build-env".
        """
        self.__project_path: str = project_abs_path
        self.__is_server_running: bool = False
        pipe: subprocess.Popen = subprocess.Popen(
            f"{init_script_path} > /dev/null; env",
            stdout=subprocess.PIPE,
            shell=True,
            cwd=self.__project_path,
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
            cwd=self.__project_path,
            executable="/bin/bash",
            text=True,
        )
        output, _ = pipe.communicate()
        connection, _ = self.__connect_server(
            server_adder_with_port, self.__project_path
        )
        self.__server_connection = connection
        self.__is_server_running = True

    def stop_server(self: "BBClient") -> None:
        """Stop bitbake XML RPC server

        Args:
            self (BBClient): none
        """
        if not self.__is_server_running:
            return
        self.__server_connection.connection.terminateServer()
        self.__server_connection.terminate()
        self.__is_server_running = False

    # --- bitbake server sync functions  ---
    def state_shutdown(self: "BBClient") -> None:
        """Terminate tasks

        Args:
            self (BBClient): none

        Note:
            Terminate tasks defined in recipes. If there are running tasks, wait for them to exit.
        """
        self.__run_command(self.__server_connection, "stateShutdown")

    def state_force_shutdown(self: "BBClient") -> None:
        """Terminate tasks

        Args:
            self (BBClient): none

        Note:
            Terminate tasks defined in recipes. If there are running tasks, terminate them.
        """
        self.__run_command(self.__server_connection, "stateForceShutdown")

    def get_all_keys_with_flags(self: "BBClient", flag_list: List[str]) -> Mapping:
        """Get value, history and specified flags of all global variables.

        Args:
            self (BBClient): none
            flag_list(List[str]): Target flags. If flags are unnecessary, please set [].

        Returns:
            | Dict object like below.
            | {
            |     "VARIABLE_A_NAME" : {
            |         "v" : "VARIABLE_A_VALUE",
            |         "history" : [
            |                         {
            |                             'parsing': True,
            |                             'variable': 'VARIABLE_NAME',
            |                             'file': 'PATH/TO/FILE/xxx.inc',
            |                             'line': ${LINE_NUM},
            |                             'op': 'set',
            |                             'detail': 'SETTING VALUE AT THIS POINT'
            |                         },
            |                         {
            |                             'parsing': True,
            |                             'variable': 'VARIABLE_NAME',
            |                             'file': 'PATH/TO/FILE/xxx.inc',
            |                             'line': ${LINE_NUM},
            |                             'op': 'set',
            |                             'detail': 'SETTING VALUE AT THIS POINT'
            |                         },
            |                     ]
            |         "FLAG_A_NAME": "FLAG_A_VALUE",
            |         "FLAG_B_NAME": "FLAG_B_VALUE"
            |     },
            |     "VARIABLE_B_NAME" : {
            |         "v" : "VARIABLE_B_VALUE",
            |         "history" : [ ... ],
            |         "FLAG_A_NAME": "FLAG_A_VALUE",
            |         "FLAG_B_NAME": "FLAG_B_VALUE"
            |     },
            | }

        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getAllKeysWithFlags", flag_list
        )

    def get_variable(self: "BBClient", name: str, expand: bool = True) -> str:
        """Get variable value

        Args:
            self (BBClient): none
            name (str): variable name
            expand (bool, optional): Whether to expand references to other variables. Defaults to True.

        Returns:
            str: variable value
        """
        return self.__run_command(self.__server_connection, "getVariable", name, expand)  # type: ignore

    def set_variable(self: "BBClient", name: str, value: str) -> None:
        """Set vaiable value

        Args:
            self (BBClient): none
            name (str): variable name
            value (str): variable value you want to set

        """
        self.__run_command(self.__server_connection, "setVariable", name, value)

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
        return self.__run_command(  # type: ignore
            self.__server_connection, "getSetVariable", name, expand
        )

    def set_config(self: "BBClient", name: str, value: str) -> None:
        """Set CookerConfigcation properties

        Args:
            self (BBClient): none
            name (str): property name
            value (str): property value

        Note:
            | If you want to know all CookerConfigcation properties, see poky/bitbake/lib/bb/cookerdata.py.
            | But I don't know the detail and how to use it...
        """
        self.__run_command(self.__server_connection, "setConfig", name, value)

    def enable_data_tracking(self: "BBClient") -> None:
        """Enable data tracking

        Args:
            self (BBClient): none

        Note:
            | If enable, cooker cacheata(VariableHistory class) logs the history of changin value.
            | You can see the log by dataStoreConnectorVarHistCmdEmit command.
        """
        self.__run_command(self.__server_connection, "enableDataTracking")

    def disable_data_tracking(self: "BBClient") -> None:
        """Disable data tracking

        Args:
            self (BBClient): none

        Note:
            Please see enable_data_tracking command
        """
        self.__run_command(self.__server_connection, "disableDataTracking")

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
            self.__server_connection, "setPrePostConfFiles", pre_files, post_files
        )

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

        Note:
            | This command can extract only one file. If you input the regex matching to many file, this command will fail.
            | This command maybe has a bug. The second parameter and the first one mixed up in the command.
        """

        return self.__run_command(  # type: ignore
            self.__server_connection, "matchFile", file_path_regex, mutli_conf_name
        )

    def get_uihandler_num(self: "BBClient") -> int:
        """Get ui handler num.

        Args:
            self (BBClient): none

        Returns:
            int: ui hanlder num
        """
        return self.__run_command(self.__server_connection, "getUIHandlerNum")  # type: ignore

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
            | debug_domains is a little bit complex.
            | If you want to extract logging.getLogger("NAME"), put { "NAME": logging.INFO }.
            | debug_domains value filters log level like log_level arg.
            | log_level arg and debug_domains value are `or conditoin`.

            | mask is also a little bit difficult.
            | This args filters log by event class name like bb.event.BuildStarted, bb.command.CommandCompleted, etc..
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
        )

    def set_features(self: "BBClient", features: List[int]) -> None:
        """Set feature(Enable feature)

        Args:
            self (BBClient): none
            features (List[int]): list of 0, 1, 2. 1 means HOB_EXTRA_CACHES, 2 means BASEDATASTORE_TRACKING and 3 means SEND_SANITYEVENTS.

        Note:
            | if enable HOB_EXTRA_CACHES, recipecheces has extra-info like SUMMARY, LICENSE, DESCRIPTION, etc...
            | if enable BASEDATASTORE_TRACKING, enable_data_tracking. See enable_data_tracking command.
            | if enable SEND_SANITYEVENTS, this feature has not been implemented and is currently meaningless.
        """
        self.__run_command(self.__server_connection, "setFeatures", features)

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
            environment (Mapping[str, str]): _description_
            command_line (str): _description_

        Note:
            | options will set like {"prefile": ["FILE_NAME", "FILE_NAME"], "postfile": ["FILE_NAME", "FILE_NAME"]}
            | They are prefiles and postfiles settings. See set_pre_post_conf_files command.
            | if you change prefiles or postfiles, bitbake will reset their cache.

            | environment is environment variables, like {"KEY": "VALUE", "KEY": "VALUE"}.
            | if you add/change/delete any environemt variable, bitbake will reset their cache.

            | command_line will set to BB_CMDLINE variable. BB_CMDLINE seems not to be used at all.
        """
        self.__run_command(
            self.__server_connection, "updateConfig", options, environment, command_line
        )

    def parse_configuration(self: "BBClient") -> None:
        """Parse configuration

        Note:
            This command clears caches and re-builds them.
        """
        self.__run_command(self.__server_connection, "parseConfiguration")

    def get_layer_priorities(self: "BBClient") -> List[List[str]]:
        """Get name, path, priority of all layers

        Args:
            self (BBClient): none

        Returns:
            List[List[str]]: name, path, priority of all layers

        Note:
            | Return value is like follows.
            | [
            |   ['core', '^/PATH/TO/POKY/poky/meta/', '^/PATH/TO/POKY/poky/meta/', 5],
            |   ['yocto', '^/PATH/TO/POKY/poky/meta-poky/', '^/PATH/TO/POKY/poky/meta-poky/', 5],
            |   ['yoctobsp', '^/PATH/TO/POKY/poky/meta-yocto-bsp/', '^/PATH/TO/POKY/poky/meta-yocto-bsp/', 5],
            |   ['raspberrypi', '^/PATH/TO/POKY/poky/meta-raspberrypi/', '^/PATH/TO/POKY/poky/meta-raspberrypi/', 9]
            | ]
            | The first element is layer name. the second is layer path, the third seems same as the second, but detail is not clear.
            | The fourth element is layer priority.
        """
        # Note: this command deletes caches(bug?)
        return self.__run_command(self.__server_connection, "getLayerPriorities")  # type: ignore

    def get_recipes(self: "BBClient", multi_config: str = "") -> List[str]:
        """Get all package name from cache

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            List[str]: package names
        """
        return self.__run_command(self.__server_connection, "getRecipes", multi_config)  # type: ignore

    def get_recipe_depends(self: "BBClient", multi_config: str = "") -> List[List[Any]]:
        """Get recipe depends

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            List[List[Any]]: See Note section.

        Note:
            | Return value is like below.
            | [
            |     ['RECIPE_NAME:RECIPE_FILE_PATH',
            |         [
            |             'depends-package-name-a',
            |             'depends-package-name-b',
            |             'depends-package-name-c',
            |         ]
            |     ],
            | ]
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getRecipeDepends", multi_config
        )

    def get_recipe_versions(
        self: "BBClient", multi_config: str = ""
    ) -> Mapping[str, List[str]]:
        """Get all recipe versions

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            Mapping[str, List[str]]: Recipes file and its version info

        Note:
            | Return value is like below.
            | {
                |   '/PATH/TO/POKY/poky/meta/recipes-graphics/cantarell-fonts/cantarell-fonts_0.303.1.bb': ['', '0.303.1', 'r0'],
            | }
            | ['', '0.303.1', 'r0'] is [PE, PV, PR]. If you want to know PE/PV/PR, see https://docs.yoctoproject.org/ref-manual/variables.html?highlight=bblayers# .
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getRecipeVersions", multi_config
        )

    def get_recipe_provides(
        self: "BBClient", multi_config: str = ""
    ) -> Mapping[str, List[str]]:
        """Get all recipe files and its packages

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            Mapping[str, List[str]]: All recipe files and its packages

        Note:
            | Return value is like below.
            | {
            |   '/PATH/TO/RECIPE/inetutils_2.2.bb': ['inetutils'],
            | }
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getRecipeProvides", multi_config
        )

    def get_recipe_packages(
        self: "BBClient", multi_config: str = ""
    ) -> Mapping[str, List[str]]:
        """Get all recipe files and its recipe files

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            Mapping[str, List[str]]: All recipe files and its recipe files.

        WARNING:
            | This command doesn't work beacuase of bitbake bug.
            | bitbake XML RPC server try to return collections.defaultdict type, but XMLRPC server can't support this type.

        Note:
            | I fixed the bug locally, then this commands returns like below.
            | {
            |   'PACKAGE_NAME': ['/PATH/TO/RECIPE/cryptodev-linux_1.12.bb']
            | }
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getRecipePackages", multi_config
        )

    def get_recipe_packages_dynamic(
        self: "BBClient", multi_config: str = ""
    ) -> Mapping[str, List[str]]:
        """Get all recipe files that provides PACKAGE_DYNAMIC and its PACKAGE_DYNAMIC

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            Mapping[str, List[str]]: all recipe files that provides PACKAGE_DYNAMIC and its PACKAGE_DYNAMIC

        WARNING:
            | This command doesn't work beacuase of bitbake bug.
            | bitbake XML RPC server try to return collections.defaultdict type, but XMLRPC server can't support this type.

        Note:
            | I fixed the bug locally, then this commands returns like below.
            | {
            |   '^nativesdk-packagegroup-sdk-host-locale-.*': ['/PATH/TO/RECIPE/nativesdk-packagegroup-sdk-host.bb'],
            | }
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getRecipePackagesDynamic", multi_config
        )

    def get_r_providers(
        self: "BBClient", multi_config: str = ""
    ) -> Mapping[str, List[str]]:
        """Get alias of PN and its recipe files

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            Mapping[str, List[str]]: alias of PN and its recipe files

        WARNING:
            | This command doesn't work beacuase of bitbake bug.
            | bitbake XML RPC server try to return collections.defaultdict type, but XMLRPC server can't support this type.

        Note:
            | If you want to know the detail of alias of PN, See https://docs.yoctoproject.org/ref-manual/variables.html?highlight=rprovide#term-RPROVIDES
            | I fixed the bug locally, then this commands returns like below.
            | {
            |   'opkg-config-base': ['/PATH/TO/RECIPE/opkg-arch-config_1.0.bb']
            | }
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getRProviders", multi_config
        )

    def get_runtime_depends(
        self: "BBClient", multi_config: str = ""
    ) -> List[List[Any]]:
        """Get all runtime dependency by all recipe files

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            List[List[Any]]: all runtime dependency by all recipe files

        Note:
            | Return value is like below.
            | [
            |   [
            |       'virtual:nativesdk:/PATH/TO/RECIPE/coreutils_9.0.bb',
            |       {
            |           'nativesdk-coreutils-src': [],
            |           'nativesdk-coreutils-dbg': [],
            |           'nativesdk-coreutils-staticdev': ['nativesdk-coreutils-dev'],
            |           'nativesdk-coreutils-dev': ['nativesdk-coreutils'],
            |           'nativesdk-coreutils-doc': [],
            |           'nativesdk-coreutils-locale': [],
            |           'nativesdk-coreutils': []
            |       }
            |   ],
            |]

        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getRuntimeDepends", multi_config
        )

    def get_runtime_recommends(
        self: "BBClient", multi_config: str = ""
    ) -> List[List[Any]]:
        """Get all runtime recoomends(=weak depends) by all recipe files

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            List[List[Any]]: all runtime recoomends(=weak depends) by all recipe files

        Note:
            Return value is same format as get_runtime_depends command.
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getRuntimeRecommends", multi_config
        )

    def get_recipe_inherits(
        self: "BBClient", multi_config: str = ""
    ) -> Mapping[str, List]:
        """Get recipes and its inherit recipes

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            Mapping[str, List]: recipes and its inherit recipes

        Note:
            | Return value is like below.
            | {
            |   '/PATH/TO/RECIPE/build-appliance-image_15.0.0.bb': [
            |       '/PATH/TO/RECIPE/base.bbclass',
            |       '/PATH/TO/RECIPE/patch.bbclass',                                                                                                           5         '/home/yosuke/work/git/yocto-learning/poky/meta/classes/terminal.bbclass',
            |       '/PATH/TO/RECIPE/staging.bbclass',
            |       '/PATH/TO/RECIPE/mirrors.bbclass',
            |       '/PATH/TO/RECIPE/utils.bbclass',
            |       '/PATH/TO/RECIPE/utility-tasks.bbclass',
            |       '/PATH/TO/RECIPE/metadata_scm.bbclass',
            |       '/PATH/TO/RECIPE/logging.bbclass',
            |   ],
            | }
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getRecipeInherits", multi_config
        )

    def get_bb_file_priority(
        self: "BBClient", multi_config: str = ""
    ) -> Mapping[str, int]:
        """Get recipe files and its priority.

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            Mapping[str, int]: recipe files and its priority

        Note:
            | Return value is like below.
            | {
            |   '/PATH/TO/RECIPE/l3afpad_git.bb': 5,
            |   '/PATH/TO/RECIPE/cups_2.4.2.bb': 5,
            | }
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getBbFilePriority", multi_config
        )

    def get_default_preference(
        self: "BBClient", multi_config: str = ""
    ) -> Mapping[str, int]:
        """Get recipes and default preference.

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            Mapping[str, int]: recipes and default preference

        Notes:
            | Return value is like below.
            | {
            |   '/PATH/TO/RECIPE/gcr_3.40.0.bb': 0,
            |   '/PATH/TO/RECIPE/python3-smmap_5.0.0.bb': 0,
            | }
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getDefaultPreference", multi_config
        )

    def get_skipped_recipes(self: "BBClient") -> List[List[Any]]:
        """Get skipped recipes and its reasons, provides, alias

        Args:
            self (BBClient): none

        Returns:
            List[List[Any]]: skipped recipes and its reasons, provides, alias

        Note:
            | Return value is like below.
            | [
            |   [
            |       '/PATH/TO/RECIPE/raspidmx_git.bb',
            |       {
            |           'pn': 'raspidmx',
            |           'skipreason': 'incompatible with host aarch64-poky-linux (not in COMPATIBLE_HOST)',
            |           'provides': ['raspidmx'],
            |           'rprovides': ['raspidmx-src', 'raspidmx-dbg', 'raspidmx-staticdev', 'raspidmx-dev', 'raspidmx-doc', 'raspidmx-locale', 'raspidmx']
            |       }
            |   ],
            | ]
        """
        return self.__run_command(self.__server_connection, "getSkippedRecipes")  # type: ignore

    def get_overlayed_recipes(self: "BBClient", multi_config: str = ""):
        return self.__run_command(
            self.__server_connection, "getOverlayedRecipes", multi_config
        )

    def get_file_appends(
        self: "BBClient", file_path: str, multi_config: str = ""
    ) -> List[str]:
        """Get append files

        Args:
            self (BBClient): none
            file_path (str): recipe file path
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            List[str]: append files
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getFileAppends", file_path, multi_config
        )

    def get_all_appends(self: "BBClient", multi_config: str = "") -> List[List[str]]:
        """Get all append recipes

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            List[List[str]]: all append recipes

        Note:
            | Return value is like below.
            | [
            |   [
            |       'busybox_%.bb',
            |       '/PATH/TO/RECIPE/busybox_%.bbappend'
            |   ],
            | ]
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "getAllAppends", multi_config
        )

    def find_providers(
        self: "BBClient", multi_config: str = ""
    ) -> List[Mapping[str, Any]]:
        """Get latest packages versions, prefered package versions, and whether there is an REQUIRED_VERSION

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            List[Mapping[str, Any]]: latest packages versions, prefered package versions, and whether there is an REQUIRED_VERSION

        Note:
            | Return value is like below.
            | [
            |   {
            |       find_providers: {'nativesdk-python3-pysocks': [['', '2.8.3', 'r0'], '/PATH/TO/RECIPE/python3-pysocks_2.8.3.bb']    # latest version info
            |   },
            |   {
            |       find_providers: {'nativesdk-python3-pysocks': [['', '1.7.1', 'r0'], '/PATH/TO/RECIPE/python3-pysocks_1.7.1.bb']    # prefered version info
            |   },
            |   {
            |       find_providers: False  # whether there is an REQUIRED_VERSION
            |   },
            | ]

        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "findProviders", multi_config
        )

    def find_best_provider(
        self: "BBClient", package_name: str, multi_config: str = ""
    ) -> List[str]:
        """Get best provider infos

        Args:
            self (BBClient): none
            package_name (str): _description_
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            List[str]: Now under investigation.

        Note:
            | Return value is like below. Now under investigation.
            | [None, None, None, '/PATH/TO/RECIPE/gcc_11.3.bb']
        """
        # if you want to know the detail of this line, see bb.runqueue.split_mc.
        package_name = (
            "mc:" + multi_config + ":" + package_name if multi_config else package_name
        )
        return self.__run_command(  # type: ignore
            self.__server_connection, "findBestProvider", package_name
        )

    def all_providers(self: "BBClient", multi_config: str = "") -> List[List[Any]]:
        """Get all providers versions and recipe file path

        Args:
            self (BBClient): none
            multi_config (str, optional): Defaults to "". See https://docs.yoctoproject.org/dev-manual/common-tasks.html?highlight=multiconfigs#building-images-for-multiple-targets-using-multiple-configurations

        Returns:
            List[List[Any]]: all providers versions and recipe file path

        Note:
            | Return value is like below.
            | [
            |   ['nativesdk-go', [[['', '1.17.10', 'r0'], '/PATH/TO/RECIPE/go_1.17.10.bb']]],  # PN, [PE, PV, PR], recipe file path
            |   ['go', [[['', '1.17.10', 'r0'], '/PATH/TO/RECIPE/go_1.17.10.bb']]],
            | ]
        """
        return self.__run_command(  # type: ignore
            self.__server_connection, "allProviders", multi_config
        )

    def get_runtime_providers(
        self: "BBClient", runtime_providers: List[str], multi_config: str = ""
    ):
        # TODO: What is runtime_provider
        return self.__run_command(
            self.__server_connection,
            "getRuntimeProviders",
            runtime_providers,
            multi_config,
        )

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
        )

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
        )

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
        )

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
        )

    def data_store_connector_release(self: "BBClient", datastore_index: int) -> None:
        """Discard data store

        Args:
            self (BBClient): none
            datastore_index (int): specify datastore_index. user can get this value by parse_recipe_file command.
        """
        self.__run_command(
            self.__server_connection, "dataStoreConnectorRelease", datastore_index
        )

    def parse_recipe_file(
        self: "BBClient",
        file_path: str,
        append: bool = True,
        append_list: Optional[str] = None,
        datastore_index: Optional[int] = None,
    ) -> int:
        """Parse recipe file

        Args:
            self (BBClient): none
            file_path (str): recipe file path
            append (bool, optional): whether to append. Defaults to True.
            append_list (Optional[str], optional): Append file list. Defaults to None. If None, bitbake loads append files automatically.
            datastore_index (int): specify datastore_index. user can get this value by parse_recipe_file command.

        Returns:
            int: data store index

        Note:
            | This commands parses recipe file and store result into datastore.
            | User can access the result by data store index.
            | It's not clear how the fifth parameter(datastore_index) works.
        """
        ret: Mapping[str, int] = (
            self.__run_command(  # type: ignore
                self.__server_connection,
                "parseRecipeFile",
                file_path,
                append,
                append_list,
                datastore_index,
            )
            if datastore_index
            else self.__run_command(
                self.__server_connection,
                "parseRecipeFile",
                file_path,
                append,
                append_list,
            )
        )
        return ret["dsindex"]

    # --- bitbake server async functions  ---
    def build_file(
        self: "BBClient", file_name: str, task_name: str, internal: bool = False
    ) -> None:
        self.__run_command(
            self.__server_connection, "buildFile", file_name, task_name, internal
        )

    def build_targets(
        self: "BBClient",
        package_names_with_task: List[str],
        task_name: str,
    ) -> None:
        self.__run_command(
            self.__server_connection, "buildTargets", package_names_with_task, task_name
        )

    def generate_dep_tree_event(
        self: "BBClient", package_names_with_multiconfig: List[str], task_name: str
    ) -> None:
        self.__run_command(
            self.__server_connection,
            "generateDepTreeEvent",
            package_names_with_multiconfig,
            task_name,
        )

    def generate_dot_graph(
        self: "BBClient", package_names_with_multiconfig: List[str], task_name: str
    ) -> None:
        self.__run_command(
            self.__server_connection,
            "generateDotGraph",
            package_names_with_multiconfig,
            task_name,
        )

    def generate_targets_tree(
        self: "BBClient", klass: str, package_names: List[str]
    ) -> None:
        self.__run_command(
            self.__server_connection, "generateTargetsTree", klass, package_names
        )

    def find_config_files(self: "BBClient", name: str) -> None:
        self.__run_command(self.__server_connection, "findConfigFiles", name)

    def find_files_matchingin_dir(
        self: "BBClient", regex_pattern: str, directory: str
    ) -> None:
        self.__run_command(
            self.__server_connection, "findConfigFiles", regex_pattern, directory
        )

    def test_cooker_command_event(self: "BBClient", pattern: str) -> None:
        self.__run_command(self.__server_connection, "testCookerCommandEvent", pattern)

    def find_config_file_path(self: "BBClient", config_file_name: str) -> None:
        self.__run_command(
            self.__server_connection, "findConfigFilePath", config_file_name
        )

    def show_versions(self: "BBClient") -> None:
        self.__run_command(self.__server_connection, "showVersions")

    def show_environment_target(self: "BBClient", package_name: str = "") -> None:
        self.__run_command(
            self.__server_connection, "showEnvironmentTarget", package_name
        )

    def show_environment(self: "BBClient", bb_file_name: str) -> None:
        self.__run_command(self.__server_connection, "showEnvironment", bb_file_name)

    def parse_files(self: "BBClient") -> None:
        self.__run_command(self.__server_connection, "parseFiles")

    def compare_revisions(self: "BBClient") -> None:
        self.__run_command(self.__server_connection, "compareRevisions")

    def trigger_event(self: "BBClient", evene_name: str) -> None:
        self.__run_command(self.__server_connection, "triggerEvent", evene_name)

    def reset_cooker(self: "BBClient") -> None:
        self.__run_command(self.__server_connection, "resetCooker")

    def client_complete(self: "BBClient") -> None:
        self.__run_command(self.__server_connection, "clientComplete")

    def find_sigInfo(
        self: "BBClient",
        package_name_with_multi_config: str,
        task_name: str,
        sigs: List[str],
    ) -> None:
        self.__run_command(
            self.__server_connection,
            "findSigInfo",
            package_name_with_multi_config,
            task_name,
            sigs,
        )

    # --- private functions ---

    @staticmethod
    def __connect_server(
        server_adder: str, project_path: str
    ) -> Tuple["bb.server.xmlrpcclient.BitBakeXMLRPCServerConnection", "module"]:  # type: ignore
        # TODO: use shell not to be depends on bb modules
        sys.path.append(f"{project_path}/bitbake/lib")
        from bb.main import setup_bitbake, BitBakeConfigParameters  # type: ignore
        from bb.tinfoil import TinfoilConfigParameters  # type: ignore

        config_params: TinfoilConfigParameters = TinfoilConfigParameters(
            config_only=False, quit=2
        )
        config_params.remote_server: str = server_adder  # type: ignore
        server_connection, ui_module = setup_bitbake(config_params, [])
        ui_module.main(
            server_connection.connection, server_connection.events, config_params
        )
        return server_connection, ui_module

    @staticmethod
    def __run_command(server_connection, command: str, *params: Any) -> Optional[Any]:
        commandline: List[str] = [command]
        commandline.extend(params if params else [])
        try:
            result = server_connection.connection.runCommand(commandline)
        except:
            print("----------------------")
            print("[ERROR]")
            print(command)
            print(result)
            print("----------------------")
            return None
        return result[0]
