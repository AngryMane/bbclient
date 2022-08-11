from .common import *
from bbclient import *

def test_match_file(main_client: BBClient) -> None:
    ret: str = main_client.match_file(".*/core-image-minimal.bb")
    assert ret is not None # this assert will fail because of bitbake bug. See match_file docstring.