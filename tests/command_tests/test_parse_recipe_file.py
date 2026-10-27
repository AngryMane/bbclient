from .common import *
from bbclient import *

params = [
    ("gcc"),
]

@pytest.mark.parametrize("package", params)
def test_generate_targets_tree_wrynose(wrynose_client: BBClient, package: str) -> None:
    __test_impl(wrynose_client, package)

@pytest.mark.parametrize("package", params)
def test_generate_targets_tree_scarthgap(scarthgap_client: BBClient, package: str) -> None:
    __test_impl(scarthgap_client, package)

def __test_impl(client: BBClient, package: str) -> None:
    ret: List[str] = client.find_best_provider(package)
    assert len(ret) == 4
    assert os.path.isfile(ret[3])
    datastore_index: int = client.parse_recipe_file(ret[3])
    result: str = client.data_store_connector_cmd(datastore_index, "getVar", "PN")
    assert result == package