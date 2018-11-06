from random import randint
import jwt

from aliceinit import app, db
from models import Users

from time import time, sleep

def numbercode(int):
    start = (10**int)-1
    end = 10**(int-1)
    code = randint(000000, 999999)
    print(code)
    return code
