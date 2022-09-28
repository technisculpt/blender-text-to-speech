import csv
import os

def list2csv(list, csv_name):
    with open(csv_name + '.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for item in list:
            writer.writerow(item)

def dir2csv(path, csv_name):
    for (dirpath, dirnames, filenames) in os.walk(path):
        with open(csv_name + '.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            for file in dirnames:
                writer.writerow([[file], ['dir']])
            for file in filenames:
                writer.writerow([[file], ['file']])
        break

def csv2list(path: list) -> list:
    with open(path + '.csv', 'rt') as f:
        csv_reader = csv.reader(f)
        csv_list = []
        for line in csv_reader:
            if len(line) > 0:
                csv_list.append(line)
        return csv_list
