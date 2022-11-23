#!/usr/bin/env python3
""" 
This file provides cli interface of bbclient
"""

from .bbclient import *

import logging, json
from argparse import ArgumentParser, Namespace, _SubParsersAction 
from logging import Logger, StreamHandler, getLogger
from typing import List, Union

from collections import namedtuple

Config = namedtuple(
    "Config",
    ["project_path", "server_adder", "port", "subcommand", "command_args"],
)


def main() -> None:
    config: Config = get_config()
    logger: Logger = setup_logger()
    client: BBClient = BBClient(config.project_path, logger=logger)
    client.start_server(config.server_adder, config.port)
    ui_handler: int = client.get_uihandler_num()
    client.set_event_mask(ui_handler, logging.DEBUG, {}, ["*"])
    client.parse_files()
    client.wait_done_async()

    config.subcommand(client, config.command_args)

    client.stop_server()

def get_config() -> List[Union[str, int]]:
    parser: ArgumentParser = ArgumentParser(description='')
    parser.add_argument("-p", "--project_path", default="../", help="path to bitbake project, basically poky dir")
    parser.add_argument("-i", "--port", type=int, default=8081, help="server port you want to use.")

    # sub commands
    sub_parsers: _SubParsersAction = parser.add_subparsers(title='get_all_keys_with_flags', description='valid subcommands', help='additional help')
    get_all_keys_with_flags_subcommand: ArgumentParser = sub_parsers.add_parser("get_all_keys_with_flags", help="Get value, history and specified flags of all global variables.")
    get_all_keys_with_flags_subcommand.add_argument("-f", "--flags", default=[], help="Target flags. The default is [].", action='append')
    get_all_keys_with_flags_subcommand.set_defaults(subcommand=get_all_keys_with_flags_command)

    args: Namespace = parser.parse_args()

    # TODO: support remote server
    server_adder: str = "localhost"
    return Config(args.project_path, server_adder, args.port, args.subcommand, args)


def setup_logger() -> Logger:
    ch = StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(name)s][%(asctime)s][%(levelname)s]: %(message)s')
    ch.setFormatter(formatter)
    logger: Logger = getLogger("bbclient")
    logger.setLevel('DEBUG')
    logger.addHandler(ch)
    return logger

def get_all_keys_with_flags_command(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[getAllKeysWithFlagsResult] = client.get_all_keys_with_flags(args.flags)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)
    #for i in ret:
    #    print(i.name)
    #    print(i.value)
    #    print(i.histories)
    #    print(i.flags)

