import requests
import datetime
import json
import pandas as pd
import json

cik = '0001018724'

'''
flow to get to financial data through dictionary keys
['facts']
['us-gaap']
['financial statement category'] e.g., accounts payable, net sales, etc.
['units']
['USD']

['USD'] can also be {'USD', 'Patent', 'Entity', 'shares', 'segment', 'Segment', 'USD/shares', 'pure', 'Year'}
'''

url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
headers = {'User-Agent': "BB Company, bab385@gmail.com",
           "Accept-Encoding": "gzip, deflate"}

r = requests.get(url, headers=headers)
data = r.json()
# print(json.dumps(data, indent=4))


financial_data = data['facts']['us-gaap']

# print(json.dumps(financial_data, indent=4))
df = pd.DataFrame(financial_data)
df.to_csv('trial.csv')
# print(df)

# creates a list of line descriptions for a financial statement
categories = []
for each in financial_data:
    categories.append(each)


x = 0
income_cash = []
line_dict = {}

# loop through each line description
for each in categories:

    # getting to the 'USD' level gives you the values for financial statements
    try:
        category = financial_data[each]['units']['USD']
    except:
        continue
    for this in category:
        if (this['form'] == '10-K' or this['form'] == '10-K/A'):

            end_date = this['end']
            end_date = datetime.datetime.strptime(
                end_date, '%Y-%m-%d').date()

            # filters out for items that don't have a start date(i.e., not BS items)
            if 'start' in this.keys():
                start_date = this['start']
                start_date = datetime.datetime.strptime(
                    start_date, '%Y-%m-%d').date()

                date_diff = end_date - start_date

                if date_diff.days > 340:
                    x += 1
                    if this['accn'] == '0001018724-22-000005':
                        this['category'] = each
                        this['cik'] = cik
                        line_dict[x] = this

data_json = json.dumps(line_dict, indent=4)
# print(data_json)
df = pd.DataFrame(line_dict).T
df.to_csv('trial.csv')
print(df)


# determines units on each category
# new_set = set()
# for each in categories:
#     category = financial_data[each]['units']
#     for this in category:
#         print(this)
#         new_set.add(this)
