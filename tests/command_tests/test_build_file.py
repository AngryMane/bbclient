from .common import * 
from bbclient import *

params = [
    ("busybox", "fetch", CommandCompletedEvent),
    ("dummy_package", "fetch", CommandFailedEvent),
]

@pytest.mark.parametrize("package, task, expect", params)
def test_build_file_main(main_client: BBClient, package: str, task: str, expect: Type[BBEventBase]) -> None:
    best_provider: List[str]  = main_client.find_best_provider(package)
    recipe_file_path: str = best_provider[3]
    main_client.build_file(recipe_file_path, task)
    result: Optional[BBEventBase] = main_client.wait_done_async()
    assert isinstance(result, expect)

@pytest.mark.parametrize("package, task, expect", params)
def test_build_file_kirkstone(kirkstone_client: BBClient, package: str, task: str, expect: Type[BBEventBase]) -> None:
    best_provider: List[str]  = kirkstone_client.find_best_provider(package)
    recipe_file_path: str = best_provider[3]
    kirkstone_client.build_file(recipe_file_path, task)
    result: Optional[BBEventBase] = kirkstone_client.wait_done_async()
    assert isinstance(result, expect)

@pytest.mark.parametrize("package, task, expect", params)
def test_build_file_dunfell(dunfell_client: BBClient, package: str, task: str, expect: Type[BBEventBase]) -> None:
    best_provider: List[str] = dunfell_client.find_best_provider(package)
    recipe_file_path: str = best_provider[3]
    dunfell_client.build_file(recipe_file_path, task)
    result: Optional[BBEventBase] = dunfell_client.wait_done_async()
    assert isinstance(result, expect)