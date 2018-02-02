#!/usr/bin/env python

def translate_field(x,v):
    return {
        'Float64':  float(v),
        'Int':      int(float(v))
    }.get(x, v)

print(translate_field('Float64','12.56'))
print(translate_field('Int','12.56'))
print(translate_field('Interna','12.56'))
