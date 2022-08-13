from .common import * 
from bbclient import *

params = [
    ("busybox", "fetch", CommandCompletedEvent),
    ("dummy_package", "fetch", CommandFailedEvent),
]

@pytest.mark.parametrize("package, task, expect", params)
def test_build_file_main(main_client: BBClient, package: str, task: str, expect: Type[BBEventBase]) -> None:
    __test_imple(main_client, package, task, expect)

@pytest.mark.parametrize("package, task, expect", params)
def test_build_file_kirkstone(kirkstone_client: BBClient, package: str, task: str, expect: Type[BBEventBase]) -> None:
    __test_imple(kirkstone_client, package, task, expect)

@pytest.mark.parametrize("package, task, expect", params)
def test_build_file_dunfell(dunfell_client: BBClient, package: str, task: str, expect: Type[BBEventBase]) -> None:
    __test_imple(dunfell_client, package, task, expect)

def __test_imple(client: BBClient, package: str, task: str, expect: Type[BBEventBase]) -> None:
    best_provider: List[str] = client.find_best_provider(package)
    recipe_file_path: str = best_provider[3]
    client.build_file(recipe_file_path, task)
    result: Optional[BBEventBase] = client.wait_done_async()
    assert isinstance(result, expect)