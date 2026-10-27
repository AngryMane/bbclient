from .common import * 
from bbclient import *

def test_all_providers_wrynose(wrynose_client: BBClient) -> None:
    __test_imple(wrynose_client)

def test_all_providers_scarthgap(scarthgap_client: BBClient) -> None:
    __test_imple(scarthgap_client)

def __test_imple(client: BBClient) -> None:
    ret: List[AllProvidersResult] = client.all_providers()
    assert ret is not None