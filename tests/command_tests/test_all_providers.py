from .common import * 
from bbclient import *

def test_all_providers_main(main_client: BBClient) -> None:
    __test_imple(main_client)

def test_all_providers_kirkstone(kirkstone_client: BBClient) -> None:
    __test_imple(kirkstone_client)

def test_all_providers_dunfell(dunfell_client: BBClient) -> None:
    __test_imple(dunfell_client)

def __test_imple(client: BBClient) -> None:
    ret: List[AllProvidersResult] = client.all_providers()
    assert ret is not None