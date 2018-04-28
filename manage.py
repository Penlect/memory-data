
from pathlib import Path


def read_names_log_file(file):
    lastnames = set()
    firstnames = dict()
    with open(file, 'r') as f:
        for line in f:
            row_data = line.rstrip().split(';')
            _, date, url, firstname, lastname = row_data
            gender = int(Path(url).stem[0])
            gender = 'male' if gender == 1 else 'female'
            firstnames.setdefault(gender, set()).add(firstname)
            lastnames.add(lastname)
    return lastnames, firstnames


def read_historical_log_file(file):
    unique = set()
    with open(file, 'r') as f:
        for line in f:
            unique.add(line.rstrip().split(';')[-1])
    with open('german_mc', 'w') as f:
        f.write('\n'.join(sorted(unique)))


if __name__ == '__main__':
    from pprint import pprint

    read_historical_log_file('../historical/de_historical.log')
