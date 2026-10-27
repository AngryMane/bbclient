from .common import *
from bbclient import *

params = [
    (["gcc"], "compile"),
]

@pytest.mark.parametrize("targets, task", params)
def test_generate_dep_tree_event_wrynose(wrynose_client: BBClient, targets: List[str], task: str) -> None:
    __test_impl(wrynose_client, targets, task)

@pytest.mark.parametrize("targets, task", params)
def test_generate_dep_tree_event_scarthgap(scarthgap_client: BBClient, targets: List[str], task: str) -> None:
    __test_impl(scarthgap_client, targets, task)

def __test_impl(client: BBClient, targets: List[str], task: str) -> None:
    callback_monitors: List[CallbackMonitor] = []
    callback_ids: List[int] = []
    for expect_event_type in [TreeDataPreparationStartedEvent, TreeDataPreparationProgressEvent, TreeDataPreparationCompletedEvent, DepTreeGeneratedEvent]:
        callback_monitor: CallbackMonitor = CallbackMonitor()
        callback_monitors.append(callback_monitor)
        callback_id: int = client.register_callback(expect_event_type, callback_monitor.callback)
        callback_ids.append(callback_id)
    client.generate_dep_tree_event(targets, task)
    for monitor in callback_monitors:
        assert monitor.is_callback
    for id in callback_ids:
        client.unregister_callback(id)