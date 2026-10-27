from .common import * 
from bbclient import *

def test_get_recipe_depends_wrynose(wrynose_client: BBClient) -> None:
    __test_impl(wrynose_client)

def test_get_recipe_depends_scarthgap(scarthgap_client: BBClient) -> None:
    __test_impl(scarthgap_client)

def __test_impl(client: BBClient) -> None:
    ret: List[GetRecipeDependsResult] = client.get_recipe_depends()
    assert ret is not None
    assert len(ret) != 0