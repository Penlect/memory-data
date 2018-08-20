import textract
from collections import Counter

c = Counter()

text = textract.process("/home/penlect/Downloads/How to remember names and faces the easy way-Final.pdf", encoding='utf-8')

index = text.find(b'USA Female Names')
text = text[index:]

file = None
count = 0
lines = list()
for line in text.decode('utf8').split('\n'):
    if line.strip() and '–' in line:
        count += 1
        name = line.split('–')[0].strip()
        name = name.replace(' ', '-')
        #print(f'{count: 3} ', name)
        lines.append(name)
    elif 'Names' in line:
        lines = list(set(lines))
        count = 0
        if file is not None:
            lines.sort()
            print(f'Writing {len(lines)} lines to {file.name}')
            file.write('\n'.join(lines))
            lines = list()
            file.close()
        print(f'{line:-^100}')
        file = open(f'{line.replace(" ", "_")}.txt', 'w', encoding='utf8')
print(f'Writing {len(lines)} lines to {file.name}')
file.write('\n'.join(lines))
file.close()