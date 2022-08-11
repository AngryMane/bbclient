from .common import *
from bbclient import *

params = [
    ("DUMMY", r"${MACHINE}"),
]

@pytest.mark.parametrize("variable_name, variable_value", params)
def test_disable_data_tracking_main(main_client: BBClient, variable_name, variable_value) -> None:

    main_client.enable_data_tracking()

    main_client.set_variable(variable_name, variable_value)
    ret = main_client.data_store_connector_varhist_cmd(0, "variable", variable_name)
    assert len(ret) == 1

    main_client.disable_data_tracking()

    main_client.set_variable(variable_name, variable_value)
    ret = main_client.data_store_connector_varhist_cmd(0, "variable", variable_name)
    assert len(ret) == 1
    ret = main_client.data_store_connector_varhist_cmd(0, "del_var_history", variable_name)

@pytest.mark.parametrize("variable_name, variable_value", params)
def test_disable_data_tracking_kirkstone(kirkstone_client: BBClient, variable_name, variable_value) -> None:

    kirkstone_client.enable_data_tracking()

    kirkstone_client.set_variable(variable_name, variable_value)
    ret = kirkstone_client.data_store_connector_varhist_cmd(0, "variable", variable_name)
    assert len(ret) == 1

    kirkstone_client.disable_data_tracking()

    kirkstone_client.set_variable(variable_name, variable_value)
    ret = kirkstone_client.data_store_connector_varhist_cmd(0, "variable", variable_name)
    assert len(ret) == 1
    ret = kirkstone_client.data_store_connector_varhist_cmd(0, "del_var_history", variable_name)

@pytest.mark.parametrize("variable_name, variable_value", params)
def test_disable_data_tracking_dunfell(dunfell_client: BBClient, variable_name, variable_value) -> None:

    dunfell_client.enable_data_tracking()

    dunfell_client.set_variable(variable_name, variable_value)
    ret = dunfell_client.data_store_connector_varhist_cmd(0, "variable", variable_name)
    assert len(ret) == 1

    dunfell_client.disable_data_tracking()

    dunfell_client.set_variable(variable_name, variable_value)
    ret = dunfell_client.data_store_connector_varhist_cmd(0, "variable", variable_name)
    assert len(ret) == 1
    ret = dunfell_client.data_store_connector_varhist_cmd(0, "del_var_history", variable_name)