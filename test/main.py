#!/usr/bin/python3

from bbclient import *

import yaml
import logging
from logging import Logger, StreamHandler, getLogger
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
    logger: Logger = setup_logger()
    client: BBClient = BBClient(project_path, init_command, logger)
    client.start_server(server_adder, server_port)
    ui_handler: int = client.get_uihandler_num()
    client.set_event_mask(ui_handler, logging.DEBUG, {}, ["*"])
    client.parse_files()
    client.wait_done_async()

    # do test
    data_store_index: int = client.parse_recipe_file(path_to_sample_recipe)
    ret: Any = client.data_store_connector_cmd(data_store_index, "getVar", "FILE")
    print(ret)
    ret: Any = client.data_store_connector_cmd(data_store_index, "items")
    print(ret)
    ret: Any = client.data_store_connector_cmd(data_store_index, "keys")
    print(ret)
    #client.build_targets(["meson"], "compile")
    #client.wait_done_async()

    client.stop_server()

def setup_logger() -> Logger:
    ch = StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(name)s][%(asctime)s][%(levelname)s]: %(message)s')
    ch.setFormatter(formatter)
    logger: Logger = getLogger("bbclient")
    logger.setLevel('DEBUG')
    logger.addHandler(ch)
    return logger

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
