from distutils.cmd import Command
from .common import *
from bbclient import *

def test_parse_files_main(main_client: BBClient) -> None:
    __test_impl(main_client)
    
def test_parse_files_kirkstone(kirkstone_client: BBClient) -> None:
    __test_impl(kirkstone_client)

def test_parse_files_dunfell(dunfell_client: BBClient) -> None:
    __test_impl(dunfell_client)

def __test_impl(client: BBClient) -> None:
    callback_monitors: List[CallbackMonitor] = []
    callback_ids: List[int] = []
    for expect_event_type in [ReachableStampsEvent]:
        callback_monitor: CallbackMonitor = CallbackMonitor()
        callback_monitors.append(callback_monitor)
        callback_id: int = client.register_callback(expect_event_type, callback_monitor.callback)
        callback_ids.append(callback_id)
    client.parse_files()
    for monitor in callback_monitors:
        assert monitor.is_callback
    for id in callback_ids:
        client.unregister_callback(id)