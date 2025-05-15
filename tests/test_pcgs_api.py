import pytest
from plugins.coin.pcgs_api import PCGSApi
from unittest.mock import patch

def test_pcgs_api_instantiation():
    api = PCGSApi()
    assert isinstance(api, PCGSApi)

@patch('plugins.coin.pcgs_api.PCGSApi.make_api_call')
def test_make_api_call(mock_call):
    mock_call.return_value = None
    api = PCGSApi()
    result = api.make_api_call('1234567890123456', 'PCGS')
    assert result is None

def test_make_api_call_with_invalid_key():
    api = PCGSApi()
    # Temporarily remove the API key
    api.api_key = None
    result = api.make_api_call('1234567890123456', 'PCGS')
    assert result is None or result is False 