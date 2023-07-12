import math
import time
import random
import sympy
import warnings
from random import randint, seed
import sys
from ecpy.curves import Curve,Point
from Crypto.Hash import SHA3_256
import requests
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import random
import re
import json
import argparse


API_URL = '10.92.52.175:6000'


def view_status():
    try:
        response = requests.get(f'http://{API_URL}')		
        if((response.ok) == False):
            raise Exception(response.json())
        else:
            print(response.json())
    except Exception as e:
        print(e)

def view_classlist():
    try:
        response = requests.get(f'http://{API_URL}/Class')		
        if((response.ok) == False):
            raise Exception(response.json())
        else:
            print(response.json())
    except Exception as e:
        print(e)



def register(id_, rand_nam):
    try:
        mes = {'ID': id_, 'random': rand_nam}
        response = requests.put(f'http://{API_URL}/Register', json = mes)
        if((response.ok) == False):
            raise Exception(response.json())
        else:
            print(response.json())
    except Exception as e:
        print(e)
        




stuID = 26045	 ##Change this to your ID number
#num = 121212122112 ##Create a random number or enter your favourite num

#Register to the most secure lottery ever:D
#register(stuID, num)

#View status
view_status()

#Comment out to view class list 
view_classlist()
