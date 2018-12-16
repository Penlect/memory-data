
import os

for path, dirs, files in os.walk('.'):
    for file in files:
        if file == 'google_translate.txt':
            print(os.path.basename(path))
        else:
            continue
        full_file = os.path.join(path, file)
        with open(full_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            for i in range(len(lines)):
                if '-' in lines[i]:
                    lines[i] = ''

        with open(full_file, 'w', encoding='utf-8') as f:
            f.write(''.join(lines))