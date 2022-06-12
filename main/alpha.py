import requests
from datetime import datetime

# def incomeStatement(compSymbol):
#     url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=' + \
#         compSymbol + '&apikey=V7FD62Y8E2LZYG05'
#     r = requests.get(url)
#     data = r.json()

#     return(data)


#newStock = incomeStatement('AAPL')
# print(newStock)

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    #print(abs((d2 - d1).days))
    return abs((d2 - d1).days)


def secStuff():
    url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json'
    headers = {'User-Agent': "BB Company, bab385@gmail.com",
               "Accept-Encoding": "gzip, deflate"}
    r = requests.get(url, headers=headers)
    data = r.json()

    # dictionary of each financial item reported
    financial_list = data['facts']['us-gaap']

    netincome = data['facts']['us-gaap']['NetIncomeLoss']['units']['USD']

    # get set of each unique file date for 10-Ks and amended 10-Ks to cycle through
    j = 0
    unique_file_dates = set()
    for each in netincome:
        record = netincome[j]
        if (record['form'] == '10-K' or record['form'] == '10-K/A'):
            file_date = record['filed']
            unique_file_dates.add(file_date)
        j += 1

    # print('Set of Unique File Dates:')
    # print(unique_file_dates)

    # get set of each unique period end date for 10-Ks and amended 10-Ks to cycle through
    k = 0
    unique_per_end_dates = set()
    for each in netincome:
        record = netincome[k]
        # filter out any quarterly data that is in the 10-K
        record_end = record['end']
        record_start = record['start']
        duration = days_between(record_end, record_start)
        if (record['form'] == '10-K' or record['form'] == '10-K/A') and duration > 325:
            # print(each)
            end_date = record['end']
            unique_per_end_dates.add(end_date)
        k += 1

    # print('Set of Unique Period End Dates for Annual Items:')
    # print(unique_per_end_dates)

    i = 0
    filed_date_list = []
    for each in netincome:
        # print(each)
        this = netincome[i]
        # want to cycle through the unique_file_dates and put here at end
        if (this['form'] == '10-K' or this['form'] == '10-K/A') and this['end'] == '2019-09-28':
            filed_date = datetime.strptime(this['filed'], "%Y-%m-%d")
            filed_date_list.append(filed_date)
        i += 1
    print(filed_date_list)
    most_recent_file_date = str(max(filed_date_list))
    print(most_recent_file_date)

    y = 0
    final_array = []
    for each in netincome:
        this = netincome[y]
        if this['form'] == '10-K' or this['form'] == '10-K/A':
            z = 0
            for end in unique_per_end_dates:
                latest = None
                if this['end'] == end:
                    filed_date = datetime.strptime(this['filed'], "%Y-%m-%d")
                    if latest == None or filed_date > latest:
                        latest = datetime.strptime(this['filed'], "%Y-%m-%d")
                z += 1
            print(latest, ' --. ', this)
        y += 1
    # for each in netincome:


secStuff()

# 'https://data.sec.gov/submissions/CIK##########.json'
# https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json
