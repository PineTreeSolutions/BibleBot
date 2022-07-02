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
        print('Book: ' + ref['book'])
        input = input[x.span()[1]:]
    else:
        return('You need to specify a book')

    # find chapter
    input = re.sub('^:', '', input).lstrip()
    x = re.search('^[1-9]+[0-9]*', input)
    if x:
        ref['chapter'] = x.group()
        print('Chapter: ' + ref['chapter'])
        input = input[x.span()[1]:].lstrip()
    else:
        return('Invalid syntax: chapter number')
    
    # find starting verse
    input = re.sub('^:', '', input).lstrip()
    x = re.search('^[1-9]+[0-9]*', input)
    if x: #case 2, 3
        ref['verse'] = x.group()
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
        ref['verse_end'] = re.sub('^-', '', x.group())
        print('End verse: ' + ref['verse_end'])
        return ref
    elif input == '': # case 2
        ref['verse_end'] = ref['verse']
        print('End verse: ' + ref['verse_end'])
        return ref
    else:
        return('Invalid syntax: verse number')

def fetch_verses(input): #WIP
    ref = regex(input)
    if type(ref) != dict:
        return ref

