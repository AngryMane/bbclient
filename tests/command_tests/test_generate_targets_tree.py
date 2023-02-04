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
    callback_monitors: List[CallbackMonitor] = []
    callback_ids: List[int] = []
    for expect_event_type in [TreeDataPreparationStartedEvent, TreeDataPreparationProgressEvent, TreeDataPreparationCompletedEvent, TargetsTreeGeneratedEvent]:
        callback_monitor: CallbackMonitor = CallbackMonitor()
        callback_monitors.append(callback_monitor)
        callback_id: int = client.register_callback(expect_event_type, callback_monitor.callback)
        callback_ids.append(callback_id)
    client.generate_targets_tree(klass_file_path, targets)
    for monitor in callback_monitors:
        assert monitor.is_callback
    for id in callback_ids:
        client.unregister_callback(id)