from .common import * 
from bbclient import *

params = [
    ("getVar", ["MACHINE"]),
]

@pytest.mark.parametrize("command, args", params)
def test_data_store_connector_cmd_wrynose(wrynose_client: BBClient, command: str, args: List[Any]) -> None:
    __test_imple(wrynose_client, command, args)

@pytest.mark.parametrize("command, args", params)
def test_data_store_connector_cmd_scarthgap(scarthgap_client: BBClient, command: str, args: List[Any]) -> None:
    __test_imple(scarthgap_client, command, args)

def __test_imple(client: BBClient, command: str, args: List[Any]) -> None:
    ret: Any = client.data_store_connector_cmd(0, command, *args)
    print(ret)
    assert isinstance(ret, str)

# tests for getVarFlags and getVarFlag
def test_get_var_flags_wrynose(wrynose_client: BBClient) -> None:
    __test_imple_for_get_var_flags(wrynose_client)

def test_get_var_flags_scarthgap(scarthgap_client: BBClient) -> None:
    __test_imple_for_get_var_flags(scarthgap_client)

def __test_imple_for_get_var_flags(client: BBClient) -> None:
    ret: Mapping[str, str] = client.data_store_connector_cmd(0, "getVarFlags", "MACHINE")
    for key, value in ret.items():
        expect: Mapping[str, str] = client.data_store_connector_cmd(0, "getVarFlag", "MACHINE", key)
        assert value == expect