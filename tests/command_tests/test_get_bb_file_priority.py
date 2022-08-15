from .common import * 
from bbclient import *

def test_get_bb_file_priority_main(main_client: BBClient) -> None:
    __test_impl(main_client)

def test_get_bb_file_priority_kirkstone(kirkstone_client: BBClient) -> None:
    __test_impl(kirkstone_client)

def test_get_bb_file_priority_dunfell(dunfell_client: BBClient) -> None:
    __test_impl(dunfell_client)

def __test_impl(client: BBClient) -> None:
    ret: List[GetBbFilePriorityResult] = client.get_bb_file_priority()
    assert ret is not None
    assert len(ret) != 0