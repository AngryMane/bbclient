from .common import *
from bbclient import *

def test_get_uihandler_num_wrynose(wrynose_client: BBClient) -> None:
    __test_impl(wrynose_client)

def test_get_uihandler_num_scarthgap(scarthgap_client: BBClient) -> None:
    __test_impl(scarthgap_client)

def __test_impl(client: BBClient) -> None:
    ret: int = client.get_uihandler_num()
    # ui handler num is a sequence number in bitbake server, so it depends on how many UIs connected before.
    assert isinstance(ret, int)
    assert ret >= 1