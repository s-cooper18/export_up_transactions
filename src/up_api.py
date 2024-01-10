import requests
from datetime import datetime
from src.utils.base_models import CamelisedBaseModel


class TransactionAmount(CamelisedBaseModel):
    currency_code: str
    value: str
    value_in_base_units: int


class TransactionAttributes(CamelisedBaseModel):
    status: str
    raw_text: str | None
    description: str
    message: str
    amount: TransactionAmount
    foreign_amount: TransactionAmount | None
    settled_at: datetime
    created_at: datetime


class TransactionData(CamelisedBaseModel):
    id: str
    attributes: TransactionAttributes
    relationships: dict[str, object]


class Links(CamelisedBaseModel):
    next: str | None
    prev: str | None


class RetrieveTransactionsResponse(CamelisedBaseModel):
    data: list[TransactionData]
    links: Links


def retrieve_all_transactions(
    token: str,
    start_date: datetime,
    end_date: datetime,
    url: str = "https://api.up.com.au/api/v1/transactions",
) -> RetrieveTransactionsResponse:
    response = requests.get(
        url,
        headers={"Authorization": "Bearer " + token},
        params={
            "filter[since]": start_date.isoformat(),
            "filter[until]": end_date.isoformat(),
            "page[size]": 100,
        },
    )
    result: dict[str, object] = response.json()
    return RetrieveTransactionsResponse(**result)
