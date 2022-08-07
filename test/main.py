#!/usr/bin/python3

from bbclient import *

import yaml
import logging
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
    ui_handler: int = client.get_uihandler_num()
    client.set_event_mask(ui_handler, logging.DEBUG, {}, ["*"])
    client.parse_files()
    client.wait_done_async()

    # do test
    client.build_targets(["busybox"], "fetch")
    client.wait_done_async() # please confirm there is no previous async command that you didn't do wait_done_async.
    client.build_targets(["busybox"], "patch")
    client.wait_done_async() # please confirm there is no previous async command that you didn't do wait_done_async.

    client.stop_server()


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
