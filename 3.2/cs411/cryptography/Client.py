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

#This ID belongs to Elif Cemre Durgut
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

#Generate key using Random function from Crypto module
def Key_Generation():
  sA = Random.new().read(int(math.log(n-1,2)))
  sA = int.from_bytes(sA, byteorder='big') % n
  qA = sA*P
  return (sA,qA)

#Generate signature with SHA3-256
def Signature_Generation(m):
  k = Random.new().read(int(math.log(n-2,2)))
  k = int.from_bytes(k, byteorder='big')%n
  R = k*P
  r = R.x%n
  conc = r.to_bytes((r.bit_length()+7)//8, byteorder = 'big')+m
  hash = SHA3_256.new(conc)
  h = int.from_bytes(hash.digest(), 'big') % n
  s = (k-sA*h)%n
  return (h,s)

#Verify the signature using the public key of the server
def Signature_Verification(m, h, s):
    V = s*P + h*IKey_Ser
    v = V.x % n
    concatenated = v.to_bytes((v.bit_length()+7)//8, byteorder = 'big')+m
    hash = SHA3_256.new(concatenated)
    h_ = int.from_bytes(hash.digest(), 'big') % n

    if h == h_:
        print("Verified successfully.")
        return True
    else:
        print("Could not verified.")
        return False


  
#IDENTITY KEY PART

#If you want to generate an IK from scratch comment the next two lines, and uncomment the next block

sA = 47243020609973021474827924840267021235853018440201017618287879379011063682130
qA= Point(0xdd61076e05e83c087835545f4163e1f00b040437a5fc678d49a65a39dee8a3e1 , 0x32503aa7646ae52257343ca31977ec36eab27b23caa67b272acf78bb006985a2, curve)

"""
(ikAPri,ikAPub) = Key_Generation()
sA=ikAPri
qA= ikAPub
print("Identitiy Key is created")
print("IKey is a long term key and shouldn't be changed and private part should be kept secret. But this is a sample run, so here is my private IKey:", ikAPri)
print("\nqA: ", qA) #uncomment this line and save the result in qA

stuID_byte = stuID.to_bytes((stuID.bit_length()+7)//8, byteorder = 'big')
print("\nMy ID number is", stuID)
print("Converted my ID to bytes in order to sign it:", stuID_byte)

(h,s) = Signature_Generation(stuID_byte)
print("\nSignature of my ID number is:\nh=", h, "\ns=", s)

print("\nSending signature and my IKEY to server via IKRegReq() function in json format")
IKRegReq(h,s,ikAPub.x, ikAPub.y)

print("\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
"""

#Identity Key Registration
"""
print("Received the verification code through email\nEnter verification code which is sent to you: \nSending the verification code to server via IKRegVerify() function in json format")
IKRegVerify(110721)
print("\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
"""

#Reseting the IK
"""
print("Trying to delete Identity Key...\n")
ResetIK(963567)
"""


#SIGNED PRE-KEY (SPK) PART

print("Generating SPK...\n")
(spkAPri, spkAPub) = Key_Generation()
print("\nPrivate SPK:", spkAPri, "\nPublic SPK.x:", spkAPub.x, "\nPublic SPK.y:", spkAPub.y)

print("\nConvert SPK.x and SPK.y to bytes in order to sign them then concatenate them")
spkAPubx = spkAPub.x.to_bytes((spkAPub.x.bit_length()+7)//8, byteorder = 'big')
spkAPuby = spkAPub.y.to_bytes((spkAPub.y.bit_length()+7)//8, byteorder = 'big')
concatenated = spkAPubx + spkAPuby
print("result will be like:", concatenated)

(spkh, spks) = Signature_Generation(concatenated)
print("\nSignature of SPK is\nh=", spkh, "\ns=", spks)

print("\nSending SPK and the signatures to the server via SPKReg() function in json format...")
spkSPubx, spkSPuby, sh, ss = SPKReg(spkh, spks, spkAPub.x, spkAPub.y)
print("\nif server verifies the signature it will send its SPK and corresponding signature. If this is the case SPKReg() function will return those")
print("\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

print("Server's SPK Verification\n")

concatenated = spkSPubx.to_bytes((spkSPubx.bit_length()+7)//8, byteorder = 'big')+spkSPuby.to_bytes((spkSPuby.bit_length()+7)//8, byteorder = 'big') 
isVerified =  Signature_Verification(concatenated, sh, ss)

print("Recreating the message(SPK) signed by the server\nVerifying the server's SPK...\nIf server's SPK is verified we can move to the OTK generation step\nIs SPK verified?: ", isVerified)

if isVerified:
    print("\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    
    #Generating HMAC Key
    print("Creating HMAC key (Diffie Hellman)\n")

    spkSPub = Point(spkSPubx,spkSPuby,curve)
    T = spkAPri*spkSPub
    print("T is",T)
    tx = T.x.to_bytes((T.x.bit_length()+7)//8, byteorder = 'big')
    ty = T.y.to_bytes((T.y.bit_length()+7)//8, byteorder = 'big')
    U = tx+ty+b'NoNeedToRideAndHide'
    print("U is",U)
    kHMAC = SHA3_256.new(U).digest()
    print("HMAC key is created {}\n".format(kHMAC))

    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    

    #Registration of OTKs
    for i in range(10):
        print("Creating OTKs starting from index 0...\n")
        print("********")
        (otkAPri, otkAPub) = Key_Generation()
        print("{}th key generated. Private part={}\nPublic (x coordinate)={}\nPublic (y coordinate)={}\n".format(i,otkAPri,otkAPub.x,otkAPub.y))

        otkAPubx = otkAPub.x.to_bytes((otkAPub.x.bit_length()+7)//8, byteorder = 'big')
        otkAPuby = otkAPub.y.to_bytes((otkAPub.y.bit_length()+7)//8, byteorder = 'big')
        concatenated = otkAPubx + otkAPuby
        print("x and y coordinates of the OTK converted to bytes and concatanated message {}\n".format(concatenated))

        #Generation HMAC value
        HMACval= HMAC.new(kHMAC, concatenated, SHA256)
        print("hmac is calculated and converted with 'hexdigest()':\n{}\n".format(HMACval.hexdigest()))
        OTKReg(i,otkAPub.x,otkAPub.y,HMACval.hexdigest())
        