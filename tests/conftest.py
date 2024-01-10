import json
from src import up_api
import pytest


@pytest.fixture
def transaction_response() -> dict[str, object]:
    FILENAME = "tests/data/sample_transactions.json"
    with open(FILENAME) as f:
        data = json.load(f)
    return up_api.RetrieveTransactionsResponse(**data)
