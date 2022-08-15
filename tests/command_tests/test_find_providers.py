from .common import *
from bbclient import *

def test_find_files_matching_in_dir_main(main_client: BBClient) -> None:
    __test_impl(main_client)
    
def test_find_config_files_kirkstone(kirkstone_client: BBClient) -> None:
    __test_impl(kirkstone_client)

def test_find_config_files_dunfell(dunfell_client: BBClient) -> None:
    __test_impl(dunfell_client)

def __test_impl(client: BBClient) -> None:
    ret: List[FindProvidersResult] = client.find_providers()
    assert ret is not None
    assert len(ret) != 0