"""
def get_all_keys_with_flags(
    self: "BBClient", flag_list: List[str]
) -> List[getAllKeysWithFlagsResult]:
def get_variable(self: "BBClient", name: str, expand: bool = True) -> str:
def set_variable(self: "BBClient", name: str, value: str) -> None:
def get_set_variable(self: "BBClient", name: str, expand: bool = True) -> str:
def set_config(self: "BBClient", name: str, value: str) -> None:
def enable_data_tracking(self: "BBClient") -> None:
def disable_data_tracking(self: "BBClient") -> None:
def set_pre_post_conf_files(
    self: "BBClient", pre_files: str, post_files: str
) -> None:
def match_file(
    self: "BBClient", file_path_regex: str, mutli_conf_name: str = ""
) -> str:
def get_uihandler_num(self: "BBClient") -> int:
def set_event_mask(
    self: "BBClient",
    handler_num: int,
    log_level: int,
    debug_domains: Mapping[str, int],
    mask: List[str],
) -> bool:
def set_features(self: "BBClient", features: List[BBFeature]) -> None:
def update_config(
    self: "BBClient",
    options: Mapping[str, Any],
    environment: Mapping[str, str],
    command_line: str,
) -> None:
def parse_configuration(self: "BBClient") -> None:
def get_layer_priorities(self: "BBClient") -> List[GetLayerPrioritiesResult]:
def get_recipes(self: "BBClient", multi_config: str = "") -> List[GetRecipesResult]:
def get_recipe_depends(
    self: "BBClient", multi_config: str = ""
) -> List[GetRecipeDependsResult]:
def get_recipe_versions(
    self: "BBClient", multi_config: str = ""
) -> List[GetRecipeVersionsResult]:
def get_recipe_provides(
    self: "BBClient", multi_config: str = ""
) -> List[GetRecipeProvidesResult]:
def get_recipe_packages(
    self: "BBClient", multi_config: str = ""
) -> List[GetRecipePackagesResult]:
def get_recipe_packages_dynamic(
    self: "BBClient", multi_config: str = ""
) -> List[GetRecipePackagesDynamicResult]:
def get_r_providers(
    self: "BBClient", multi_config: str = ""
) -> List[GetRProvidersResult]:
def get_runtime_depends(
    self: "BBClient", multi_config: str = ""
) -> List[GetRuntimeDependsResult]:
def get_runtime_recommends(
    self: "BBClient", multi_config: str = ""
) -> List[GetRuntimeRecommendsResult]:
def get_recipe_inherits(
    self: "BBClient", multi_config: str = ""
) -> List[GetRecipeInheritsResult]:
def get_bb_file_priority(
    self: "BBClient", multi_config: str = ""
) -> List[GetBbFilePriorityResult]:
def get_default_preference(
    self: "BBClient", multi_config: str = ""
) -> List[GetDefaultPreferenceResult]:
def get_skipped_recipes(self: "BBClient") -> List[GetSkippedRecipesResult]:
def get_overlayed_recipes(self: "BBClient", multi_config: str = ""):
def get_file_appends(
    self: "BBClient", file_path: str, multi_config: str = ""
) -> List[str]:
def get_all_appends(
    self: "BBClient", multi_config: str = ""
) -> List[GetAllAppendsResult]:
def find_providers(
    self: "BBClient", multi_config: str = ""
) -> List[FindProvidersResult]:
def find_best_provider(
    self: "BBClient", package_name: str, multi_config: str = ""
) -> List[str]:
def all_providers(
    self: "BBClient", multi_config: str = ""
) -> List[AllProvidersResult]:
def get_runtime_providers(
    self: "BBClient", runtime_providers: List[str], multi_config: str = ""
):
def data_store_connector_cmd(
    self: "BBClient", datastore_index: int, command: str, *args, **kwargs
) -> Any:
def data_store_connector_varhist_cmd(
    self: "BBClient", datastore_index: int, command: str, *args, **kwargs
) -> Any:
def data_store_connector_var_hist_cmd_emit(
    self: "BBClient",
    datastore_index: int,
    variable: str,
    comment: str,
    val: str,
    override_datastore_index: int,
) -> str:
def data_store_connector_inc_hist_cmd(
    self: "BBClient", datastore_index: int, command: str, *args, **kwargs
) -> Any:
def data_store_connector_release(self: "BBClient", datastore_index: int) -> None:
def parse_recipe_file(
    self: "BBClient",
    file_path: str,
    append: bool = True,
    append_list: Optional[str] = None,
    datastore_index: Optional[int] = None,
) -> Optional[int]:
def build_file(
    self: "BBClient", file_path: str, task_name: str, internal: bool = False
) -> None:
def build_targets(
    self: "BBClient",
    targets: List[str],
    task_name: str,
) -> None:
def generate_dep_tree_event(
    self: "BBClient", targets: List[str], task_name: str
) -> None:
def generate_dot_graph(
    self: "BBClient", targets: List[str], task_name: str
) -> None:
def generate_targets_tree(
    self: "BBClient", bb_klass_file_path: str, package_names: List[str]
) -> None:
def find_config_files(self: "BBClient", variable_name: str) -> None:
def find_files_matching_in_dir(
    self: "BBClient", target_file_name_substring: str, directory: str
) -> None:
def test_cooker_command_event(self: "BBClient", pattern: str) -> None:
def find_config_file_path(self: "BBClient", config_file_name: str) -> None:
def show_versions(self: "BBClient") -> None:
def show_environment_target(self: "BBClient", package_name: str = "") -> None:
def show_environment(self: "BBClient", bb_file_path: str) -> None:
def parse_files(self: "BBClient") -> None:
def compare_revisions(self: "BBClient") -> None:
def trigger_event(self: "BBClient", evene_name: str) -> None:
def reset_cooker(self: "BBClient") -> None:
def client_complete(self: "BBClient") -> None:
def find_sigInfo(
    self: "BBClient",
    package_name_with_multi_config: str,
    task_name: str,
    sigs: List[str],
) -> None:
"""