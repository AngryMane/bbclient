from .common import *
from bbclient import *

def test_parse_configuration_wrynose(wrynose_client: BBClient) -> None:
    __test_impl(wrynose_client)

def test_parse_configuration_scarthgap(scarthgap_client: BBClient) -> None:
    __test_impl(scarthgap_client)

def __test_impl(client: BBClient) -> None:
    client.parse_configuration()
    # This command will return no results and events.