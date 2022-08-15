from .common import *
from bbclient import *

def test_get_uihandler_num_main(main_client: BBClient) -> None:
    __test_impl(main_client)

def test_get_uihandler_num_kirkstone(kirkstone_client: BBClient) -> None:
    __test_impl(kirkstone_client)

def test_get_uihandler_num_dunfell(dunfell_client: BBClient) -> None:
    __test_impl(dunfell_client)

def __test_impl(client: BBClient) -> None:
    ret: int = client.get_uihandler_num()
    assert ret == 1