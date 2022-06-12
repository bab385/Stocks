import requests
import datetime
import csv
import pandas as pd

from django.shortcuts import render
from django.core import serializers
from .models import Company, AccnNumber, StatementFields


def index(request):
    return render(request, 'main/index.html', {
    })


def income(request, symbol):
    return render(request, 'main/alpha.html', {

    })


def companies(request):
    companies = Company.objects.all().order_by('ticker')
    return render(request, 'main/companies.html', {
        'companies': companies,
    })


def company(request, pk):
    company = Company.objects.get(id=pk)
    accn_nums = AccnNumber.objects.filter(cik=company)
    return render(request, 'main/company_main.html', {
        'company': company,
        'accn_nums': accn_nums,
    })

# changed to financials 1 so i could mess around


def financials1(request, pk):
    # gives me company and accn numbers from database
    company = Company.objects.get(id=pk)
    accn_nums = AccnNumber.objects.filter(cik=company)

    # add 0s to the beginning of the cik to get to 10 digits. Needed for URL
    cik_num = company.cik
    while len(cik_num) < 10:
        cik_num = '0' + cik_num

    # make the URL request to get the financial data and return json info
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_num}.json"
    print(url)
    headers = {'User-Agent': "BB Company, bab385@gmail.com",
               "Accept-Encoding": "gzip, deflate"}
    r = requests.get(url, headers=headers)
    data = r.json()

    # get a list of fields
    fields = []
    for each in data['facts']['us-gaap']:
        fields.append(each)

    current_asset_list = []
    current_assets = StatementFields.objects.filter(
        header='CA').order_by('line_number').values_list()

    for each in current_assets:
        each = list(each)
        current_asset_list.append(each[2])
    print(current_asset_list)

    values = data['facts']['us-gaap']['AccountsPayableCurrent']['units']['USD']
    # value_list = []
    # unique_filed_dates = set()
    unique_end_dates = set()
    for value in values:
        if value['form'] == '10-K' or value['form'] == '10-K/A':

            # get list of unique end dates
            unique_end_dates.add(value['end'])

            # line = {'end': value['end'],
            #         'value': value['val'],
            #         'filed': value['filed']}
            # value_list.append(line)

    unique_end_dates = list(unique_end_dates)
    unique_end_dates.sort(reverse=True)

    print(unique_end_dates)
    final_list = []

    def field_values(field):
        # get first unique end date and find latest filing date.
        latest_filing = ""
        latest_filings = []
        for end_date in unique_end_dates:
            # end_date = unique_end_dates[1]
            latest_filed_date = ""
            parent_dict = {}
            values = data['facts']['us-gaap'][field]['units']['USD']
            for value in values:

                if value['form'] == '10-K' or value['form'] == '10-K/A':

                    if value['end'] == end_date:
                        # finds the most recent filed date for each end date
                        if latest_filed_date == "" or value['filed'] > latest_filed_date:
                            latest_filed_date = value['filed']
                            # value['field'] = 'AccountsPayableCurrent'
                            latest_filing = value
            latest_filings.append(latest_filing)
        parent_dict[field] = latest_filings
        final_list.append(parent_dict)

        # for key, value in parent_dict.items():
        # print(key, value)
    for current_asset in current_asset_list:
        try:
            field_values(current_asset)
        except:
            pass

    # send the data to the html page
    return render(request, 'main/financials.html', {
        'company': company,
        'fields': fields,
        'filings': final_list,
        'end_dates': unique_end_dates,
    })


def financials(request, pk):
    # gives me company and accn numbers from database
    company = Company.objects.get(id=pk)
    accn_nums = AccnNumber.objects.filter(cik=company)

    # add 0s to the beginning of the cik to get to 10 digits. Needed for URL
    cik_num = company.cik
    while len(cik_num) < 10:
        cik_num = '0' + cik_num

    # make the URL request to get the financial data and return json info
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_num}.json"
    print(url)
    headers = {'User-Agent': "BB Company, bab385@gmail.com",
               "Accept-Encoding": "gzip, deflate"}
    r = requests.get(url, headers=headers)
    data = r.json()

    # get a list of fields
    fields = []
    for each in data['facts']['us-gaap']:
        fields.append(each)

    current_asset_list = []
    current_assets = StatementFields.objects.filter(
        header='CA').order_by('line_number').values_list()

    for each in current_assets:
        each = list(each)
        current_asset_list.append(each[2])
    print(current_asset_list)

    # create a list of unique end dates
    values = data['facts']['us-gaap']['AccountsPayableCurrent']['units']['USD']
    unique_end_dates = set()
    for value in values:
        if value['form'] == '10-K' or value['form'] == '10-K/A':

            # get list of unique end dates
            unique_end_dates.add(value['end'])

    unique_end_dates = list(unique_end_dates)
    unique_end_dates.sort(reverse=True)

    print(unique_end_dates)

    final_list = []
    latest_filings = []
    for field in current_asset_list:
        # get first unique end date and find latest filing date.
        latest_filing = ""

        for end_date in unique_end_dates:
            # end_date = unique_end_dates[1]
            latest_filed_date = ""
            parent_dict = {}
            try:
                values = data['facts']['us-gaap'][field]['units']['USD']
                for value in values:

                    if value['form'] == '10-K' or value['form'] == '10-K/A':

                        if value['end'] == end_date:
                            # finds the most recent filed date for each end date
                            if latest_filed_date == "" or value['filed'] > latest_filed_date:
                                latest_filed_date = value['filed']
                                # value['field'] = 'AccountsPayableCurrent'
                                value['field'] = field
                                value['val'] = value['val']/1000

                                latest_filing = value
                if latest_filing != "":
                    latest_filings.append(latest_filing)
            except:
                pass

    df = pd.DataFrame(latest_filings)

    df = df[['field', 'end', 'val']]
    df = df.pivot_table(index="field", columns="end",
                        values="val", fill_value=10)
    df = df.sort_index(axis=1, ascending=False)
    # df = df.style.format({'val': '{0:,}'}) THIS DIDN'T WORK
    df_list = df.to_dict()
    df2 = df.to_html(classes="table table-bordered table-hover")
    print(df_list['2020-12-31'])

    # send the data to the html page
    return render(request, 'main/financials_df.html', {
        'company': company,
        'fields': fields,
        'filings': final_list,
        'end_dates': unique_end_dates,
        'df': df2,
    })
