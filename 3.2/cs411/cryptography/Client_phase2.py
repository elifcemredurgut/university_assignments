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

API_URL = 'http://10.92.52.175:5000/'

stuID =  26493  ## Change this to your ID number

curve = Curve.get_curve('secp256k1')
n = curve.order
p = curve.field
P = curve.generator

#server's Identity public key
IKey_Ser = Point(93223115898197558905062012489877327981787036929201444813217704012422483432813 , 8985629203225767185464920094198364255740987346743912071843303975587695337619, curve)

#Send Public Identity Key Coordinates and corresponding signature
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

#Pseudo-client will send you 5 messages to your inbox via server when you call this function
def PseudoSendMsg(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "PseudoSendMsg"), json = mes)		
    print(response.json())

#get your messages. server will send 1 message from your inbox 
def ReqMsg(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.get('{}/{}'.format(API_URL, "ReqMsg"), json = mes)	
    print(response.json())	
    if((response.ok) == True): 
        res = response.json()
        return res["IDB"], res["OTKID"], res["MSGID"], res["MSG"], res["EK.X"], res["EK.Y"]

#If you decrypted the message, send back the plaintext for grading
def Checker(stuID, stuIDB, msgID, decmsg):
    mes = {'IDA':stuID, 'IDB':stuIDB, 'MSGID': msgID, 'DECMSG': decmsg}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "Checker"), json = mes)		
    print(response.json())

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

#Identity Keys
sA = 47243020609973021474827924840267021235853018440201017618287879379011063682130
qA= Point(0xdd61076e05e83c087835545f4163e1f00b040437a5fc678d49a65a39dee8a3e1 , 0x32503aa7646ae52257343ca31977ec36eab27b23caa67b272acf78bb006985a2, curve)


#SAVING OTK'S
stuID_byte = stuID.to_bytes((stuID.bit_length()+7)//8, byteorder = 'big')
(h,s) = Signature_Generation(stuID_byte)

ResetOTK(h,s)

#Hard coded kHMAC from phase 1
kHMAC = b'\xf3(^\xc97\xb9\rZ\x1d\x89d\xc8\x86H\x87(\x18%\xe0\xd5=d\xdf-\x15\xdb\xa0J\x0f\xc4pM'

#Registration of OTKs
OTKs = {}
for i in range(10):
    (otkAPri, otkAPub) = Key_Generation()

    otkAPubx = otkAPub.x.to_bytes((otkAPub.x.bit_length()+7)//8, byteorder = 'big')
    otkAPuby = otkAPub.y.to_bytes((otkAPub.y.bit_length()+7)//8, byteorder = 'big')
    concatenated = otkAPubx + otkAPuby

    #Generation HMAC value
    HMACval= HMAC.new(kHMAC, concatenated, SHA256)
    OTKReg(i,otkAPub.x,otkAPub.y,HMACval.hexdigest())
    OTKs[i] = otkAPri

print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
print("Telling pseudoclient to send me messages using PseudoSendMsg\n")

#Signing Student ID 
stuID_byte = stuID.to_bytes((stuID.bit_length()+7)//8, byteorder = 'big')
(h,s) = Signature_Generation(stuID_byte)

#Telling pseudoclient to send me messages
messages = PseudoSendMsg(h,s)

print("\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

#downloading the messages
messages = []

#Boolean value to control is Ks calculated or not for KDF chaing
is_Ks_calculated = False

for i in range(5):
    idb, otkid, msgid, msg, ekx, eky = ReqMsg(h, s)
    messages.append([idb,otkid,msgid,msg,ekx,eky])

    print("Converting message to bytes to decrypt it...")
    message = msg.to_bytes((msg.bit_length()+7)//8, byteorder = 'big')
    print("Converted message is:")
    print(message)

    # message_bytes = nonce + cipher + MAC
    print("Seperate nonce, ciphertext and hmac parts")
    nonce = message[:8]
    ciphertext = message[8:len(message)-32]
    MAC = message[len(ciphertext)+8:]
    
    
    # SESSION KEY AND KEY DERIVATION
    OTK_A_Pri = OTKs[otkid]
    EK_B_Pub = Point(ekx,eky,curve)
    
    T = OTK_A_Pri*EK_B_Pub
    print("T is:\n{}\n".format(T))
    tx = T.x.to_bytes((T.x.bit_length()+7)//8, byteorder = 'big')
    ty = T.y.to_bytes((T.y.bit_length()+7)//8, byteorder = 'big')
    U = tx+ty+b'MadMadWorld'
    print("U is:\n{}\n".format(U))
    Ks = SHA3_256.new(U).digest()
    print("Ks is:\n{}\n".format(Ks))

    Kenc = 0
    Khmac = 0
    Kkdf = Ks
    for i in range(msgid):
        Kenc = SHA3_256.new(Kkdf+b'LeaveMeAlone').digest()
        Khmac = SHA3_256.new(Kenc+b'GlovesAndSteeringWheel').digest()
        Kkdf = SHA3_256.new(Khmac+b'YouWillNotHaveTheDrink').digest()

        print("Kenc{} is:\n{}\n".format(i+1,Kenc))
        print("Khmac{} is:\n{}\n".format(i+1,Kenc))
        print("Kkdf{} is:\n{}\n".format(i+1,Kenc))
    
    print("\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    
    # HMAC VERIFICATION
    HMACval= HMAC.new(Khmac, ciphertext, SHA256).digest()
    print("calculated hmac is\n", HMACval)
    print("Incoming MAC is\n", MAC)

    if HMACval == MAC:
        print("\nHmac verified")

        # Decryption
        cipher = AES.new(Kenc, AES.MODE_CTR, nonce=nonce)
        ptext = cipher.decrypt(ciphertext)
        plaintext = ptext.decode('utf-8')

        Checker(stuID, idb, msgid, plaintext)

    else:
        print("\nHmac couldn't be verified")
        Checker(stuID, idb, msgid,"INVALIDHMAC")

    print("\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

 