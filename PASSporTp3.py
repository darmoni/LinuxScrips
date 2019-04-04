#!/usr/bin/env python3

# RFC 7515 https://tools.ietf.org/pdf/rfc7515.pdf#section-4
# file name PASSporT.py
# utilities for creating and reading STIR PASSporT parts
# $Id$ $Date$


#uuid HOW TO: https://docs.python.org/2/library/uuid.html?highlight=rfc_4122
#SHAKEN https://tools.ietf.org/id/draft-wendt-stir-passport-shaken-01.html
#JWS RFC 7515 https://tools.ietf.org/html/rfc7515

import json, base64, uuid, hashlib, binascii

sample_header = '{"typ":"JWT",\r\n "alg":"HS256"}'
sample_protected_header = '{"iss":"joe",\r\n "exp":1300819380,\r\n "http://example.com/is_root":true}'

key = '{"kty":"oct","k":"AyM1SysPpbyDfgZld3umj1qzKObwVMkoqQ-EstJQLr_T-1qS0gZH75aKtMN3Yj0iPS4hcgUuTwjAzZr1Z9CAow"}'

sample_shah = bytearray([116, 24, 223, 180, 151, 153, 224, 37, 79, 250, 96, 125, 216, 173,
   187, 186, 22, 212, 37, 77, 105, 214, 191, 240, 91, 88, 5, 88, 83,
   132, 141, 121])

'''
def bytes(encoded_text):
    bytes=[]
    for i in range(len(encoded_text)):
        bytes.append(ord(encoded_text[i]))
    return bytes
'''
def decode_header(text):
    step1 = base64.urlsafe_b64encode(bytes(text)).split(b'=')[0]       # get rid of padding
    return step1

def hmac(hmac_parts):
    headers=[]
    for h in hmac_parts:
        headers.append(h)
    print(headers)
    before = '.'.join(headers)
    return before

#print(bytes(sample_header.encode('utf-8')))
print(binascii.hexlify(decode_header(sample_header.encode('utf-8'))).decode())


#print(bytes(sample_header.encode('utf-8')))
print(decode_header(sample_protected_header.encode('utf-8')).decode())


#the_hmac = hmac([decode_header(sample_header.encode('utf-8')),decode_header(sample_protected_header.encode('utf-8'))])
#print(the_hmac.replace('.','\n.\n'))
#print(bytes(the_hmac))
#jkey = json.loads(key)
#print (json.dumps(jkey))

#print(sample_shah)
#print(decode_header(str(sample_shah)))
def list2str(bytes_l):
    chars=''
    for b in bytes_l:
        chars += chr(b)
    return chars

#print(list2str(sample_shah).encode('utf-8'))
#signature = base64.urlsafe_b64encode(list2str(sample_shah).encode('utf-8')).split('=')[0]
signature = base64.urlsafe_b64encode(sample_shah).split(b'=')[0]
print(binascii.hexlify(signature).decode())
#print(base64.urlsafe_b64encode(str(sample_shah)))
the_hmac = hmac([decode_header(sample_header.encode('utf-8')).decode(),decode_header(sample_protected_header.encode('utf-8')).decode(), signature.decode()])
print(the_hmac.replace('.','\n.\n'))

dk = hashlib.pbkdf2_hmac('sha256', b'AyM1SysPpbyDfgZld3umj1qzKObwVMkoqQ-EstJQLr_T-1qS0gZH75aKtMN3Yj0iPS4hcgUuTwjAzZr1Z9CAow', b'eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ', 100000)

print(binascii.hexlify(dk).decode())
