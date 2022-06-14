import requests

base_url = 'https://www.sec.gov/files/dera/data/financial-statement-data-sets/'

year = 2022
years = []
while year > 2008:
    years.append(str(year))
    year -= 1

print(years)

quarters = ['q1', 'q2', 'q3', 'q4']
quarters.sort(reverse=True)

data_list = []

for year in years:
    for quarter in quarters:
        data = year + quarter
        data_list.append(data)

print(data_list)

# commented out section below because this will write to a file. Uncomment to use

# for each in data_list:
#     end_url = each + '.zip'
#     url = base_url + end_url
#     print(url)

#     response = requests.get(url)
#     open('D:\Stock_Data' + f'\{end_url}', 'wb').write(response.content)

#     print(end_url + ' ---> download complete!')
