
from pathlib import Path
import os
import hashlib

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

    for class_, words in d['swedish'].items():

        with open(f'words/swedish/{class_}.txt', 'r', encoding='utf-8') as out:
            old_words = [w.rstrip() for w in out.readlines() if w.strip()]

        words = set(words) | set(old_words)

        with open(f'words/swedish/{class_}.txt', 'w', encoding='utf-8') as out:
            out.write('\n'.join(sorted(words)))

def sort_and_unique_lines(file):
    with open(file, 'r', encoding='utf-8') as f:
        liens = [x.strip() for x in f.readlines()]
        uni = list(sorted(set(liens)))
        print(file, len(liens), len(uni))
    with open(file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(uni))


def rename_files(path, gender):

    files = list(Path(path).iterdir())
    for file in files:
        if not file.suffix == '.jpg':
            raise Exception('Wrong suffix: %s' % file)

    gender = int(gender)
    assert gender in {0, 1, 2}

    f2h = dict.fromkeys(files)
    for file in f2h:
        m = hashlib.md5()
        with open(file, 'rb') as img:
            m.update(img.read())
            f2h[file] = m.hexdigest()

    seen = set()
    for file, md5 in f2h.items():
        if md5 in seen:
            print('Duplicate: ')



    for file in :
        m = hashlib.md5()
        with open(file, 'rb') as img:
            m.update(img.read())
        gender = file.name.split('-')[0]

        if len(str(file.name)) < 15:
            os.rename(str(file), str(file.with_name(f'{gender}-{m.hexdigest()}{file.suffix}')))



if __name__ == '__main__':

    memocamp_md5_name_images()

