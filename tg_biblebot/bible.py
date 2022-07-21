# Copyright (C) 2022 NuclearPine
import re
import pandas as pd

kjv = pd.read_csv('kjv.tsv', sep='\t', index_col='index') # load KJV into a pandas dataframe

def regex(input):

    ref = {
        'book' : None,
        'chapter' : None,
        'verse' : None,
        'verse_end' : None,
        'exact' : False
    }
    
    # 1. <book>:?<chapter>
    # 2. <book>:?<chapter>:<verse>
    # 3. <book>:?<chapter>:<verse>-<verse>

    # find book
    x = re.search('^[1-9]?[a-zA-Z ]+', input)
    if x:
        ref['book'] = x.group().lower().rstrip()
        input = input[x.span()[1]:]
    else:
        return('Invalid syntax: book name')

    # find chapter
    input = re.sub('^:', '', input).lstrip()
    x = re.search('^[1-9]+[0-9]*', input)
    if x:
        ref['chapter'] = int(x.group())
        input = input[x.span()[1]:].lstrip()
    else:
        return('Invalid syntax: chapter number')
    
    # find starting verse
    input = re.sub('^:', '', input).lstrip()
    x = re.search('^[1-9]+[0-9]*', input)
    if x: #case 2, 3
        ref['verse'] = int(x.group())
        ref['exact'] = True
        input = input[x.span()[1]:].lstrip()
    elif input == '': # case 1
        ref['exact'] = False
        return ref
    else:
        return('Invalid syntax: verse number')

    # find ending verse
    x = re.search('^-[1-9]+[0-9]*$', input)
    if x: # case 3
        ref['verse_end'] = int(re.sub('^-', '', x.group()))
        return ref
    elif input == '': # case 2
        ref['verse_end'] = ref['verse']
        return ref
    else:
        return('Invalid syntax: verse number')

def fetch_verses(input):
    ref = regex(input)
    if type(ref) != dict:
        return ref

    book_num = 0
    if kjv.book_abr.eq(ref['book']).any():
        book_num = kjv[kjv.book_abr == ref['book']].iloc[0].book_num
    elif kjv.book.eq(ref['book']).any():
        book_num = kjv[kjv.book == ref['book']].iloc[0].book_num
    else:
        return 'Invalid book name'
    df = kjv[kjv.book_num == book_num]

    if not df.chapter.eq(ref['chapter']).any():
        return 'Invalid chapter'
    df = df[df.chapter == ref['chapter']]

    if not (df.verse.eq(ref['verse']).any() & df.verse.eq(ref['verse_end']).any()):
        return 'Invalid verse selection'
    verses = df[(df.verse >= ref['verse']) & (df.verse <= ref['verse_end'])]

    message = ''
    for i, j in zip(verses.verse, verses.text):
        message += f'<b>{i}.</b> {j}\n'
    
    return message