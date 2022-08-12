from asyncio.base_subprocess import BaseSubprocessTransport
from distutils.cmd import Command
from tkinter import W
from .common import *
from bbclient import *

params = [
    (".conf", "recipes-bsp", [FilesMatchingFoundEvent], CommandCompletedEvent),
    (".conf", "recipes-dummy_dir", [], CommandCompletedEvent),
    (".conffff", "recipes-bsp", [], CommandCompletedEvent),
]

@pytest.mark.parametrize("file_regex, directory, expect_event_types, expect_command_result", params)
def test_find_files_matching_in_dir_main(main_client: BBClient, file_regex: str, directory: str, expect_event_types: List[BBEventBase], expect_command_result: BBEventBase) -> None:
    main_client.find_files_matching_in_dir(file_regex, directory)
    for expect_event_type in expect_event_types:
        ret: Optional[BBEventBase] = main_client.wait_event([expect_event_type])
        assert isinstance(ret, FilesMatchingFoundEvent)
    ret: Optional[BBEventBase] = main_client.wait_done_async()
    assert isinstance(ret, expect_command_result)
    
@pytest.mark.parametrize("file_regex, directory, expect_event_types, expect_command_result", params)
def test_find_config_files_kirkstone(kirkstone_client: BBClient, file_regex: str, directory: str, expect_event_types: List[BBEventBase], expect_command_result: BBEventBase) -> None:
    kirkstone_client.find_files_matching_in_dir(file_regex, directory)
    for expect_event_type in expect_event_types:
        ret: Optional[BBEventBase] = kirkstone_client.wait_event([expect_event_type])
        assert isinstance(ret, FilesMatchingFoundEvent)
    ret: Optional[BBEventBase] = kirkstone_client.wait_done_async()
    assert isinstance(ret, expect_command_result)

@pytest.mark.parametrize("file_regex, directory, expect_event_types, expect_command_result", params)
def test_find_config_files_dunfell(dunfell_client: BBClient, file_regex: str, directory: str, expect_event_types: List[BBEventBase], expect_command_result: BBEventBase) -> None:
    dunfell_client.find_files_matching_in_dir(file_regex, directory)
    for expect_event_type in expect_event_types:
        ret: Optional[BBEventBase] = dunfell_client.wait_event([expect_event_type])
        assert isinstance(ret, FilesMatchingFoundEvent)
    ret: Optional[BBEventBase] = dunfell_client.wait_done_async()
    assert isinstance(ret, expect_command_result)