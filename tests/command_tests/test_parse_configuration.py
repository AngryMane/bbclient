from .common import *
from bbclient import *

def test_parse_configuration_main(main_client: BBClient) -> None:
    __test_impl(main_client)

def test_parse_configuration_kirkstone(kirkstone_client: BBClient) -> None:
    __test_impl(kirkstone_client)

def test_parse_configuration_dunfell(dunfell_client: BBClient) -> None:
    __test_impl(dunfell_client)

def __test_impl(client: BBClient) -> None:
    client.parse_configuration()
    # This command will return no results and events.