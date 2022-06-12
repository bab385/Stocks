import requests
from main.models import Company

url = 'https://www.sec.gov/files/company_tickers.json'
headers = {'User-Agent': "BB Company, bab385@gmail.com",
           "Accept-Encoding": "gzip, deflate"}
r = requests.get(url, headers=headers)
data = r.json()

# for each in data:
#     print(data[each]['cik_str'])
#     print(data[each]['ticker'])
#     print(data[each]['title'])
#     break

for each in data:
    print(each)
    company_add = Company(
        cik=data[each]['cik_str'],
        ticker=data[each]['ticker'],
        name=data[each]['title'])
    company_add.save()
