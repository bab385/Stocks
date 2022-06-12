import requests
from bs4 import BeautifulSoup
import pandas as pd

cik = '320193'
assc_num = '000032019318000145'
r_number = '9'
# 2 - income, 5 - balance sheet, 9 - cash flow


def headers():
    x = 1
    while x < 68:
        print(x)
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
        print(statement_type)
        x += 1


# headers()


def pageContent(cik, assc_num, r_number):
    cik = cik
    assc_num = assc_num
    r_number = r_number
    url = 'https://www.sec.gov/Archives/edgar/data/' + \
        cik + '/' + assc_num + '/R' + r_number + '.htm'
    headers = {'User-Agent': "BB Company, bab385@gmail.com",
               "Accept-Encoding": "gzip, deflate"}
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)

    tables = soup.find_all("table")

    my_table = tables[0]

    headers = my_table.findChildren('th')

    # financial statement title
    statement_type = headers[0].text
    print(statement_type)

    # array of dates for each column
    dates = []
    for each in headers:
        dates.append(each.text)
    dates.pop(0)
    print(len(dates))

    rows = my_table.findChildren(['th', 'tr'])
    total_array = []

    for row in rows:
        cells = row.findChildren('td')
        if cells == []:
            continue
            # else:
        cell_array = []
        for cell in cells:
            cell_array.append(cell.text)
        total_array.append(cell_array)

    def charReplace(string):
        x = 0
        for one in total_array:
            y = 0
            for two in one:
                total_array[x][y] = two.replace(string, "")
                y += 1
            x += 1

    charReplace('\n')
    charReplace('$ ')
    charReplace('\xa0')
    # if len(dates) == 1:
    #     columns = ['Description', dates[0]]
    # elif len(dates) == 2:
    #     columns = ['Description', dates[0], dates[1]]
    # elif len(dates) == 3:
    #     columns = ['Description', dates[0], dates[1], dates[2]]
    # elif len(dates) == 4:
    #     columns = ['Description', dates[0], dates[1], dates[2], dates[3]]
    # elif len(dates) == 5:
    #     columns = ['Description', dates[0],
    #                dates[1], dates[2], dates[3], dates[4]]
    # elif len(dates) == 6:
    #     columns = ['Description', dates[0], dates[1],
    #                dates[2], dates[3], dates[4], dates[5]]
    # df = pd.DataFrame(total_array, columns=columns)
    df = pd.DataFrame(total_array)
    print(df)


pageContent(cik, assc_num, r_number)
