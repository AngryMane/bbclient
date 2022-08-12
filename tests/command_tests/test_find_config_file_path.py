from .common import *
from bbclient import *

params = [
    ("bblayers.conf"),
]

@pytest.mark.parametrize("config_file_name", params)
def test_find_config_file_path_main(main_client: BBClient, config_file_name: str) -> None:
    main_client.find_config_file_path(config_file_name)
    ret: Optional[BBEventBase] = main_client.wait_event([ConfigFilePathFoundEvent], 3)
    assert isinstance(ret, ConfigFilePathFoundEvent)
    ret: ConfigFilePathFoundEvent
    assert os.path.isfile(ret.path)
    ret: Optional[BBEventBase] = main_client.wait_done_async()
    assert isinstance(ret, CommandCompletedEvent)

@pytest.mark.parametrize("config_file_name", params)
def test_find_config_file_path_kirkstone(kirkstone_client: BBClient, config_file_name: str) -> None:
    kirkstone_client.find_config_file_path(config_file_name)
    ret: Optional[BBEventBase] = kirkstone_client.wait_event([ConfigFilePathFoundEvent], 3)
    assert isinstance(ret, ConfigFilePathFoundEvent)
    ret: ConfigFilePathFoundEvent
    assert os.path.isfile(ret.path)
    ret: Optional[BBEventBase] = kirkstone_client.wait_done_async()
    assert isinstance(ret, CommandCompletedEvent)

@pytest.mark.parametrize("config_file_name", params)
def test_find_config_file_path_dunfell(dunfell_client: BBClient, config_file_name: str) -> None:
    dunfell_client.find_config_file_path(config_file_name)
    ret: Optional[BBEventBase] = dunfell_client.wait_event([ConfigFilePathFoundEvent], 3)
    assert isinstance(ret, ConfigFilePathFoundEvent)
    ret: ConfigFilePathFoundEvent
    assert os.path.isfile(ret.path)
    ret: Optional[BBEventBase] = dunfell_client.wait_done_async()
    assert isinstance(ret, CommandCompletedEvent)