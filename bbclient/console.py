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
    if not config.subcommand:
        print("bbclient command needs subcommand. See bbclient --help.")
        return 
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

    get_variable_subcommand: ArgumentParser = sub_parsers.add_parser("get_variable", help="Get variable value.")
    get_variable_subcommand.add_argument("name", help="variable name")
    get_variable_subcommand.add_argument("-e", "--expand",  default=True, help="Whether to expand references to other variables. Defaults to True.")
    get_variable_subcommand.set_defaults(subcommand=get_variable)

    match_file_subcommand: ArgumentParser = sub_parsers.add_parser("match_file", help="Search file by regex.")
    match_file_subcommand.add_argument("file_path_regex", help="search regex pattern")
    match_file_subcommand.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    match_file_subcommand.set_defaults(subcommand=match_file)

    get_layer_priorities_subcommand: ArgumentParser = sub_parsers.add_parser("get_layer_priorities", help="Get name, path, priority of all layers.")
    get_layer_priorities_subcommand.set_defaults(subcommand=get_layer_priorities)

    get_recipes_subcommand: ArgumentParser = sub_parsers.add_parser("get_recipes", help="Get all package name from cache.")
    get_recipes_subcommand.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_recipes_subcommand.set_defaults(subcommand=get_recipes)

    get_recipe_depends_subcommand: ArgumentParser = sub_parsers.add_parser("get_recipe_depends", help="Get recipe depends.")
    get_recipe_depends_subcommand.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_recipe_depends_subcommand.set_defaults(subcommand=get_recipe_depends)

    get_recipe_versions_subcommand: ArgumentParser = sub_parsers.add_parser("get_recipe_versions", help="Get all recipe versions.")
    get_recipe_versions_subcommand.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_recipe_versions_subcommand.set_defaults(subcommand=get_recipe_versions)

    get_recipe_provides_subcommand: ArgumentParser = sub_parsers.add_parser("get_recipe_provides", help="Get all recipe files and its packages.")
    get_recipe_provides_subcommand.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_recipe_provides_subcommand.set_defaults(subcommand=get_recipe_provides)

    get_recipe_packages_subcommand: ArgumentParser = sub_parsers.add_parser("get_recipe_packages", help="Get all recipe files and its recipe files.")
    get_recipe_packages_subcommand.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_recipe_packages_subcommand.set_defaults(subcommand=get_recipe_packages)

    get_recipe_packages_dynamic_subcommand: ArgumentParser = sub_parsers.add_parser("get_recipe_packages_dynamic", help="Get all recipe files that provides PACKAGE_DYNAMIC and its PACKAGE_DYNAMIC.")
    get_recipe_packages_dynamic_subcommand.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_recipe_packages_dynamic_subcommand.set_defaults(subcommand=get_recipe_packages_dynamic)

    get_r_providers_subcommand: ArgumentParser = sub_parsers.add_parser("get_r_providers", help="Get alias of PN and its recipe files.")
    get_r_providers_subcommand.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_r_providers_subcommand.set_defaults(subcommand=get_r_providers)

    get_runtime_depends_subcommand: ArgumentParser = sub_parsers.add_parser("get_runtime_depends", help="Get all runtime dependency by all recipe files.")
    get_runtime_depends_subcommand.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_runtime_depends_subcommand.set_defaults(subcommand=get_runtime_depends)

    get_runtime_recommends_subcommand: ArgumentParser = sub_parsers.add_parser("get_runtime_recommends", help="Get all runtime recoomends(=weak depends) by all recipe files.")
    get_runtime_recommends_subcommand.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_runtime_recommends_subcommand.set_defaults(subcommand=get_runtime_recommends)

    get_recipe_inherits_subcommands: ArgumentParser = sub_parsers.add_parser("get_recipe_inherits", help="Get recipes and its inherit recipes.")
    get_recipe_inherits_subcommands.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_recipe_inherits_subcommands.set_defaults(subcommand=get_recipe_inherits)
    
    get_bb_file_priority_subcommands: ArgumentParser = sub_parsers.add_parser("get_bb_file_priority", help="Get recipe files and its priority.")
    get_bb_file_priority_subcommands.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_bb_file_priority_subcommands.set_defaults(subcommand=get_bb_file_priority)

    get_default_preference_subcommands: ArgumentParser = sub_parsers.add_parser("get_default_preference", help="Get recipes and default preference.")
    get_default_preference_subcommands.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_default_preference_subcommands.set_defaults(subcommand=get_default_preference)

    get_skipped_recipes_subcommands: ArgumentParser = sub_parsers.add_parser("get_skipped_recipes", help="Get skipped recipes and its reasons, provides, alias.")
    get_skipped_recipes_subcommands.set_defaults(subcommand=get_skipped_recipes)

    get_file_appends_subcommands: ArgumentParser = sub_parsers.add_parser("get_file_appends", help="Get append files.")
    get_file_appends_subcommands.add_argument("file_path", help="recipe file path")
    get_file_appends_subcommands.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_file_appends_subcommands.set_defaults(subcommand=get_file_appends)

    get_all_appends_subcommands: ArgumentParser = sub_parsers.add_parser("get_all_appends", help="Get all append recipes.")
    get_all_appends_subcommands.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    get_all_appends_subcommands.set_defaults(subcommand=get_all_appends)

    find_providers_subcommands: ArgumentParser = sub_parsers.add_parser("find_providers", help="Get latest packages versions, prefered package versions, and whether there is an REQUIRED_VERSION.")
    find_providers_subcommands.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    find_providers_subcommands.set_defaults(subcommand=find_providers)

    find_best_provider_subcommands: ArgumentParser = sub_parsers.add_parser("find_best_provider", help="Get best provider infos.")
    find_best_provider_subcommands.add_argument("package_name", help="a package name you want to know the detail of best provider")
    find_best_provider_subcommands.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    find_best_provider_subcommands.set_defaults(subcommand=find_best_provider)

    all_providers_subcommands: ArgumentParser = sub_parsers.add_parser("all_providers", help="Get all providers versions and recipe file path.")
    all_providers_subcommands.add_argument("-m", "--mutli_conf_name",  default="", help="target multi-config. Defaults to ''")
    all_providers_subcommands.set_defaults(subcommand=all_providers)


    args: Namespace = parser.parse_args()

    # TODO: support remote server
    server_adder: str = "localhost"
    return Config(args.project_path, server_adder, args.port, getattr(args, "subcommand", None), args)


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

