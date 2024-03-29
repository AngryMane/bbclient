from .common import * 
from bbclient import *

params = [
    (["busybox"], "fetch", CommandCompletedEvent),
    (["busybox", "python3:patch"], "fetch", CommandFailedEvent),
    (["busybox", "python3:do_patch"], "fetch", CommandCompletedEvent),
    (["busybox", "dummy_package"], "fetch", CommandFailedEvent),
]

@pytest.mark.parametrize("targets, task, expect", params)
def test_build_targets_main(main_client: BBClient, targets: List[str], task: str, expect: Type[BBEventBase]) -> None:
    __test_impl(main_client, targets, task, expect)

@pytest.mark.parametrize("targets, task, expect", params)
def test_build_targets_kirkstone(kirkstone_client: BBClient, targets: List[str], task: str, expect: Type[BBEventBase]) -> None:
    __test_impl(kirkstone_client, targets, task, expect)

@pytest.mark.parametrize("targets, task, expect", params)
def test_build_targets_dunfell(dunfell_client: BBClient, targets: List[str], task: str, expect: Type[BBEventBase]) -> None:
    __test_impl(dunfell_client, targets, task, expect)

def __test_impl(client: BBClient, targets: List[str], task: str, expect: Type[BBEventBase]) -> None:
    callback_monitor: CallbackMonitor = CallbackMonitor()
    callback_id: int = client.register_callback(expect, callback_monitor.callback)
    client.build_targets(targets, task)
    client.unregister_callback(callback_id)
    assert(callback_monitor.is_callback == True)