from .common import * 
from bbclient import *

def test_all_providers_main(main_client: BBClient) -> None:
    ret: List[AllProvidersResult] = main_client.all_providers()
    assert ret is not None

def test_all_providers_kirkstone(kirkstone_client: BBClient) -> None:
    ret: List[AllProvidersResult] = kirkstone_client.all_providers()
    assert ret is not None

def test_all_providers_dunfell(dunfell_client: BBClient) -> None:
    ret: List[AllProvidersResult] = dunfell_client.all_providers()
    assert ret is not None