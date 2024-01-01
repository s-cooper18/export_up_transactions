import datetime
import requests


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
    aest_tz = datetime.timezone(datetime.timedelta(hours=10))
    
    start_date = datetime.datetime(year, month, 1, tzinfo=aest_tz)
    
    end_year = year + (month // 12)
    end_month = (month % 12) + 1
    
    end_date = datetime.datetime(end_year, end_month, 1, tzinfo=aest_tz)
    return [start_date.isoformat(), end_date.isoformat()]


def retrieve_all_transactions(
    token: str, params: dict, transactionsEndpoint: str
) -> list:
    all_transactions = []
    urls = [transactionsEndpoint]
    next_url = urls[0]
    while next_url is not None and len(urls) < 10:
        response = requests.get(
            next_url, headers={"Authorization": "Bearer " + token}, params=params
        )
        all_transactions.extend(response.json()["data"])
        next_url = response.json()["links"]["next"]
        urls.append(next_url)
    return all_transactions


def get_accounts(token: str) -> list[dict]:
    accountEndpoint = "https://api.up.com.au/api/v1/accounts"
    response = requests.get(
        accountEndpoint, headers={"Authorization": "Bearer " + token}
    )
    accounts = [create_accounts_dict(account) for account in response.json()["data"]]
    return accounts


def transform_row(transaction: dict) -> dict:
    attributes_dict = transaction["attributes"]
    attributes_dict.update({"amount": transaction["attributes"]["amount"]["value"]})
    holdInfo = (
        transaction["attributes"]["holdInfo"].get("value")
        if transaction["attributes"]["holdInfo"] != None
        else None
    )
    attributes_dict.update({"holdInfo": holdInfo})
    category = (
        transaction["relationships"]["category"]["data"].get("id")
        if transaction["relationships"]["category"]["data"] != None
        else None
    )
    attributes_dict.update({"category": category})
    return attributes_dict
