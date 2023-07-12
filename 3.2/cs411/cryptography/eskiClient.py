import math
import time
import random
import sympy
import warnings
from random import randint, seed
import sys
from ecpy.curves import Curve,Point
from Crypto.Hash import SHA3_256, HMAC, SHA256
import requests
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import random
import re
import json

ikAPri = 0
ikAPub = 0
sA = 0
qA = 0
spkAPri = 0
spkAPub = 0

curve = Curve.get_curve('secp256k1')
n = curve.order
p = curve.field
P = curve.generator

API_URL = 'http://10.92.52.175:5000/'

stuID =  26493  ## Change this to your ID number

#server's Identitiy public key
IKey_Ser = Point(93223115898197558905062012489877327981787036929201444813217704012422483432813 , 8985629203225767185464920094198364255740987346743912071843303975587695337619, curve)

#Send Public Identitiy Key Coordinates and corresponding signature
def IKRegReq(h,s,x,y):
    mes = {'ID':stuID, 'H': h, 'S': s, 'IKPUB.X': x, 'IKPUB.Y': y}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "IKRegReq"), json = mes)		
    if((response.ok) == False): print(response.json())

#Send the verification code
def IKRegVerify(code):
    mes = {'ID':stuID, 'CODE': code}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "IKRegVerif"), json = mes)
    if((response.ok) == False): raise Exception(response.json())
    print(response.json())

#Send SPK Coordinates and corresponding signature
def SPKReg(h,s,x,y):
    mes = {'ID':stuID, 'H': h, 'S': s, 'SPKPUB.X': x, 'SPKPUB.Y': y}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "SPKReg"), json = mes)		
    if((response.ok) == False): 
        print(response.json())
    else: 
        res = response.json()
        return res['SPKPUB.X'], res['SPKPUB.Y'], res['H'], res['S']

#Send OTK Coordinates and corresponding hmac
def OTKReg(keyID,x,y,hmac):
    mes = {'ID':stuID, 'KEYID': keyID, 'OTKI.X': x, 'OTKI.Y': y, 'HMACI': hmac}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "OTKReg"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True

#Send the reset code to delete your Identitiy Key
#Reset Code is sent when you first registered
def ResetIK(rcode):
    mes = {'ID':stuID, 'RCODE': rcode}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetIK"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True

#Sign your ID  number and send the signature to delete your SPK
def ResetSPK(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetSPK"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True

#Send the reset code to delete your Identitiy Key
def ResetOTK(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetOTK"), json = mes)		
    if((response.ok) == False): print(response.json())

def Key_Generation():
  sA = Random.new().read(int(math.log(n-1,2)))
  sA = int.from_bytes(sA, byteorder='big') % n
  qA = sA*P
  return (sA,qA)

def Signature_Generation(m):
  k = Random.new().read(int(math.log(n-2,2)))
  k = int.from_bytes(k, byteorder='big')%n
  R = k*P
  r = R.x%n
  #m = m.to_bytes((m.bit_length()+7)//8, byteorder = 'big')
  conc = r.to_bytes((r.bit_length()+7)//8, byteorder = 'big')+m
  hash = SHA3_256.new(conc)
  h = int.from_bytes(hash.digest(), 'big') % n
  s = (k-sA*h)%n
  return (h,s)

def Signature_Verification(m, h, s):
    V = s*P + h*IKey_Ser
    v = V.x % n
    #m = m.to_bytes((m.bit_length()+7)//8, byteorder = 'big')
    concatenated = v.to_bytes((v.bit_length()+7)//8, byteorder = 'big')+m
    hash = SHA3_256.new(concatenated)
    h_ = int.from_bytes(hash.digest(), 'big') % n

    if h == h_:
        print("Verified successfully.")
        return True
    else:
        print("Could not verify.")
        return False


  
#IK
sA = 8622802264767405067977352475390176018886079620378498944444171491782623058309
qA= Point(0x3fe187e9224eead3c16973fac1a2f87ee96d00a7819fb12b355b4ce37fbf79f9 , 0x7fd5b3617b280e8d8b8f0aaa5c16108bed89014cafe6b1041721447300b8855b, curve)
"""
(ikAPri,ikAPub) = Key_Generation()
sA=ikAPri
qA= ikAPub
print("\nPrivate IK: ", ikAPri, "\nPublic IK.x: ", ikAPub.x, "\nPublic IK.y: ", ikAPub.y)
print("\nqA: ", qA)
"""
stuID_byte = stuID.to_bytes((stuID.bit_length()+7)//8, byteorder = 'big')
(h,s) = Signature_Generation(stuID_byte)
print("\nThe signature of ID", stuID, "is\nh:", h, "\ns:", s)

#IKRegReq(h,s,ikAPub.x, ikAPub.y)

Signature_Verification(stuID_byte, h, s) # to test

#IKRegVerify(669118)
#ResetIK(667820)

#SPK

print("\nGenerating SPK...")
(spkAPri, spkAPub) = Key_Generation()
print("\nPrivate SPK: ", spkAPri, "\nPublic SPK.x: ", spkAPub.x, "\nPublic SPK.y: ", spkAPub.y)

spkAPubx = spkAPub.x.to_bytes((spkAPub.x.bit_length()+7)//8, byteorder = 'big')
spkAPuby = spkAPub.y.to_bytes((spkAPub.y.bit_length()+7)//8, byteorder = 'big')
concatenated = spkAPubx + spkAPuby
(spkh, spks) = Signature_Generation(concatenated)
print("\nThe signature of SPK is\nh:", spkh, "\ns:", spks)

spkSPubx, spkSPuby, sh, ss = SPKReg(spkh, spks, spkAPub.x, spkAPub.y)
print("\nThe server sent \nPublic SPK.x: ", spkSPubx, "\nPublic SPK.y: ", spkSPuby, "\nh: ", sh, "\ns: ", ss)
spkSPubx = spkSPubx.to_bytes((spkSPubx.bit_length()+7)//8, byteorder = 'big')
spkSPuby = spkSPuby.to_bytes((spkSPuby.bit_length()+7)//8, byteorder = 'big')
conc_spkS = spkSPubx + spkSPuby

if Signature_Verification(conc_spkS, sh, ss):
    print("otkk ")
    #OTK PART - METEHAN




