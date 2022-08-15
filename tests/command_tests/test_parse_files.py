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
    client.parse_files()
    ret: Optional[BBEventBase] = client.wait_event([ReachableStampsEvent])
    assert isinstance(ret, ReachableStampsEvent)
    ret: Optional[BBEventBase] = client.wait_done_async()
    assert isinstance(ret, CommandCompletedEvent)