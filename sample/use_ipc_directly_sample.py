#!/usr/bin/python3

from bbclient import *

def main() -> None:
    project_path: str = "tests/dunfell"
    init_command: str = ". oe-init-build-env"
    client: BBClient = BBClient(project_path, init_command)
    client.start_server()

    def monitor(bbclient_:BBClient, event: ProcessProgressEvent):
        print(event.pid)
        print(event.processname)
        print(event.progress)
    callback_index:int = client.register_callback(ProcessProgressEvent, monitor)
    client.build_targets(["alsa"], "compile")
    client.unregister_callback(callback_index)

    client.stop_server()

if __name__ == "__main__":
    main()
