from .common import * 
from bbclient import *

params = [
    ("busybox"),
]

@pytest.mark.parametrize("target", params)
def test_get_file_appends_main(main_client: BBClient, target: str) -> None:
    __test_impl(main_client, target)

@pytest.mark.parametrize("target", params)
def test_get_file_appends_kirkstone(kirkstone_client: BBClient, target: str) -> None:
    __test_impl(kirkstone_client, target)

@pytest.mark.parametrize("target", params)
def test_get_file_appends_dunfell(dunfell_client: BBClient, target: str) -> None:
    __test_impl(dunfell_client, target)

def __test_impl(client: BBClient, target: str) -> None:
    ret: List[str] = client.find_best_provider(target)
    target_recipe_file_path: str = ret[3]
    ret: List[getAllKeysWithFlagsResult] = client.get_file_appends(target_recipe_file_path)
    assert ret is not None
    assert len(ret) != 0