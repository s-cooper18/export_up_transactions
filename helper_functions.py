import requests

def create_accounts_dict(row):
    my_dict = {
        'displayName': row['attributes']['displayName'],
        'id': row['id'],
        'balance': row['attributes']['balance']['value']
    }
    return my_dict

def calc_start_end_strings(month, year):
    timezoneStr = 'T00:00:00+10:00'
    startDate = '-'.join([str(year), str(month).zfill(2), '01'])
    endDate = '-'.join([str(year), str(month + 1).zfill(2), '01'])
    return [startDate + timezoneStr, endDate + timezoneStr]

def retrieve_all_transactions(token, params, transactionsEndpoint):
    all_transactions = []
    urls = [transactionsEndpoint]
    next_url = urls[0]
    while (next_url is not None and len(urls) < 10):
        response = requests.get(next_url, headers={'Authorization': 'Bearer ' + token}, params=params)
        all_transactions.extend(response.json()['data'])
        next_url = response.json()['links']['next']
        urls.append(next_url)
    return all_transactions

def get_accounts(token):
    accountEndpoint ='https://api.up.com.au/api/v1/accounts'
    response = requests.get(accountEndpoint, headers={'Authorization': 'Bearer ' + token})
    accounts = [create_accounts_dict(account) for account in response.json()['data']]
    return accounts

def create_accounts_dict(row):
    my_dict = {
        'displayName': row['attributes']['displayName'],
        'id': row['id'],
        'balance': row['attributes']['balance']['value']
    }
    return my_dict

def transform_row(transaction):
    attributes_dict = transaction['attributes']
    attributes_dict.update({'amount':  transaction['attributes']['amount']['value']})
    #attributes_dict.update({'holdInfo':  transaction['attributes']['holdInfo']['value']})
    #attributes_dict.update({'currencyCode': transaction['attributes']['amount']['currencyCode']})
    category = transaction['relationships']['category']['data']['id'] if transaction['relationships']['category']['data'] != None else None
    #tags = ','.join(transaction['relationships']['tags']['data']['tags'])
    attributes_dict.update({'category': category})
    return attributes_dict