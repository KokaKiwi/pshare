import string
import random
import hashlib
import base64
import time
import re
from string import (ascii_letters, digits, punctuation)

alphanum = ascii_letters + digits

alphafull = alphanum + punctuation

def generate(length = 8, chars = alphanum):
    return ''.join(random.choice(chars) for x in range(length))

def transform(h, length = None, strip = True):
    h = h.encode()

    h = hashlib.sha1(h).digest()
    h = base64.urlsafe_b64encode(h)

    h = str(h, 'ascii')

    if strip:
        h = re.sub(r'[=]+$', '', h)

    if length:
        h = h[:length]

    return h

secure_length = 16
secure_chars = alphafull
def generate_secure(salt = None, length = secure_length, chars = secure_chars):
    s = generate(length, chars)
    s += str(time.time())

    if salt:
        s += str(salt)

    s = transform(s)

    if length:
        s = s[:length]

    return s
