# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:21:05 2018

@author: Asus
"""
from word import Word
import itertools as it
import pandas as pd

def generate(length, n):
    b = [(e,1) for e in range(n)]
    b.extend([(e,-1) for e in range(n)])
    for data in it.product(b, repeat=length):
        w = Word()
        w.symbols = data
        w = w.reduce(n)
        if w.length() < length:
            continue
        if w.totpow()<0:
            yield w.inverse().reduce(n)
        else:
            yield w
            
def make_dictionary(length, cycle):
    data = []
    for l in range(1, length + 1):
        for index, w in enumerate(generate(l, cycle)):
            if index%1000 == 0:
                print('\rlength:{0} w:{1}   '.format(l, index), end='')
            data.append(str(w))
    print()
        
    df = pd.DataFrame(data, columns=['form']).set_index('form')
    df = df[~df.index.duplicated(keep='first')]
    df.to_csv('outputs/dict{0}.csv'.format(length))
    
    return df

def read_dictionary(length):
    df = pd.read_csv('outputs/dict{0}.csv'.format(length))
    df['word'] = df['form'].apply(lambda x: Word(x))
    return df