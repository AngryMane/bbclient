from .common import *
from bbclient import *

def test_set_variable(main_client: BBClient) -> None:
    variable_name: str = "DUMMY"
    variable_value: str = "test"
    main_client.set_variable(variable_name, variable_value)
    ret: str = main_client.get_variable(variable_name)
    assert ret == variable_value