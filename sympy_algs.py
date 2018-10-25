# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:23:30 2018

@author: Asus
"""
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
import itertools as it
import pandas as pd

def Gn(n):
    params = ''
    for i in range(0, n):
        params += 'a' + str(i) + ','
    params = params[0:-1]
    
    t = free_group(params)
    F = t[0]
    a = t[1:]
    
    relations = []
    for i in range(0,n-1):
        relations.append(a[i]*a[i+1]*a[i]**(-1)*a[i+1]**(-1))
    relations.append(a[n-1]*a[0]*a[n-1]**(-1)*a[0]**(-1))
    
    G = FpGroup(F, relations)
    return G, a

def rho(word, G):
    #n even reflection no fixed points
    a = G.generators
    n = len(a)
    arr_form = list(word.array_form)
    for i, (letter, pw) in enumerate(arr_form):
        index = int(str(letter)[1:])
        arr_form[i] = (a[n - index - 1], pw)
    
    val = G.identity
    for letter, pw in arr_form:
        val = val*pow(letter, pw)
    
    return val

def rho1(word, G):
    #n even reflection 2 fixed points
    #n odd reflection 1 fixed point
    a = G.generators
    n = len(a)
    arr_form = list(word.array_form)
    for i, (letter, pw) in enumerate(arr_form):
        index = int(str(letter)[1:])
        arr_form[i] = (a[(n - index)%n], pw)
    val = G.identity
    for letter, pw in arr_form:
        val = val*pow(letter, pw)
    
    return val

def sigma(word, r, G):
    #rotation on r
    a = G.generators
    n = len(a)
    arr_form = list(word.array_form)
    for i, (letter, pw) in enumerate(arr_form):
        index = int(str(letter)[1:])
        arr_form[i] = (a[(index + r)%n], pw)
    
    val = G.identity
    for letter, pw in arr_form:
        val = val*pow(letter, pw)
        
    return val

def generate(length, G):
    b = []
    b.extend(G.generators)
    b.extend([e**-1 for e in G.generators])
    
    for current_word in it.product(b, repeat=length):
        w = G.identity
        for e in current_word: w = w*e
#        w = G.reduce(w)
        if len(w.letter_form) < length:
            continue
        
        yield w        
    return

def make_dictionary(length, G):
    data = []
    for index, word in enumerate(generate(length, G)):
        print('\r{0}'.format(index), end='')
        data.append([word])    
    print()
    
    df = pd.DataFrame(data, columns=['form'])
    df['form'] = df['form'].apply( lambda x: str(G.reduce(x)) )
    df.set_index('form', inplace=True)
    df = df[~df.index.duplicated(keep='first')]
    
    df.to_csv('outputs/w{0}.csv'.format(length))
    
    return df