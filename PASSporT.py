#!/usr/bin/env python

# RFC 7515 https://tools.ietf.org/pdf/rfc7515.pdf#section-4
# file name PASSporT.py
# utilities for creating and reading STIR PASSporT parts
# $Id$ $Date$

import json

sample_header = '{"typ":"JWT",\r\n "alg":"HS256"}'

def bytes(text):
    utf8 = text.encode('utf-8')
    utf8_bytes=[]
    for i in range(len(utf8)):
        utf8_bytes.append(ord(utf8[i]))
    return utf8_bytes

print(bytes(sample_header))