def get_variable(
    client: "BBClient", args: Namespace
) -> None:
    ret: str = client.get_variable(args.name, args.expand)
    print(ret)

def match_file(
    client: "BBClient", args: Namespace
) -> None:
    print("NOTE: This command can't run normaly because of bitbake bug. See https://angrymane.github.io/bbclient/bbclient.html#bbclient.bbclient.BBClient.match_file.")
    #ret: str = client.match_file(args.file_path_regex, args.mutli_conf_name)
    #print(ret)

def get_layer_priorities(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[GetLayerPrioritiesResult] = client.get_layer_priorities()
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_recipes(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[GetRecipesResult] = client.get_recipes(args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_recipe_depends(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[GetRecipeDependsResult] = client.get_recipe_depends(args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_recipe_versions(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[GetRecipeVersionsResult] = client.get_recipe_versions(args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_recipe_provides(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[GetRecipeProvidesResult] = client.get_recipe_provides(args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_recipe_packages(
    client: "BBClient", args: Namespace
) -> None:
    print("NOTE: This command can't run normaly because of bitbake bug. See https://angrymane.github.io/bbclient/bbclient.html#bbclient.bbclient.BBClient.get_recipe_packages.")
    #ret: List[GetRecipePackagesResult] = client.get_recipe_packages(args.mutli_conf_name)
    #json_str = json.dumps(ret, cls=JsonEncoder)
    #print(json_str)

def get_recipe_packages_dynamic(
    client: "BBClient", args: Namespace
) -> None:
    print("NOTE: This command can't run normaly because of bitbake bug. See https://angrymane.github.io/bbclient/bbclient.html#bbclient.bbclient.BBClient.get_recipe_packages_dynamic.")
    #ret: List[GetRecipePackagesDynamicResult] = client.get_recipe_packages_dynamic(args.mutli_conf_name)
    #json_str = json.dumps(ret, cls=JsonEncoder)
    #print(json_str)

def get_r_providers(
    client: "BBClient", args: Namespace
) -> None:
    print("NOTE: This command can't run normaly because of bitbake bug. See https://angrymane.github.io/bbclient/bbclient.html#bbclient.bbclient.BBClient.get_r_providers.")
    #ret: List[GetRProvidersResult] = client.get_r_providers(args.mutli_conf_name)
    #json_str = json.dumps(ret, cls=JsonEncoder)
    #print(json_str)

def get_runtime_depends(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[GetRuntimeDependsResult] = client.get_runtime_depends(args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_runtime_recommends(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[GetRuntimeRecommendsResult] = client.get_runtime_recommends(args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_recipe_inherits(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[GetRecipeInheritsResult] = client.get_recipe_inherits(args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_bb_file_priority(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[GetBbFilePriorityResult] = client.get_bb_file_priority(args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_default_preference(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[GetDefaultPreferenceResult] = client.get_default_preference(args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_skipped_recipes(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[GetSkippedRecipesResult] = client.get_skipped_recipes()
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_file_appends(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[str] = client.get_file_appends(args.file_path, args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_all_appends(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[GetAllAppendsResult] = client.get_all_appends(args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def find_providers(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[FindProvidersResult] = client.find_providers(args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def find_best_provider(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[str] = client.find_best_provider(args.package_name, args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def all_providers(
    client: "BBClient", args: Namespace
) -> None:
    ret: List[AllProvidersResult] = client.all_providers(args.mutli_conf_name)
    json_str = json.dumps(ret, cls=JsonEncoder)
    print(json_str)

def get_runtime_providers(
    client: "BBClient", args: Namespace
) -> None:
    # TODO
    pass

def data_store_connector_cmd(
    client: "BBClient", args: Namespace
) -> None:
    # TODO
    pass

def data_store_connector_varhist_cmd(
    client: "BBClient", args: Namespace
) -> None:
    # TODO
    pass

"""
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
def find_config_file_path(self: "BBClient", config_file_name: str) -> None:
def show_versions(self: "BBClient") -> None:
def show_environment_target(self: "BBClient", package_name: str = "") -> None:
def show_environment(self: "BBClient", bb_file_path: str) -> None:
def parse_files(self: "BBClient") -> None:

def compare_revisions(self: "BBClient") -> None:
"""
