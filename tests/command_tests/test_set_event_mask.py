from .common import *
from bbclient import *

def test_set_event_mask(main_client: BBClient) -> None:
    ui_handler: int = main_client.get_uihandler_num()
    ret: bool = main_client.set_event_mask(ui_handler, logging.DEBUG, {}, ["*"])
    assert ret == True