import json
import pytest
from src import up_api


@pytest.fixture
def sample_transaction_response() -> dict[str, object]:
    FILENAME = "tests/data/sample_transactions.json"
    with open(FILENAME) as f:
        data = json.load(f)
    return data


class TestRetrieveAllTransactionsSerialisation:
    def test_retrieve_all_transactions(self, sample_transaction_response):
        up_api.RetrieveTransactionsResponse(**sample_transaction_response)
