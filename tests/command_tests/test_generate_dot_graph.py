from .common import *
from bbclient import *

params = [
    (["gcc"], "compile"),
    (["busybox", "python3:do_fetch"], "compile"),
]

@pytest.mark.parametrize("targets, task", params)
def test_generate_dot_graph_main(main_client: BBClient, targets: List[str], task: str) -> None:
    __test_impl(main_client, targets, task)

@pytest.mark.parametrize("targets, task", params)
def test_generate_dot_graph_kirkstone(kirkstone_client: BBClient, targets: List[str], task: str) -> None:
    __test_impl(kirkstone_client, targets, task)

@pytest.mark.parametrize("targets, task", params)
def test_generate_dot_graph_dunfell(dunfell_client: BBClient, targets: List[str], task: str) -> None:
    __test_impl(dunfell_client, targets, task)

def __test_impl(client: BBClient, targets: List[str], task: str) -> None:
    callback_monitors: List[CallbackMonitor] = []
    callback_ids: List[int] = []
    for expect_event_type in [TreeDataPreparationStartedEvent, TreeDataPreparationProgressEvent, TreeDataPreparationCompletedEvent]:
        callback_monitor: CallbackMonitor = CallbackMonitor()
        callback_monitors.append(callback_monitor)
        callback_id: int = client.register_callback(expect_event_type, callback_monitor.callback)
        callback_ids.append(callback_id)
    client.generate_dot_graph(targets, task)
    for monitor in callback_monitors:
        assert monitor.is_callback
    for id in callback_ids:
        client.unregister_callback(id)