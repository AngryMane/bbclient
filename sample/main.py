#!/usr/bin/python3

from bbclient import *

import logging
from logging import Logger, StreamHandler, getLogger
from typing import Tuple

def main() -> None:
    
    project_path: str = "tests/dunfell"
    init_command: str = ". oe-init-build-env"
    logger: Logger = setup_logger()
    client: BBClient = BBClient(project_path, init_command, logger)
    client.start_server()
    #client.parse_files()
    client.build_targets(["curl"], "clean")
    client.build_targets(["curl"], "compile")
    client.stop_server()

def setup_logger() -> Logger:
    ch = StreamHandler()
    ch.setLevel(logging.CRITICAL)
    formatter = logging.Formatter('[%(name)s][%(asctime)s][%(levelname)s]: %(message)s')
    ch.setFormatter(formatter)
    logger: Logger = getLogger("bbclient")
    logger.setLevel('DEBUG')
    logger.addHandler(ch)
    return logger

if __name__ == "__main__":
    main()
