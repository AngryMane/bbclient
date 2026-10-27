from .common import *
from bbclient import *

def test_find_files_matching_in_dir_wrynose(wrynose_client: BBClient) -> None:
    __test_impl(wrynose_client)
    
def test_find_config_files_scarthgap(scarthgap_client: BBClient) -> None:
    __test_impl(scarthgap_client)

def __test_impl(client: BBClient) -> None:
    ret: List[FindProvidersResult] = client.find_providers()
    assert ret is not None
    assert len(ret) != 0
