from .common import * 
from bbclient import *

def test_compare_revisions_wrynose(wrynose_client: BBClient) -> None:
    __test_imple(wrynose_client)

# bitbake 2.8 (scarthgap) fails compareRevisions itself with
# "TypeError: 'dict' object does not support the context manager protocol" in fetcher_compare_revisions.
@pytest.mark.xfail(reason="compareRevisions is broken in bitbake 2.8")
def test_compare_revisions_scarthgap(scarthgap_client: BBClient) -> None:
    __test_imple(scarthgap_client)

def __test_imple(client: BBClient) -> None:
    # compareRevisions finishes with CommandExit(code=1) when the cache is out of date,
    # otherwise it finishes with CommandCompleted.
    callback_monitors: List[CallbackMonitor] = []
    callback_ids: List[int] = []
    for expect_event_type in [CommandCompletedEvent, CommandExitEvent]:
        callback_monitor: CallbackMonitor = CallbackMonitor()
        callback_monitors.append(callback_monitor)
        callback_ids.append(client.register_callback(expect_event_type, callback_monitor.callback))
    client.compare_revisions()
    for id in callback_ids:
        client.unregister_callback(id)
    assert any(monitor.is_callback for monitor in callback_monitors)