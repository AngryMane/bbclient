#!/usr/bin/python3

from gettext import find
from bbclient import *

import yaml
import logging
from typing import Optional, Any, List
from time import sleep
from typing import Tuple

YML_KEY_BB_PROJECT_ABS_PATH: str = "bb_project_abs_path"
YML_KEY_SERVER_ADDER: str = "server_adder"
YML_KEY_SERVER_PORT: str = "server_port"
YML_KEY_INIT_COMMAND: str = "init_command"
YML_KEY_PATH_TO_SAMPLE_RECIPE: str = "path_to_sample_recipe"


def main() -> None:
    project_path, server_adder, server_port, init_command, path_to_sample_recipe = load_test_settings(
        "./test.yml"
    )
    client: BBClient = BBClient(project_path, init_command)
    client.start_server(server_adder, server_port)

    typical_setup(client, logging.DEBUG)

    # do test
    client.generate_targets_tree("", ["gcc"])
    ret: Any = client.wait_event(["bb.event.ReachableStamps"])
    print(ret.__dict__)

    client.stop_server()


def typical_setup(client: BBClient, log_level: int) -> None:
    ret = client.get_uihandler_num()
    client.set_event_mask(
        ret, log_level, {"": 0}, ["*"]
    )  # mask unnecessary logging info
    ret = client.parse_configuration()
    ret = client.parse_files()
    # wainting for parse files
    # TODO: use client.get_event
    sleep(3)


def get_class_name(obj: Any) -> str:
    return str(type(obj))[8:-2]


def load_test_settings(yml_file_path: str) -> Tuple[str, str, int]:
    with open(yml_file_path) as yml_file:
        yml_content = yaml.safe_load(yml_file)
        return (
            yml_content[YML_KEY_BB_PROJECT_ABS_PATH],
            yml_content[YML_KEY_SERVER_ADDER],
            int(yml_content[YML_KEY_SERVER_PORT]),
            yml_content[YML_KEY_INIT_COMMAND],
            yml_content[YML_KEY_PATH_TO_SAMPLE_RECIPE],
        )


if __name__ == "__main__":
    main()
