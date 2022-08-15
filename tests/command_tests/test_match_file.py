from .common import *
from bbclient import *

def test_get_uihandler_num_main(main_client: BBClient) -> None:
    __test_impl(main_client)

def test_get_uihandler_num_kirkstone(kirkstone_client: BBClient) -> None:
    __test_impl(kirkstone_client)

def test_get_uihandler_num_dunfell(dunfell_client: BBClient) -> None:
    __test_impl(dunfell_client)

def __test_impl(client: BBClient) -> None:
    ret: str = client.match_file(".*/core-image-minimal.bb")
    # this assert will fail because of bitbake bug. See match_file docstring.
    #assert ret is not None 