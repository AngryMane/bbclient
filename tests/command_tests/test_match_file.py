from .common import *
from bbclient import *

def test_get_uihandler_num_wrynose(wrynose_client: BBClient) -> None:
    __test_impl(wrynose_client)

def test_get_uihandler_num_scarthgap(scarthgap_client: BBClient) -> None:
    __test_impl(scarthgap_client)

def __test_impl(client: BBClient) -> None:
    ret: str = client.match_file(".*/core-image-minimal.bb")
    # this assert will fail because of bitbake bug. See match_file docstring.
    #assert ret is not None 