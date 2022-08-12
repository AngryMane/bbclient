from .common import *
from bbclient import *

params = [
    ("gcc"),
]

@pytest.mark.parametrize("package_name", params)
def test_find_best_provider_main(main_client: BBClient, package_name) -> None:

    result: List[str] = main_client.find_best_provider(package_name)
    recipe_file_path: str = result[3]
    data_store_index: int = main_client.parse_recipe_file(recipe_file_path)
    package_name_from_recipe: str = main_client.data_store_connector_cmd(data_store_index, "getVar", "PN")

    assert package_name == package_name_from_recipe

@pytest.mark.parametrize("package_name", params)
def test_find_best_provider_kirkstone(kirkstone_client: BBClient, package_name) -> None:

    result: List[str] = kirkstone_client.find_best_provider(package_name)
    recipe_file_path: str = result[3]
    data_store_index: int = kirkstone_client.parse_recipe_file(recipe_file_path)
    package_name_from_recipe: str = kirkstone_client.data_store_connector_cmd(data_store_index, "getVar", "PN")

    assert package_name == package_name_from_recipe

@pytest.mark.parametrize("package_name", params)
def test_find_best_provider_dunfell(dunfell_client: BBClient, package_name) -> None:

    result: List[str] = dunfell_client.find_best_provider(package_name)
    recipe_file_path: str = result[3]
    data_store_index: int = dunfell_client.parse_recipe_file(recipe_file_path)
    package_name_from_recipe: str = dunfell_client.data_store_connector_cmd(data_store_index, "getVar", "PN")

    assert package_name == package_name_from_recipe