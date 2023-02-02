#!/usr/bin/python3

from bbclient import *

def main() -> None:
    project_path: str = "tests/dunfell"
    init_command: str = ". oe-init-build-env"
    client: BBClient = BBClient(project_path, init_command)
    client.start_server()
    client.build_targets(["curl"], "compile")
    client.stop_server()

if __name__ == "__main__":
    main()
