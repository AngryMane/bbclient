from .common import *
from bbclient import *

params = [
    ("MACHINE", [ConfigFilesFoundEvent], CommandCompletedEvent),
    ("DUMMY", [], CommandCompletedEvent),
]

@pytest.mark.parametrize("variable_name, except_event_types, expect_command_result", params)
def test_find_config_files_main(main_client: BBClient, variable_name: str, except_event_types: List[BBEventBase], expect_command_result: BBEventBase) -> None:
    __test_impl(main_client, variable_name, except_event_types, expect_command_result)

@pytest.mark.parametrize("variable_name, except_event_types, expect_command_result", params)
def test_find_config_files_kirkstone(kirkstone_client: BBClient, variable_name: str, except_event_types: List[BBEventBase], expect_command_result: BBEventBase) -> None:
    __test_impl(kirkstone_client, variable_name, except_event_types, expect_command_result)

@pytest.mark.parametrize("variable_name, except_event_types, expect_command_result", params)
def test_find_config_files_dunfell(dunfell_client: BBClient, variable_name: str, except_event_types: List[BBEventBase], expect_command_result: BBEventBase) -> None:
    __test_impl(dunfell_client, variable_name, except_event_types, expect_command_result)

def __test_impl(client: BBClient, variable_name: str, except_event_types: List[BBEventBase], expect_command_result: BBEventBase) -> None:
    callback_monitors: List[CallbackMonitor] = []
    callback_ids: List[int] = []
    for expect_event_type in except_event_types:
        callback_monitor: CallbackMonitor = CallbackMonitor()
        callback_monitors.append(callback_monitor)
        callback_id: int = client.register_callback(expect_event_type, callback_monitor.callback)
        callback_ids.append(callback_id)
    client.find_config_files(variable_name)
    for monitor in callback_monitors:
        assert monitor.is_callback
    for id in callback_ids:
        client.unregister_callback(id)