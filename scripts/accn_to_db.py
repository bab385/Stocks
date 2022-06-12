import csv
import datetime
from main.models import AccnNumber, Company, ReportType


def run():
    with open('main/accn_num_all_2022_06_04.csv') as file:
        reader = csv.reader(file)
        next(reader)
        reader = list(reader)
        # print(reader[0])
        new_list = []

        # check_list is for verifying that a batch does not have duplicates in it
        check_list = []

        # to run through rows in smaller batches
        x = 0
        increment = 10000

        for row in reader[x:x+increment]:
            # excel modifies the date, so this gets it back to db form
            date_filed = datetime.datetime.strptime(
                row[1], ('%m/%d/%Y')).date()

            # needed for the foreign key relationships in the new instances
            company = Company.objects.filter(cik=row[4])
            report = ReportType.objects.get(report_type=row[2])

            # creates the new instance for the db
            each = AccnNumber(filed_date=date_filed,
                              report_type=report,
                              accn=row[3],
                              cik=company[0])

            # creates the list item for checking for duplicates in a batch
            dict_value = {'cik': company[0], 'accn': row[3]}

            # exists checks to see if an instance already exists in the db
            exists = AccnNumber.objects.filter(accn=row[3], cik=company[0])
            exists = list(exists)

            # if exists in a blank list, the instance does not exist in the db
            if exists == []:
                print(each)

                # checks to see if there is a duplicate in the batch
                if dict_value in check_list:
                    continue

                # create a list of instances for pushing to db
                new_list.append(each)
                check_list.append(dict_value)
                print(x)
                x += 1
        print(new_list)
        AccnNumber.objects.bulk_create(new_list, batch_size=1000)
