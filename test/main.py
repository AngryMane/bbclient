#!/usr/bin/python3

from bbclient.bbclient import BBClient

import yaml
from time import sleep
from typing import Tuple

YML_KEY_BB_PROJECT_ABS_PATH: str = "bb_project_abs_path"
YML_KEY_SERVER_ADDER: str = "server_adder"
YML_KEY_SERVER_PORT: str = "server_port"
YML_KEY_INIT_COMMAND: str = "init_command"


def main() -> None:
    project_path, server_adder, server_port, init_command = load_test_settings(
        "./test.yml"
    )
    client: BBClient = BBClient(project_path, init_command)
    client.start_server(server_adder, server_port)

    ret = client.parse_configuration()
    ret = client.parse_files()
    sleep(3)  # wainting for parse files

    # ret = client.data_store_connector_cmd(ret["dsindex"], "getVar", "FILE")
    # print(f"data_store_connector_cmd: {ret}")
    # ret = client.find_best_provider("gcc")
    # print(f"find_best_provider: {ret}")
    # ret = client.get_overlayed_recipes()
    # print(f"get_overlayed_recipes: {ret}")
    # ret = client.get_variable("FILE")
    # print(f"get_variable: {ret}")
    # ret = client.get_skipped_recipes()
    # print(f"get_skipped_recipes: {ret}")
    # ret = client.show_environment_target()
    # print(f"show_environment_target: {ret}")
    # ret = client.get_layer_priorities()
    # print(f"get_layer_priorities: {ret}")
    # ret = client.get_recipes()
    # print(f"get_recipes: {len(ret)}")
    # ret = client.get_r_providers()
    # print(f"get_r_providers: {ret}")
    # ret = client.find_sigInfo("", "bulid", [])
    # print(f"find_sigInfo: {ret}")
    ret = client.get_all_keys_with_flags([])
    print(f"get_all_keys_with_flags: {ret}")

    client.stop_server()


def load_test_settings(yml_file_path: str) -> Tuple[str, str, int]:
    with open(yml_file_path) as yml_file:
        yml_content = yaml.safe_load(yml_file)
        return (
            yml_content[YML_KEY_BB_PROJECT_ABS_PATH],
            yml_content[YML_KEY_SERVER_ADDER],
            int(yml_content[YML_KEY_SERVER_PORT]),
            yml_content[YML_KEY_INIT_COMMAND],
        )


if __name__ == "__main__":
    main()
