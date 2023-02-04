from .common import *
from bbclient import *

params = [
    (".conf", "recipes-bsp", [FilesMatchingFoundEvent], CommandCompletedEvent),
    (".conf", "recipes-dummy_dir", [], CommandCompletedEvent),
    (".conffff", "recipes-bsp", [], CommandCompletedEvent),
]

@pytest.mark.parametrize("file_regex, directory, expect_event_types, expect_command_result", params)
def test_find_files_matching_in_dir_main(main_client: BBClient, file_regex: str, directory: str, expect_event_types: List[BBEventBase], expect_command_result: BBEventBase) -> None:
    __test_impl(main_client, file_regex, directory, expect_event_types, expect_command_result)
    
@pytest.mark.parametrize("file_regex, directory, expect_event_types, expect_command_result", params)
def test_find_config_files_kirkstone(kirkstone_client: BBClient, file_regex: str, directory: str, expect_event_types: List[BBEventBase], expect_command_result: BBEventBase) -> None:
    __test_impl(kirkstone_client, file_regex, directory, expect_event_types, expect_command_result)

@pytest.mark.parametrize("file_regex, directory, expect_event_types, expect_command_result", params)
def test_find_config_files_dunfell(dunfell_client: BBClient, file_regex: str, directory: str, expect_event_types: List[BBEventBase], expect_command_result: BBEventBase) -> None:
    __test_impl(dunfell_client, file_regex, directory, expect_event_types, expect_command_result)

def __test_impl(client: BBClient, file_regex: str, directory: str, expect_event_types: List[BBEventBase], expect_command_result: BBEventBase) -> None:
    callback_monitors: List[CallbackMonitor] = []
    callback_ids: List[int] = []
    for expect_event_type in expect_event_types:
        callback_monitor: CallbackMonitor = CallbackMonitor()
        callback_monitors.append(callback_monitor)
        callback_id: int = client.register_callback(expect_event_type, callback_monitor.callback)
        callback_ids.append(callback_id)
    client.find_files_matching_in_dir(file_regex, directory)
    for monitor in callback_monitors:
        assert monitor.is_callback
    for id in callback_ids:
        client.unregister_callback(id)