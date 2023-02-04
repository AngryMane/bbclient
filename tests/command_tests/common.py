#!/usr/bin/python3

from bbclient import *

import os
import logging
import pytest
import logging


CUR_FILE_PATH: str = os.path.dirname(__file__)
INIT_COMMAND: str = ". oe-init-build-env"

class CallbackMonitor:
    def __init__(self: "CallbackMonitor"):
        self.is_callback: bool = False
        self.event: Optional[BBEventBase] = None

    def callback(self: "CallbackMonitor", _: BBClient, event: BBEventBase):
        self.is_callback = True
        self.event = event

@pytest.fixture(scope="module")
def main_client():
    PATH_TO_MAIN = CUR_FILE_PATH + "/../main"
    client: BBClient = BBClient(PATH_TO_MAIN, INIT_COMMAND)
    client.start_server()
    client.parse_files()
    yield client
    client.stop_server()

@pytest.fixture(scope="module")
def kirkstone_client():
    PATH_TO_KIRKSTONE = CUR_FILE_PATH + "/../kirkstone"
    client: BBClient = BBClient(PATH_TO_KIRKSTONE, INIT_COMMAND)
    client.start_server()
    client.parse_files()
    yield client
    client.stop_server()

@pytest.fixture(scope="module")
def dunfell_client():
    PATH_TO_DUNFELL = CUR_FILE_PATH + "/../dunfell"
    client: BBClient = BBClient(PATH_TO_DUNFELL, INIT_COMMAND)
    client.start_server()
    client.parse_files()
    yield client
    client.stop_server()
