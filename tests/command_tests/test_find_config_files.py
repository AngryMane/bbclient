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
    client.find_config_files(variable_name)
    for expect_event_type in except_event_types:
        ret: Optional[BBEventBase] = client.wait_event([expect_event_type], 3)
        assert isinstance(ret, expect_event_type)
    ret: BBEventBase = client.wait_done_async()
    assert isinstance(ret, expect_command_result)