from .common import *
from bbclient import *

params = [
    (["gcc"], "compile"),
]

@pytest.mark.parametrize("targets, task", params)
def test_generate_dep_tree_event_main(main_client: BBClient, targets: List[str], task: str) -> None:
    __test_impl(main_client, targets, task)

@pytest.mark.parametrize("targets, task", params)
def test_generate_dep_tree_event_kirkstone(kirkstone_client: BBClient, targets: List[str], task: str) -> None:
    __test_impl(kirkstone_client, targets, task)

@pytest.mark.parametrize("targets, task", params)
def test_generate_dep_tree_event_dunfell(dunfell_client: BBClient, targets: List[str], task: str) -> None:
    __test_impl(dunfell_client, targets, task)

def __test_impl(client: BBClient, targets: List[str], task: str) -> None:
    client.generate_dep_tree_event(targets, task)
    ret: Optional[BBEventBase] = client.wait_event([TreeDataPreparationStartedEvent])
    assert isinstance(ret, TreeDataPreparationStartedEvent)
    ret: Optional[BBEventBase] = client.wait_event([TreeDataPreparationProgressEvent])
    assert isinstance(ret, TreeDataPreparationProgressEvent)
    ret: Optional[BBEventBase] = client.wait_event([TreeDataPreparationCompletedEvent])
    assert isinstance(ret, TreeDataPreparationCompletedEvent)
    ret: Optional[BBEventBase] = client.wait_event([DepTreeGeneratedEvent])
    assert isinstance(ret, DepTreeGeneratedEvent)
    ret: Optional[BBEventBase] = client.wait_done_async()
    assert isinstance(ret, CommandCompletedEvent)