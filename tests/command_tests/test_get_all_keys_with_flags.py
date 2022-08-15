from .common import * 
from bbclient import *

params = [
    ([],),
    (["doc"],),
    (["doc", "dummy"],)
]

@pytest.mark.parametrize("flags", params)
def test_generate_targets_tree_main(main_client: BBClient, flags: List[str]) -> None:
    __test_impl(main_client, flags)

@pytest.mark.parametrize("flags", params)
def test_generate_targets_tree_kirkstone(kirkstone_client: BBClient, flags: List[str]) -> None:
    __test_impl(kirkstone_client, flags)

@pytest.mark.parametrize("flags", params)
def test_generate_targets_tree_dunfell(dunfell_client: BBClient, flags: List[str]) -> None:
    __test_impl(dunfell_client, flags)

def __test_impl(client: BBClient, flags: List[str]) -> None:
    ret: List[getAllKeysWithFlagsResult] = client.get_all_keys_with_flags(flags)
    assert ret is not None