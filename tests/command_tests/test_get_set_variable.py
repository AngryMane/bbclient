from .common import *
from bbclient import *

def test_get_runtime_recommends_main(main_client: BBClient) -> None:
    __test_impl(main_client)

def test_get_runtime_recommends_kirkstone(kirkstone_client: BBClient) -> None:
    __test_impl(kirkstone_client)

def test_get_runtime_recommends_dunfell(dunfell_client: BBClient) -> None:
    __test_impl(dunfell_client)

def __test_impl(client: BBClient) -> None:
    variable_name: str = "DUMMY"
    variable_value: str = r"${MACHINE}"
    client.set_variable(variable_name, variable_value)

    ret: str = client.get_set_variable(variable_name)
    machine_variable_name: str = "MACHINE"
    machine_variable_value: str = client.get_variable(machine_variable_name)
    assert ret == machine_variable_value

    ret: str = client.get_variable(variable_name, False)
    assert ret == machine_variable_value