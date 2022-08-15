#!/usr/bin/python3

from bbclient import *

import os
import logging
import pytest
from logging import Logger, StreamHandler, getLogger


CUR_FILE_PATH: str = os.path.dirname(__file__)
SERVER_ADDR: str = "localhost"
INIT_COMMAND: str = ". oe-init-build-env"

@pytest.fixture(scope="module")
def main_client():
    PATH_TO_MAIN = CUR_FILE_PATH + "/../main"
    client: BBClient = BBClient(PATH_TO_MAIN, INIT_COMMAND, None)
    client.start_server(SERVER_ADDR, 8082)
    ui_handler: int = client.get_uihandler_num()
    client.set_event_mask(ui_handler, logging.WARNING, {}, ["*"])
    client.parse_files()
    client.wait_done_async()
    yield client
    client.stop_server()

@pytest.fixture(scope="module")
def kirkstone_client():
    PATH_TO_KIRKSTONE = CUR_FILE_PATH + "/../kirkstone"
    client: BBClient = BBClient(PATH_TO_KIRKSTONE, INIT_COMMAND, None)
    client.start_server(SERVER_ADDR, 8083)
    ui_handler: int = client.get_uihandler_num()
    client.set_event_mask(ui_handler, logging.WARNING, {}, ["*"])
    client.parse_files()
    client.wait_done_async()
    yield client
    client.stop_server()

@pytest.fixture(scope="module")
def dunfell_client():
    PATH_TO_DUNFELL = CUR_FILE_PATH + "/../dunfell"
    client: BBClient = BBClient(PATH_TO_DUNFELL, INIT_COMMAND, None)
    client.start_server(SERVER_ADDR, 8084)
    ui_handler: int = client.get_uihandler_num()
    client.set_event_mask(ui_handler, logging.WARNING, {}, ["*"])
    client.parse_files()
    client.wait_done_async()
    yield client
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
