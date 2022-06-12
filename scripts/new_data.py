import csv
import json

with open('2022q1/sub.txt') as f:
    reader = csv.reader(f, delimiter='\t')

    # create a list of headers for dictionary keys
    x = 0
    for line in reader:
        y = 0
        headers = line
        for header in line:
            print(y, '---->', header)
            y += 1
        x += 1
        if x > 0:
            break

    print(headers)

    # initialize a list for the lines
    line_list = []

    for line in reader:
        # get only lines that are for 10-Ks and variants of 10-Ks
        if "10-K" in line[25]:
            # creates a dictionary item for each line in the file
            y = 0
            line_dict = {}
            for each in line:
                line_dict[headers[y]] = each
                y += 1
            line_list.append(line_dict)

    # take new list of dictionaries and format as json
    json_look = json.dumps(line_list, indent=4)
    print(json_look)

# values that I want from the list of information
# 0, 1, 2, 24, 25, 26, 27, 28, 29,

'''
0 ----> adsh
1 ----> cik
2 ----> name
3 ----> sic
4 ----> countryba
5 ----> stprba
6 ----> cityba
7 ----> zipba
8 ----> bas1
9 ----> bas2
10 ----> baph
11 ----> countryma
12 ----> stprma
13 ----> cityma
14 ----> zipma
15 ----> mas1
16 ----> mas2
17 ----> countryinc
18 ----> stprinc
19 ----> ein
20 ----> former
21 ----> changed
22 ----> afs
23 ----> wksi
24 ----> fye
25 ----> form
26 ----> period
27 ----> fy
28 ----> fp
29 ----> filed
30 ----> accepted
31 ----> prevrpt
32 ----> detail
33 ----> instance
34 ----> nciks
35 ----> aciks
'''
