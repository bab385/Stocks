import requests
import datetime
import json
import re
from bs4 import BeautifulSoup
import pandas as pd

cik = '1018724'
assc_num = '000101872422000005'
r_number = '4'
# 2 - income, 5 - balance sheet, 9 - cash flow

# gives me a list of all of the statements available for the assc number
# assc_no_list = ['000101872422000005', '000101872421000004',
#                 '000101872420000004', '000101872419000004',
#                 '000101872418000005', '000101872417000011',
#                 '000101872416000172', '000101872415000006',
#                 '000101872414000006', '000119312513028520',
#                 '000119312512032846', '000119312511016253',
#                 '000119312510016098']


def statements(assc_num):
    x = 1
    while x < 40:

        url = 'https://www.sec.gov/Archives/edgar/data/' + \
            cik + '/' + assc_num + '/R' + str(x) + '.htm'

        headers = {'User-Agent': "BB Company, bab385@gmail.com",
                   "Accept-Encoding": "gzip, deflate"}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        tables = soup.find_all('table')

        my_table = tables[0]

        headers = my_table.findChildren('th')

        statement_type = headers[0].text
        statement_type = statement_type.lower()
        consolidated = re.search('consolidated', statement_type)

        if consolidated:
            print(x)
            print(url)
            print(consolidated)
            print(statement_type.title())
            print('---------------------------------------')
        x += 1


# statements('000101872422000005')
# for each in assc_no_list[0:11]:

#     print(each)
#     statements(each)


url = 'https://www.sec.gov/Archives/edgar/data/' + \
    cik + '/' + assc_num + '/R' + r_number + '.htm'
print(url)
headers = {'User-Agent': "BB Company, bab385@gmail.com",
           "Accept-Encoding": "gzip, deflate"}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('table', class_="report")
# print(table.prettify())
rows = table.find_all('tr')
statement_title = rows[0].find('strong').text

pattern = re.compile(r'\d\d\d\d')
header_cells = table.find_all('th')
date_array = []
for date in header_cells:
    matches = pattern.findall(date.text)
    for this in matches:
        date_text = date.text
        formatted_date = datetime.datetime.strptime(
            date_text, '%b. %d, %Y').date()
        formatted_date = str(formatted_date)
        date_array.append(formatted_date)
print(date_array)
print(len(date_array))

# date_cells = rows[1].find_all('th')
# date_array = []
# for date in date_cells:
#     date_text = date.text
#     formatted_date = datetime.datetime.strptime(date_text, '%b. %d, %Y').date()
#     formatted_date = str(formatted_date)
#     print(formatted_date)
#     date_array.append(formatted_date)
# print(date_array)

financials_array = []
y = 1
for row in rows[2:]:
    cells = list(row.children)
    value1 = cells[3].text.strip().replace('$ ', '').replace(',', '')
    if value1.startswith('('):
        value1 = value1.replace('(', '-').replace(')', '')
    if value1 != "":
        value1 = float(value1)

    value2 = cells[5].text.strip().replace('$ ', '').replace(',', '')
    if value2.startswith('('):
        value2 = value2.replace('(', '-').replace(')', '')
    if value2 != "":
        value2 = float(value2)

    value3 = cells[7].text.strip().replace('$ ', '').replace(',', '')
    if value3.startswith('('):
        value3 = value3.replace('(', '-').replace(')', '')
    if value3 != "":
        value3 = float(value3)

    if value1 == "" and value2 == "" and value3 == "":
        header = True
    else:
        header = False

    financials_array.append({
        'line': y,
        'header': header,
        'Description': cells[1].text,
        'financials': {date_array[0]: value1,
                       date_array[1]: value2,
                       date_array[2]: value3}})
    y += 1
print(json.dumps(financials_array, indent=4))
# financials_array = json.dumps(financials_array)

# df = pd.json_normalize(financials_array,
#                        record_path=['financials'],
#                        meta=['line', 'header', 'Description'])

df = pd.DataFrame(financials_array)
print(df)
