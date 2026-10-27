from .common import *
from bbclient import *

def test_get_uihandler_num_wrynose(wrynose_client: BBClient) -> None:
    __test_impl(wrynose_client)

def test_get_uihandler_num_scarthgap(scarthgap_client: BBClient) -> None:
    __test_impl(scarthgap_client)

def __test_impl(client: BBClient) -> None:
    variable_name: str = "MACHINE"
    ret: str = client.get_variable(variable_name)
    assert ret is not None