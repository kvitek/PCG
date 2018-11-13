# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:19:11 2018

@author: Asus
"""

from word import Word
from multiprocessing import Pool
import os
import dictionary as ddict


            
def process_words(length, cycle, rho, istart, iend):    
    f = open('outputs/wg/wg{0}-{1}-{2}.txt'.format(length, istart, iend), 'w')
    wdict = ddict.read_dictionary(length)
    
    data = []
    for g_index, g_row in enumerate(wdict.iloc[istart:iend].iterrows()):
        g = g_row[1]['word']    
        for w_index, w_row in enumerate(wdict.iterrows()):
            w = w_row[1]['word']
            rho_w = rho(w, cycle)
            res = rho_w.inverse().mul(g.inverse()).mul(w).mul(g)
            res = res.reduce(cycle)
            if res.isidentity():
                data.append([str(w), str(g)])
                print()
                print(w, g)
                f.write('{0}\t{1}\n'.format(str(w), str(g)))
                f.flush()
                
            if w_index%1000 == 0: 
                print('\rg_index:{0} w_index:{1} w:{2} g:{3}               '
                      .format(g_index + istart, w_index, w, g), end='')
    f.close()
    return 'end with range:{0}-{1}'.format(istart, iend)


if __name__ == '__main__':
    cpus = os.cpu_count() - 1
    params = []
    start, end, step = 1000, 5000, 100
    for i in range(start, end, step):
        params.append([6, 6, rho_new, i, i + step])    
    with Pool(cpus) as p:
        print(p.starmap(process_words, params))  