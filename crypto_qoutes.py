#!/usr/bin/env python3

e_phrase = "xtpd zd ltw mbjsl qb nmbg kbch f qsdd fhk t ctuu lgdhk qmd vtslq vbjs lmfsgdhthx qmd fwd"

#print(e_phrase.upper())

decryptor = {'b': 'O',
 'c': 'W',
 'd': 'E',
 'f': 'A',
 'g': 'P',
 'h': 'N',
 'j': 'U',
 'k': 'D',
 'l': 'S',
 'm': 'H',
 'n': 'C',
 'p': 'V',
 'q': 'T',
 's': 'R',
 't': 'I',
 'u': 'L',
 'v': 'F',
 'w': 'X',
 'x': 'G',
 'z': 'M'}
'''
decryptor.update({'t':'I'})
decryptor.update({'q':'T'})

decryptor.update({'f':'A'})
decryptor.update({'d':'E'})
decryptor.update({'s':'R'})
decryptor.update({'m':'H'})
decryptor.update({'h':'N'})
decryptor.update({'k':'D'})
decryptor.update({'x':'G'})
decryptor.update({'p':'V'})
decryptor.update({'z':'M'})
decryptor.update({'c':'W'})
decryptor.update({'u':'L'})
decryptor.update({'b':'O'})

decryptor.update({'w':'X'})
decryptor.update({'l':'S'})
decryptor.update({'v':'F'})

decryptor.update({'n':'C'})
decryptor.update({'g':'P'})
decryptor.update({'j':'U'})
'''
#import json, pprint
#pprint.pprint (decryptor)

d_phrase =''
for e in e_phrase:
    if e in decryptor:
        d_phrase += decryptor[e]
    else: d_phrase += e

print (d_phrase)
