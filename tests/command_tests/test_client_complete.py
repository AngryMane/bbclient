from .common import * 
from bbclient import *

def test_client_complete_main(main_client: BBClient) -> None:
    __test_imple(main_client)

def test_client_complete_kirkstone(kirkstone_client: BBClient) -> None:
    __test_imple(kirkstone_client)

def test_client_complete_dunfell(dunfell_client: BBClient) -> None:
    __test_imple(dunfell_client)

def __test_imple(client: BBClient) -> None:
    callback_monitor: CallbackMonitor = CallbackMonitor()
    callback_id: int = client.register_callback(CommandCompletedEvent, callback_monitor.callback)
    client.client_complete()
    client.unregister_callback(callback_id)
    assert callback_monitor.is_callback
