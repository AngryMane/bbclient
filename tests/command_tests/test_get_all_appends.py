from .common import *
from bbclient import *

def test_get_all_appends_wrynose(wrynose_client: BBClient) -> None:
    __test_impl(wrynose_client)

def test_get_all_appends_scarthgap(scarthgap_client: BBClient) -> None:
    __test_impl(scarthgap_client)

def __test_impl(client: BBClient) -> None:
    ret: List[GetAllAppendsResult] = client.get_all_appends()
    assert ret is not None
    assert len(ret) != 0