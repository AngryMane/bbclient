from .common import *
from bbclient import *

params = [
    ("MACHINE"),
    ("DUMMY"),
]

@pytest.mark.parametrize("variable_name", params)
def test_find_config_files_main(main_client: BBClient, variable_name: str) -> None:
    main_client.find_config_files(variable_name)
    ret: Optional[BBEventBase] = main_client.wait_event(ConfigFilesFoundEvent)
    assert isinstance(ret, ConfigFilesFoundEvent)
    ret: Optional[BBEventBase] = main_client.wait_done_async()
    assert isinstance(ret, CommandCompletedEvent)

@pytest.mark.parametrize("variable_name", params)
def test_find_config_files_kirkstone(kirkstone_client: BBClient, variable_name: str) -> None:
    kirkstone_client.find_config_files(variable_name)

@pytest.mark.parametrize("variable_name", params)
def test_find_config_files_dunfell(dunfell_client: BBClient, variable_name: str) -> None:
    dunfell_client.find_config_files(variable_name)