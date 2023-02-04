from .common import *
from bbclient import *

params = [
    ("bblayers.conf"),
]

@pytest.mark.parametrize("config_file_name", params)
def test_find_config_file_path_main(main_client: BBClient, config_file_name: str) -> None:
    __test_impl(main_client, config_file_name)

@pytest.mark.parametrize("config_file_name", params)
def test_find_config_file_path_kirkstone(kirkstone_client: BBClient, config_file_name: str) -> None:
    __test_impl(kirkstone_client, config_file_name)

@pytest.mark.parametrize("config_file_name", params)
def test_find_config_file_path_dunfell(dunfell_client: BBClient, config_file_name: str) -> None:
    __test_impl(dunfell_client, config_file_name)

def __test_impl(client: BBClient, config_file_name: str) -> None:
    complete_monitor: CallbackMonitor = CallbackMonitor()
    file_path_monitor: CallbackMonitor = CallbackMonitor()
    complete_id: int = client.register_callback(CommandCompletedEvent, complete_monitor.callback)
    file_path_id: int = client.register_callback(ConfigFilePathFoundEvent, file_path_monitor.callback)
    client.find_config_file_path(config_file_name)
    client.unregister_callback(complete_id)
    client.unregister_callback(file_path_id)
    ret: ConfigFilePathFoundEvent = file_path_monitor.event

    assert file_path_monitor.is_callback
    assert complete_monitor.is_callback
    assert os.path.isfile(ret.path)