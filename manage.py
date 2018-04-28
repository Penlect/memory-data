
from pathlib import Path
import os

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

def read_total_recall_words(file):
    d = dict()
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            row_data = line.rstrip().split(',')
            lang, class_, word = row_data
            d.setdefault(lang, dict()).setdefault(class_, list()).append(word)

    d.pop('swedish')
    for lang, c2w in d.items():
        for class_, words in c2w.items():
            os.makedirs(f'words/{lang}', exist_ok=True)
            with open(f'words/{lang}/{class_}.txt', 'w', encoding='utf-8') as out:
                out.write('\n'.join(sorted(words)))


if __name__ == '__main__':
    from pprint import pprint

    read_total_recall_words('words/total_recall.txt')
