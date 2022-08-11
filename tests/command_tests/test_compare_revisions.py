from .common import * 
from bbclient import *

def test_compare_revisions(main_client: BBClient) -> None:
    main_client.compare_revisions()
    result: Optional[BBEventBase] = main_client.wait_done_async()
    assert isinstance(result, CommandCompletedEvent)

def test_build_file_kirkstone(kirkstone_client: BBClient) -> None:
    kirkstone_client.compare_revisions()
    result: Optional[BBEventBase] = kirkstone_client.wait_done_async()
    assert isinstance(result, CommandCompletedEvent)

def test_build_file_dunfell(dunfell_client: BBClient) -> None:
    dunfell_client.compare_revisions()
    result: Optional[BBEventBase] = dunfell_client.wait_done_async()
    assert isinstance(result, CommandCompletedEvent)