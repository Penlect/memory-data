
import pandas as pd

df = pd.read_excel('/home/penlect/Downloads/words/Words-TURKISH.xls',
                   sheet_name='Words')

df_turk = df[['Part of Speech', 'DANISH', 'ENGLISH', 'TURKISH']]

df = pd.read_excel('/home/penlect/Downloads/words/ITA_EUROPEAN_WORDS_2018 Stage 04.xls',
                   sheet_name='Words')

df_ital = df[['Part of Speech', 'ITALIAN']]

df = pd.read_excel('/home/penlect/Downloads/words/EUROPEAN_WORDS_2018-Stage-04_UKR.xls',
                   sheet_name='Words')

df_ukra = df[['Part of Speech', 'UKRAINIAN']]

df = pd.read_excel('/home/penlect/Downloads/words/EUROPEAN_WORDS_2018 Stage 04_FR.xls',
                   sheet_name='Words')

df_fren = df[['Part of Speech', 'FRENCH']]

df = pd.read_excel('/home/penlect/Downloads/words/WORDS_Polish_Translation.xls',
                   sheet_name='Words')

df_pols = df[['Part of Speech', 'POLISH']]

df = pd.read_excel('/home/penlect/Downloads/words/[European] German Translations - Words & Dates.xlsx',
                   sheet_name='Final Words')

df_germ = df[['Part of Speech', 'GERMAN']]


x = pd.concat([
    df_turk['Part of Speech'],
    df_turk['DANISH'],
    df_turk['ENGLISH'],
    df_turk['TURKISH'],
    df_ital['ITALIAN'],
    df_ukra['UKRAINIAN'],
    df_fren['FRENCH'],
    df_pols['POLISH'],
    df_germ['GERMAN']
    ], axis=1)
x.index += 2
delete_us = [
    # FR
    47, 48, 69, 126, 129, 130, 245, 261, 276, 284, 291, 316, 392, 393, 394, 395, 396, 397, 406, 413, 435, 449, 450, 457, 468, 469, 470,

    # UKR
    47, 48, 277, 280, 284, 285, 297, 392, 393, 394, 395, 396, 397, 406, 457, 468, 469, 470,

    # ITA
    47, 48, 83, 126, 130, 193, 261, 280, 284, 291, 297, 310, 392, 393, 394, 395, 396, 397, 406, 457, 468, 469, 470,

    # POLISH
    47, 48, 83, 126, 130, 194, 280, 284, 285, 291, 297, 310, 314, 340, 354, 392, 393, 394, 395, 396, 397, 406, 457, 468, 469, 470,

    # TURK
    6, 47, 48, 88, 119, 126, 130, 138, 165, 175, 225, 246, 259, 392, 393, 394, 395, 396, 397, 406, 457, 468, 469, 470,

    # Has spaces
    #23, 25, 45, 51, 57, 57, 72, 74, 98, 103, 104, 106, 106, 117, 141, 186, 191, 235, 236, 270, 288, 296, 328, 357, 359, 368, 373, 382, 401, 403, 404, 404, 427, 429, 437, 445, 453, 455, 455, 467
]



from collections import Counter
dup_words = list()
for key in x:
    print(key)
    data = list(x[key])
    c = Counter(data)
    v = {k: v for k, v in c.items() if v > 1}
    dup_words += list(v.keys())

def has_spaces(df):
    space_words = list()
    for index, row in df.iterrows():
        for word in row[1:]:
            if isinstance(word, float):
                space_words.append(index)
                break
            word = word.strip()
            if '-' in word or word in dup_words or len(word.split()) > 2:
                space_words.append(index)
                print(word)
                break
    return space_words

delete_us = has_spaces(x)
print('has spaces', delete_us)

x = x.drop(x.index[[i - 2 for i in delete_us]])

x['Part of Speech'] = list(map(lambda i: i.upper().strip(), x['Part of Speech']))

print(x.to_string())


print(x['Part of Speech'].value_counts())

print(len(x))

from collections import Counter
for key in x:
    break
    print(key)
    data = list(x[key])
    c = Counter(data)
    print({k: v for k, v in c.items() if v > 1})
    print(len(data), len(set(data)))
    print(list(x[x[key].duplicated()].index))
    print()

w = pd.ExcelWriter('all_words.xls')
x.to_excel(w, 'Words')
w.save()