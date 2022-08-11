from .common import *
from bbclient import *

def test_get_variable(main_client: BBClient) -> None:
    variable_name: str = "MACHINE"
    ret: str = main_client.get_variable(variable_name)
    assert ret is not None