from .common import * 
from bbclient import *

def test_get_overlayed_recipes_main(main_client: BBClient) -> None:
    __test_impl(main_client)

def test_get_overlayed_recipes_kirkstone(kirkstone_client: BBClient) -> None:
    __test_impl(kirkstone_client)

def test_get_overlayed_recipes_dunfell(dunfell_client: BBClient) -> None:
    __test_impl(dunfell_client)

def __test_impl(client: BBClient) -> None:
    ret: Any = client.get_overlayed_recipes()
    # TODO: assert