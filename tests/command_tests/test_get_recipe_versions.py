from .common import * 
from bbclient import *

def test_get_recipe_versions_wrynose(wrynose_client: BBClient) -> None:
    __test_impl(wrynose_client)

def test_get_recipe_versions_scarthgap(scarthgap_client: BBClient) -> None:
    __test_impl(scarthgap_client)

def __test_impl(client: BBClient) -> None:
    ret: List[GetRecipeVersionsResult] = client.get_recipe_versions()
    assert ret is not None
    assert len(ret) != 0