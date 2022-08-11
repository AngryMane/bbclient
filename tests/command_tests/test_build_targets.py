from .common import * 
from bbclient import *

params = [
    (["busybox"], "fetch", CommandCompletedEvent),
    (["busybox", "dummy_package"], "fetch", CommandFailedEvent),
]

@pytest.mark.parametrize("targets, task, expect", params)
def test_build_targets_main(main_client: BBClient, targets: List[str], task: str, expect: Type[BBEventBase]) -> None:
    main_client.build_targets(targets, task)
    result: Optional[BBEventBase] = main_client.wait_done_async()
    assert isinstance(result, expect)

@pytest.mark.parametrize("targets, task, expect", params)
def test_build_targets_kirkstone(kirkstone_client: BBClient, targets: List[str], task: str, expect: Type[BBEventBase]) -> None:
    kirkstone_client.build_targets(targets, task)
    result: Optional[BBEventBase] = kirkstone_client.wait_done_async()
    assert isinstance(result, expect)

@pytest.mark.parametrize("targets, task, expect", params)
def test_build_targets_dunfell(dunfell_client: BBClient, targets: List[str], task: str, expect: Type[BBEventBase]) -> None:
    dunfell_client.build_targets(targets, task)
    result: Optional[BBEventBase] = dunfell_client.wait_done_async()
    assert isinstance(result, expect)