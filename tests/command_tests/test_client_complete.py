from .common import * 
from bbclient import *

def test_client_complete(main_client: BBClient) -> None:
    __test_imple(main_client)

def test_build_targets_kirkstone(kirkstone_client: BBClient) -> None:
    __test_imple(kirkstone_client)

def test_build_targets_dunfell(dunfell_client: BBClient) -> None:
    __test_imple(dunfell_client)

def __test_imple(client: BBClient) -> None:
    client.client_complete()
    result: Optional[BBEventBase] = client.wait_done_async()
    assert isinstance(result, CommandCompletedEvent)
