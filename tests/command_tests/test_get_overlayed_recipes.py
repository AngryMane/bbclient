from .common import * 
from bbclient import *

def test_get_overlayed_recipes_wrynose(wrynose_client: BBClient) -> None:
    __test_impl(wrynose_client)

def test_get_overlayed_recipes_scarthgap(scarthgap_client: BBClient) -> None:
    __test_impl(scarthgap_client)

def __test_impl(client: BBClient) -> None:
    ret: Any = client.get_overlayed_recipes()
    # TODO: assert