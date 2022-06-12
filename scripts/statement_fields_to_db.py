import csv
from main.models import StatementFields


def run():
    with open('main/Balance_Sheet.csv') as file:
        reader = csv.reader(file)
        next(reader)
        reader = list(reader)
        for row in reader:
            if row[1] != "Heading":
                if row[5].lower() == 'true':
                    reverse = True
                else:
                    reverse = False
                each = StatementFields(line_number=row[0],
                                       statement_field=row[1],
                                       readable_field=row[2],
                                       header=row[3],
                                       statement=row[4],
                                       reverse=reverse)
                print(each)
                each.save()
