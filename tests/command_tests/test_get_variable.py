from .common import *
from bbclient import *

def test_get_uihandler_num_main(main_client: BBClient) -> None:
    __test_impl(main_client)

def test_get_uihandler_num_kirkstone(kirkstone_client: BBClient) -> None:
    __test_impl(kirkstone_client)

def test_get_uihandler_num_dunfell(dunfell_client: BBClient) -> None:
    __test_impl(dunfell_client)

def __test_impl(client: BBClient) -> None:
    variable_name: str = "MACHINE"
    ret: str = client.get_variable(variable_name)
    assert ret is not None