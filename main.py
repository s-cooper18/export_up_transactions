import pandas as pd
import helper_functions
import argparse

# function to obtain my transactions and save to a csv file

# Uncomment this line and enter your token - remember this is secret
# token = 


def main(token, month, year):
    accounts = helper_functions.get_accounts(token)

    my_id = accounts[0]['id']

    startDate, endDate = helper_functions.calc_start_end_strings(month, year)

    transactionsEndpoint ='https://api.up.com.au/api/v1/accounts/' + my_id + '/transactions'

    params = {'filter[since]': startDate, 'filter[until]': endDate, 'page[size]': 100}

    all_transactions = helper_functions.retrieve_all_transactions(token, params, transactionsEndpoint)

    col_names = ["status", "rawText", "description", "message", "holdInfo", "amount", "createdAt", "settledAt", 'category', 'tags', 'currencyCode']

    transactions_list = [helper_functions.transform_row(transaction) for transaction in all_transactions]

    df = pd.DataFrame(transactions_list, columns=col_names)

    df.to_csv('filename.csv', index=False)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Export a monthly csv file for up transactions')
    parser.add_argument('month', metavar='month', type=int,
                    help='month to retrieve transactions for')
    parser.add_argument('year', metavar='year', type=int,
                    help='year to retrieve transactions for')
    parser.add_argument('token', metavar='token',
                    help='personal id token')
    args = parser.parse_args()

    main(args.token, args.month, args.year)
    print('file saved')





