from .common import * 
from bbclient import *

def test_client_complete_wrynose(wrynose_client: BBClient) -> None:
    __test_imple(wrynose_client)

def test_client_complete_scarthgap(scarthgap_client: BBClient) -> None:
    __test_imple(scarthgap_client)

def __test_imple(client: BBClient) -> None:
    callback_monitor: CallbackMonitor = CallbackMonitor()
    callback_id: int = client.register_callback(CommandCompletedEvent, callback_monitor.callback)
    client.client_complete()
    client.unregister_callback(callback_id)
    assert callback_monitor.is_callback
