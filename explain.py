# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 12:52:56 2018

@author: Asus
"""

from word import Word
from rhosigma import rho_new
import pandas as pd

words = pd.read_csv('outputs/1000-15000.csv', names=['w', 'g'], sep='\t')

words['w'] = words['w'].apply(lambda x: Word(x))
words['g'] = words['g'].apply(lambda x: Word(x))
words['div'] = words.apply(lambda x: x[0].inverse().mul(x[1]).mul(rho_new(x[1], 6)).reduce(6).isidentity(), axis=1)
#words['ldiv'] = words.apply(lambda x: x[0].inverse().mul(x[1].inverse()).mul(rho_new(x[1].inverse(), 6)).reduce(6).isidentity(), axis=1)


words.to_csv('outputs/1000-15000div.csv', sep='\t')