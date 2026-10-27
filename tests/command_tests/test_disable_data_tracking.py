from .common import *
from bbclient import *

params = [
    ("DUMMY", r"${MACHINE}"),
]

@pytest.mark.parametrize("variable_name, variable_value", params)
def test_disable_data_tracking_wrynose(wrynose_client: BBClient, variable_name, variable_value) -> None:
    __test_impl(wrynose_client, variable_name, variable_value)

@pytest.mark.parametrize("variable_name, variable_value", params)
def test_disable_data_tracking_scarthgap(scarthgap_client: BBClient, variable_name, variable_value) -> None:
    __test_impl(scarthgap_client, variable_name, variable_value)

def __test_impl(client: BBClient, variable_name, variable_value) -> None:
    client.enable_data_tracking()
    client.set_variable(variable_name, variable_value)
    ret = client.data_store_connector_varhist_cmd(0, "variable", variable_name)
    assert len(ret) == 1
    client.disable_data_tracking()
    client.set_variable(variable_name, variable_value)
    ret = client.data_store_connector_varhist_cmd(0, "variable", variable_name)
    assert len(ret) == 1
    ret = client.data_store_connector_varhist_cmd(0, "del_var_history", variable_name)