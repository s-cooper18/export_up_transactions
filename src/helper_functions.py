from datetime import datetime, timezone, timedelta
import requests
from dataclasses import dataclass
from src import up_api


@dataclass
class DataRow:
    status: str
    raw_text: str
    description: str
    message: str
    amount: str
    created_at: str
    category: str
    tags: str
    currency_code: str


def create_accounts_dict(
    row: dict[str, dict[str, dict[str, object]]]
) -> dict[str, object]:
    my_dict = {
        "displayName": row["attributes"]["displayName"],
        "id": row["id"],
        "balance": row["attributes"]["balance"]["value"],
    }
    return my_dict


def calc_start_end_strings(month: int, year: int) -> list[str]:
    aest_tz = timezone(timedelta(hours=10))

    start_date = datetime(year, month, 1, tzinfo=aest_tz)

    end_year = year + (month // 12)
    end_month = (month % 12) + 1

    end_date = datetime(end_year, end_month, 1, tzinfo=aest_tz)
    return [start_date.isoformat(), end_date.isoformat()]


def retrieve_all_transactions(
    token: str, start_date: datetime, end_date: datetime
) -> list[up_api.TransactionData]:
    all_transactions: list[up_api.TransactionData]
    urls = []

    result = up_api.retrieve_all_transactions(token, start_date, end_date)
    all_transactions = result.data
    while result.links.next is not None and len(urls) < 10:
        result = up_api.retrieve_all_transactions(
            token, start_date, end_date, result.links.next
        )
        all_transactions.extend(result.data)
        urls.append(result.links.next)
    return all_transactions


def get_accounts(token: str) -> list[dict]:
    accountEndpoint = "https://api.up.com.au/api/v1/accounts"
    response = requests.get(
        accountEndpoint, headers={"Authorization": "Bearer " + token}
    )
    accounts = [create_accounts_dict(account) for account in response.json()["data"]]
    return accounts


def transform_row(transaction: dict) -> DataRow:
    attributes_dict = transaction["attributes"]
    attributes_dict.update({"amount": transaction["attributes"]["amount"]["value"]})
    holdInfo = (
        transaction["attributes"]["holdInfo"].get("value")
        if transaction["attributes"]["holdInfo"] is not None
        else None
    )
    attributes_dict.update({"holdInfo": holdInfo})
    category = (
        transaction["relationships"]["category"]["data"].get("id")
        if transaction["relationships"]["category"]["data"] is not None
        else None
    )
    attributes_dict.update({"category": category})
    breakpoint()
    return DataRow(**attributes_dict)
