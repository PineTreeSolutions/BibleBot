# Copyright (C) 2022 NuclearPine
import re
import pandas as pd

def parse_ref(query):

    kjv = pd.from_csv('kjv.tsv', sep='\t') # load KJV into a pandas dataframe
    kjv.columns = ['book', 'book_abr', 'book_num', 'chapter', 'verse', 'text']

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
    x = re.search('^[1-9]?[a-zA-Z ]+', query)
    if x:
        ref['book'] = x.group().lower().rstrip()
        print('Book: ' + ref['book'])
        query = query[x.span()[1]:]
    else:
        return(False)

    # find chapter
    query = re.sub('^:', '', query).lstrip()
    x = re.search('^[1-9]+[0-9]*', query)
    if x:
        ref['chapter'] = x.group()
        print('Chapter: ' + ref['chapter'])
        query = query[x.span()[1]:].lstrip()
    else:
        return('You need to specify a chapter')
    
    # find starting verse
    query = re.sub('^:', '', query).lstrip()
    x = re.search('^[1-9]+[0-9]*', query)
    if x: #case 2, 3
        ref['verse'] = x.group()
        ref['exact'] = True
        print('Start verse: ' + ref['verse'])
        query = query[x.span()[1]:].lstrip()
    elif query == '': # case 1
        ref['exact'] = False
        return ref
    else:
        return(False)

    x = re.search('^-[1-9]+[0-9]*$', query)
    if x: # case 3
        ref['verse_end'] = re.sub('^-', '', x.group())
        print('End verse: ' + ref['verse_end'])
        return ref
    elif query == '': # case 2
        ref['verse_end'] = ref['verse']
        print('End verse: ' + ref['verse_end'])
        return ref
    else:
        return(False)
