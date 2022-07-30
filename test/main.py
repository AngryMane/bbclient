#!/usr/bin/python3

from bbclient.bbclient import BBClient

import yaml
import logging
from typing import Optional, Any
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

    typical_setup(client, logging.DEBUG)

    # do test
    client.show_versions()

    sleep(5)

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


def wait_event(client: BBClient, class_name: str) -> Optional[Any]:
    count: int = 0
    while count < 3000:
        ret: Optional[Any] = client.get_event(0.03)
        # if type(ret) == f"<class '{class_name}'>":
        if not ret:
            count = count + 1
        elif get_class_name(ret) == class_name:
            return ret
        else:
            count = 0
        sleep(0.01)
    return None


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
        )


if __name__ == "__main__":
    main()
