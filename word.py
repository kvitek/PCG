# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 13:58:54 2018

@author: Asus
"""

class Word(object):
    def __init__(self, s_word=None):
        self.letter = 'a'
        self.symbols = []
        if s_word is not None:
            self.read(s_word)
        
    def __str__(self):
        s = ''
        for e in self.symbols:
            if e[1] == 1:
                s += self.letter + '{0}*'.format(e[0])
            else:
                s += self.letter + '{0}**{1}*'.format(e[0],e[1])
        return s[:-1]
    
    def __eq__(self, w):
        if len(w.symbols) != len(self.symbols):
            return False
        for (e1, pw1), (e2, pw2) in zip(self.symbols, w.symbols):
            if e1 != e2 or pw1 != pw2:
                return False
        return True
    
    def read(self, s_word):
        s = s_word.replace('**','^')
        s = s.split('*')
        self.symbols = []
        
        for e in s:
            e = e.split('^')
            if len(e)==2:
                self.symbols.append((int(e[0][1:]), int(e[1])))
            else:
                self.symbols.append((int(e[0][1:]), 1))
        return
    
    def inverse(self):
        w = Word()
        w.symbols = [(e[0],-e[1]) for e in reversed(self.symbols)]
        return w
    
    def simplify(self):               
        simple = [a for a in self.symbols]
        
        dosmt = True
        while dosmt:
            simpler = []
            if len(simple) == 0:
                break
        
            dosmt = False
            cur_symb = list(simple[0])
            for i in range(1, len(simple)):
                if simple[i][0] == cur_symb[0]:
                    dosmt = True
                    cur_symb[1] += simple[i][1]
                else:
                    if cur_symb[1] != 0:
                        simpler.append((cur_symb[0], cur_symb[1]))
                    cur_symb = list(simple[i])
            
            if cur_symb[1] != 0: simpler.append(cur_symb)
            
            simple = simpler
        
        w = Word()
        w.symbols = simple
        return w
    
    def order(self, cycle):
        new_order = [e for e in self.symbols]
        for j in range(1, len(new_order)):
            for i in range(0, len(new_order)-j):
                if (new_order[i][0] - new_order[i+1][0] == 1 or
                   new_order[i][0] - new_order[i+1][0] == (cycle-1)):
                    new_order[i], new_order[i+1] = new_order[i+1], new_order[i]
        
        w = Word()
        w.symbols = new_order
        
        return w
        
    def mul(self, right):
        w = Word()
        w.symbols.extend(self.symbols)
        w.symbols.extend(right.symbols)
        return w
    
    def reduce(self, cycle):        
        w = self.simplify()
        while True:            
            for letter in range(cycle-1, -1, -1):
                pos = []
                for i, (s,pw) in enumerate(w.symbols):
                    if s == letter: pos.append(i)
                for p in pos:
                    for i in range(p, 0, -1):
                        if (abs(w.symbols[i-1][0] - w.symbols[i][0]) == 1 or
                            abs(w.symbols[i-1][0] - w.symbols[i][0]) == cycle-1):
                            w.symbols[i-1], w.symbols[i] = w.symbols[i], w.symbols[i-1]
                        else:
                            break
            v = w.simplify()
            if v == w: break
            else: w = v
            
        return v
    
    def totpow(self):
        return sum([pw for (e,pw) in self.symbols])
    
    def length(self):
        return sum([abs(pw) for (e,pw) in self.symbols])
    
    def isidentity(self):
        return (len(self.symbols) == 0)
    
    __repr__ = __str__



