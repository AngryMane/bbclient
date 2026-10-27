#!/usr/bin/python3

from bbclient import *

import os
import logging
import pytest
import logging


CUR_FILE_PATH: str = os.path.dirname(__file__)
INIT_COMMAND: str = ". oe-init-build-env"
# wrynose has no poky repository, so add the layers poky used to include.
WRYNOSE_INIT_COMMAND: str = INIT_COMMAND + " && bitbake-layers add-layer ../../meta-yocto/meta-poky ../../meta-yocto/meta-yocto-bsp"

class CallbackMonitor:
    def __init__(self: "CallbackMonitor"):
        self.is_callback: bool = False
        self.event: Optional[BBEventBase] = None

    def callback(self: "CallbackMonitor", _: BBClient, event: BBEventBase):
        self.is_callback = True
        self.event = event

@pytest.fixture(scope="module")
def scarthgap_client():
    PATH_TO_SCARTHGAP = CUR_FILE_PATH + "/../scarthgap"
    client: BBClient = BBClient(PATH_TO_SCARTHGAP, INIT_COMMAND)
    client.start_server()
    client.parse_files()
    yield client
    client.stop_server()

@pytest.fixture(scope="module")
def wrynose_client():
    PATH_TO_WRYNOSE = CUR_FILE_PATH + "/../wrynose/openembedded-core"
    client: BBClient = BBClient(PATH_TO_WRYNOSE, WRYNOSE_INIT_COMMAND)
    client.start_server()
    client.parse_files()
    yield client
    client.stop_server()
