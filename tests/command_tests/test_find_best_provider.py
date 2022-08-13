from .common import *
from bbclient import *

params = [
    ("gcc"),
]

@pytest.mark.parametrize("package_name", params)
def test_find_best_provider_main(main_client: BBClient, package_name) -> None:
    __test_imple(main_client, package_name)

@pytest.mark.parametrize("package_name", params)
def test_find_best_provider_kirkstone(kirkstone_client: BBClient, package_name) -> None:
    __test_imple(kirkstone_client, package_name)

@pytest.mark.parametrize("package_name", params)
def test_find_best_provider_dunfell(dunfell_client: BBClient, package_name) -> None:
    __test_imple(dunfell_client, package_name)

def __test_imple(client: BBClient, package_name) -> None:
    result: List[str] = client.find_best_provider(package_name)
    recipe_file_path: str = result[3]
    data_store_index: int = client.parse_recipe_file(recipe_file_path)
    package_name_from_recipe: str = client.data_store_connector_cmd(data_store_index, "getVar", "PN")
    assert package_name == package_name_from_recipe