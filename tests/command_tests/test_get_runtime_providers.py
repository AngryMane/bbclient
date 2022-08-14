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
    client.get_runtime_providers(targets, task)