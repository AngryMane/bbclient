from .common import * 
from bbclient import *

def test_get_layer_priorities_main(main_client: BBClient) -> None:
    __test_impl(main_client)

def test_get_layer_priorities_kirkstone(kirkstone_client: BBClient) -> None:
    __test_impl(kirkstone_client)

def test_get_layer_priorities_dunfell(dunfell_client: BBClient) -> None:
    __test_impl(dunfell_client)

def __test_impl(client: BBClient) -> None:
    ret: List[GetLayerPrioritiesResult] = client.get_layer_priorities()
    assert ret is not None
    assert len(ret) != 0