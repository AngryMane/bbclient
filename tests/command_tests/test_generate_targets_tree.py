from .common import *
from bbclient import *

params = [
    ("meta/classes/core-image.bbclass", ["gcc"]),
    ("meta/classes/core-image.bbclass", ["busybox", "python3:do_fetch"]),
]

@pytest.mark.parametrize("klass_file_path, targets", params)
def test_generate_targets_tree_main(main_client: BBClient, klass_file_path: str, targets: List[str]) -> None:
    __test_impl(main_client, klass_file_path, targets)

@pytest.mark.parametrize("klass_file_path, targets", params)
def test_generate_targets_tree_kirkstone(kirkstone_client: BBClient, klass_file_path: str, targets: List[str]) -> None:
    __test_impl(kirkstone_client, klass_file_path, targets)

@pytest.mark.parametrize("klass_file_path, targets", params)
def test_generate_targets_tree_dunfell(dunfell_client: BBClient, klass_file_path: str, targets: List[str]) -> None:
    __test_impl(dunfell_client, klass_file_path, targets)

def __test_impl(client: BBClient, klass_file_path: str, targets: List[str]) -> None:
    client.generate_targets_tree(klass_file_path, targets)
    ret: Optional[BBEventBase] = client.wait_event([TreeDataPreparationStartedEvent])
    assert isinstance(ret, TreeDataPreparationStartedEvent)
    ret: Optional[BBEventBase] = client.wait_event([TreeDataPreparationProgressEvent])
    assert isinstance(ret, TreeDataPreparationProgressEvent)
    ret: Optional[BBEventBase] = client.wait_event([TreeDataPreparationCompletedEvent])
    assert isinstance(ret, TreeDataPreparationCompletedEvent)
    ret: Optional[BBEventBase] = client.wait_event([TargetsTreeGeneratedEvent])
    assert isinstance(ret, TargetsTreeGeneratedEvent)
    ret: Optional[BBEventBase] = client.wait_done_async()
    assert isinstance(ret, CommandCompletedEvent)