from .common import * 
from bbclient import *

def test_client_complete(main_client: BBClient) -> None:
    main_client.client_complete()
    result: Optional[BBEventBase] = main_client.wait_done_async()
    assert isinstance(result, CommandCompletedEvent)

def test_build_targets_kirkstone(kirkstone_client: BBClient) -> None:
    kirkstone_client.client_complete()
    result: Optional[BBEventBase] = kirkstone_client.wait_done_async()
    assert isinstance(result, CommandCompletedEvent)

def test_build_targets_dunfell(dunfell_client: BBClient) -> None:
    dunfell_client.client_complete()
    result: Optional[BBEventBase] = dunfell_client.wait_done_async()
    assert isinstance(result, CommandCompletedEvent)
