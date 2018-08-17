#!/usr/bin/env python

words={}
for word in ('db','ghost','db','ACD'):
    if word in words:
        words[word] +=1
    else:
        words[word]=1
print(words)
