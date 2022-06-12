import requests
from datetime import datetime
import pandas as pd


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    # print(abs((d2 - d1).days))
    return abs((d2 - d1).days)


url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json'
headers = {'User-Agent': "BB Company, bab385@gmail.com",
           "Accept-Encoding": "gzip, deflate"}
r = requests.get(url, headers=headers)
data = r.json()
financial_item_list = data['facts']['us-gaap']

new_set = set()
for each in financial_item_list:
    values = financial_item_list[each]['units']
    for this in values:
        new_set.add(this)
print(new_set)

new_list = []
for each in financial_item_list:
    try:
        values = financial_item_list[each]['units']['USD']
    except:
        pass
    for this in values:
        try:
            this['line'] = each
        except:
            continue
        print(this)
        new_list.append(this)
df = pd.DataFrame.from_dict(new_list)
df.to_excel('trial.xlsx')

# print(new_list)


def secStuff(fin_data):

    df1 = pd.DataFrame.from_dict(values)
    df1['fin-type'] = fin_data
    # print(df1)
    df_cont = pd.concat([df_cont, df1])


# secStuff('OperatingIncomeLoss')
# print(df)
# secStuff('Revenues')
# print(df)

# df.to_excel('trial.xlsx')


# 'https://data.sec.gov/submissions/CIK##########.json'
# https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json
