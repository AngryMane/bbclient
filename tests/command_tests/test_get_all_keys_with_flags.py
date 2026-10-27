from .common import * 
from bbclient import *

params = [
    ([],),
    (["doc"],),
    (["doc", "dummy"],)
]

@pytest.mark.parametrize("flags", params)
def test_generate_targets_tree_wrynose(wrynose_client: BBClient, flags: List[str]) -> None:
    __test_impl(wrynose_client, flags)

@pytest.mark.parametrize("flags", params)
def test_generate_targets_tree_scarthgap(scarthgap_client: BBClient, flags: List[str]) -> None:
    __test_impl(scarthgap_client, flags)

def __test_impl(client: BBClient, flags: List[str]) -> None:
    ret: List[getAllKeysWithFlagsResult] = client.get_all_keys_with_flags(flags)
    assert ret is not None