from .common import * 
from bbclient import *

params = [
    ([],),
    (["doc"],),
    (["doc", "dummy"],)
]

@pytest.mark.parametrize("flags", params)
def test_get_all_keys_with_flags(main_client: BBClient, flags: List[str]) -> None:
    ret: List[getAllKeysWithFlagsResult] = main_client.get_all_keys_with_flags(flags)
    assert ret is not None