# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 22:11:28 2018

@author: Asus
"""
from word import Word

def rho_new(w, cycle):
    new = Word()
    new.symbols = []
    for (e, pw) in w.symbols:
        new.symbols.append((cycle - e -1, pw))
    return new