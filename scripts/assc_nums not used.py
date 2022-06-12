from code import interact
import requests
import json
import re
from bs4 import BeautifulSoup
import pandas as pd

cik_url = 'https://www.sec.gov/files/company_tickers.json'
cik_headers = {'User-Agent': "BB Company, bab385@gmail.com",
               "Accept-Encoding": "gzip, deflate"}
cik_r = requests.get(cik_url, headers=cik_headers)
cik_data = cik_r.json()
# print(cik_data)
ciks = []
for each in cik_data:
    ciks.append(cik_data[each]['cik_str'])
    # print(cik_data[each]['cik_str'])
# print(ciks)
apple = '320193'
microsoft = '789019'
amazon = '1018724'
autozone = '866787'
# cik = amazon
print(len(ciks))
items = []
comp_count = 9000
for cik in ciks[comp_count:]:
    # define endpoint
    endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"

    # define parameters
    param_dict = {'action': 'getcompany',
                  'CIK': cik,
                  'type': '10-k',
                  'dateb': '',
                  'datea': '',
                  'owner': 'exclude',
                  'start': '',
                  'output': 'html',
                  'count': '100'}

    headers = {'User-Agent': "BB Company, bab385@gmail.com",
               "Accept-Encoding": "gzip, deflate"}

    # define response
    response = requests.get(url=endpoint, params=param_dict, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup.prettify())

    table = soup.find(class_="tableFile2")

    rows = list(table.children)

    # find company name
    span = soup.find(['span'], class_='companyName')
    name_end = re.search(' CIK#', str(span.text)).span()[0]
    company_name = span.text[:name_end]

    # items = []

    # creates a list of dictionaries of all assc numbers
    x = 1
    for row in rows[2:len(rows)]:
        if isinstance(row, str):
            continue
        else:
            link = row.find_all(['a'], id='interactiveDataBtn')
            if link != []:
                interactive_data = True
            else:
                interactive_data = False
            cells = list(row.children)

            acc_pos = re.search("Acc-no: ", str(cells[5])).span()
            start_pos = acc_pos[1]
            end_pos = acc_pos[1] + 20
            acc_no = str(cells[5])[start_pos:end_pos]
            report = cells[1].text
            file_date = cells[7].text
            if interactive_data == True:
                items.append({'file_date': file_date,
                              'report': report,
                              'acc-no': acc_no,
                              'cik': cik,
                              'id': x,
                              'interactive_data': interactive_data})
            x += 1
            # print(x)
    print(comp_count)
    comp_count += 1

    # print(json.dumps(items, sort_keys=True, indent=4))

    # filters through assc numbers for those with interactive data
    interactive_assc = []
    for item in items:
        item_new = item['acc-no'].replace('-', '')
        if item['interactive_data'] == True:
            interactive_assc.append(item_new)
    # print(interactive_assc)

    # finds the interactive data buttons and gives the assc number associated with it
    links = soup.find_all(['a'], id="interactiveDataBtn")
    for link in links:
        href = link['href']
        href = href.split('&')
        accs_num = href[2].split('=')[1]
        # print(accs_num)

df = pd.DataFrame.from_dict(items)
df.to_csv('accn_num.csv')
print(df)
