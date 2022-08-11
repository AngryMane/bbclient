from .common import *
from bbclient import *

def test_enable_data_tracking(main_client: BBClient) -> None:
    variable_name: str = "DUMMY"
    variable_value: str = r"${MACHINE}"

    main_client.set_variable(variable_name, variable_value)
    ret = main_client.data_store_connector_varhist_cmd(0, "variable", "DUMMY")
    assert len(ret) == 0

    main_client.enable_data_tracking()

    main_client.set_variable(variable_name, variable_value)
    ret = main_client.data_store_connector_varhist_cmd(0, "variable", "DUMMY")
    assert len(ret) == 1

    main_client.disable_data_tracking()
    ret = main_client.data_store_connector_varhist_cmd(0, "del_var_history", "DUMMY") # delete history for latter tests