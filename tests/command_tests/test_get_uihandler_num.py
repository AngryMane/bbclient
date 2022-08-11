from .common import *
from bbclient import *

def test_get_uihandler_num(main_client: BBClient) -> None:
    ret: int = main_client.get_uihandler_num()
    assert ret == 1