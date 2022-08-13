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
    client.find_config_file_path(config_file_name)
    ret: Optional[BBEventBase] = client.wait_event([ConfigFilePathFoundEvent], 3)
    assert isinstance(ret, ConfigFilePathFoundEvent)
    ret: ConfigFilePathFoundEvent
    assert os.path.isfile(ret.path)
    ret: Optional[BBEventBase] = client.wait_done_async()
    assert isinstance(ret, CommandCompletedEvent)