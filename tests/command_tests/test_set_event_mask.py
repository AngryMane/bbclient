from .common import *
from bbclient import *

def test_set_event_mask(wrynose_client: BBClient) -> None:
    ui_handler: int = wrynose_client.get_uihandler_num()
    ret: bool = wrynose_client.set_event_mask(ui_handler, logging.DEBUG, {}, ["*"])
    assert ret == True