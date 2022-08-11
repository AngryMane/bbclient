from .common import * 
from bbclient import *

params = [
    ("getVar", ["MACHINE"]),
]

@pytest.mark.parametrize("command, args", params)
def test_data_store_connector_cmd_main(main_client: BBClient, command: str, args: List[Any]) -> None:
    ret: Any = main_client.data_store_connector_cmd(0, command, *args)
    print(ret)
    assert isinstance(ret, str)

@pytest.mark.parametrize("command, args", params)
def test_data_store_connector_cmd_kirkstone(kirkstone_client: BBClient, command: str, args: List[Any]) -> None:
    ret: Any = kirkstone_client.data_store_connector_cmd(0, command, *args)
    print(ret)
    assert isinstance(ret, str)

@pytest.mark.parametrize("command, args", params)
def test_data_store_connector_cmd_dunfell(dunfell_client: BBClient, command: str, args: List[Any]) -> None:
    ret: Any = dunfell_client.data_store_connector_cmd(0, command, *args)
    print(ret)
    assert isinstance(ret, str)

# tests for getVarFlags and getVarFlag
def test_get_var_flags_main(main_client: BBClient) -> None:
    ret: Mapping[str, str] = main_client.data_store_connector_cmd(0, "getVarFlags", "MACHINE")
    for key, value in ret.items():
        expect: Mapping[str, str] = main_client.data_store_connector_cmd(0, "getVarFlag", "MACHINE", key)
        assert value == expect

def test_get_var_flags_kirkstone(kirkstone_client: BBClient) -> None:
    ret: Mapping[str, str] = kirkstone_client.data_store_connector_cmd(0, "getVarFlags", "MACHINE")
    for key, value in ret.items():
        expect: Mapping[str, str] = kirkstone_client.data_store_connector_cmd(0, "getVarFlag", "MACHINE", key)
        assert value == expect

def test_get_var_flags_dunfell(dunfell_client: BBClient) -> None:
    ret: Mapping[str, str] = dunfell_client.data_store_connector_cmd(0, "getVarFlags", "MACHINE")
    for key, value in ret.items():
        expect: Mapping[str, str] = dunfell_client.data_store_connector_cmd(0, "getVarFlag", "MACHINE", key)
        assert value == expect