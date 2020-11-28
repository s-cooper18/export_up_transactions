import pandas as pd
import helper_functions

# function to obtain my transactions and save to a csv file

# Uncomment this line and enter your token - remember this is secret
# token = 

accounts = helper_functions.get_accounts(token)

# ID for main up account
my_id = accounts[0]['id']

month = 10
year = 2020

startDate, endDate = helper_functions.calc_start_end_strings(month, year)

transactionsEndpoint ='https://api.up.com.au/api/v1/accounts/' + my_id + '/transactions'

params = {'filter[since]': startDate, 'filter[until]': endDate, 'page[size]': 100}

all_transactions = retrieve_all_transactions(token, params, transactionsEndpoint)

col_names = ["status", "rawText", "description", "message", "holdInfo", "amount", "createdAt", "settledAt", 'category', 'tags', 'currencyCode']

transactions_list = [transform_row(transaction) for transaction in all_transactions]

df = pd.DataFrame(transactions_list, columns=row_names)

df.to_csv('filename.csv', index=False)
