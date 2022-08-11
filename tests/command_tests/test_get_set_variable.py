from .common import *
from bbclient import *

def test_get_set_variable(main_client: BBClient) -> None:
    variable_name: str = "DUMMY"
    variable_value: str = r"${MACHINE}"
    main_client.set_variable(variable_name, variable_value)

    ret: str = main_client.get_set_variable(variable_name)
    machine_variable_name: str = "MACHINE"
    machine_variable_value: str = main_client.get_variable(machine_variable_name)
    assert ret == machine_variable_value

    ret: str = main_client.get_variable(variable_name, False)
    assert ret == machine_variable_value