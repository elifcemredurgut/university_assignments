import math
import time
import random
import sympy
import warnings
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

stuID =  26493  ## ID of the sender
stuIDB = 26751  ## ID of the receiver
pseudoClientID = 18007

curve = Curve.get_curve('secp256k1')
n = curve.order
p = curve.field
P = curve.generator

#Identity Keys (Elif)
sA = 47243020609973021474827924840267021235853018440201017618287879379011063682130
qA= Point(0xdd61076e05e83c087835545f4163e1f00b040437a5fc678d49a65a39dee8a3e1 , 0x32503aa7646ae52257343ca31977ec36eab27b23caa67b272acf78bb006985a2, curve)

#Identity Keys (Metehan)
#sA = 74784421138790515375402862622676614617121382749600498455611505624377150548522
#qA =  Point(0x8ecd0d9cd6adcd046f48407fceeac6d8b14496940f6877cab4e0aa340163915d , 0xfe5ffab658f4236ba5f518a53115ada1e2c4dfb94d587508dd29ac88986f6193, curve)


#Server's Identity public key
IKey_Ser = Point(93223115898197558905062012489877327981787036929201444813217704012422483432813 , 8985629203225767185464920094198364255740987346743912071843303975587695337619, curve)

def IKRegReq(h,s,x,y):
    mes = {'ID':stuID, 'H': h, 'S': s, 'IKPUB.X': x, 'IKPUB.Y': y}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "IKRegReq"), json = mes)		
    if((response.ok) == False): print(response.json())

def IKRegVerify(code):
    mes = {'ID':stuID, 'CODE': code}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "IKRegVerif"), json = mes)
    if((response.ok) == False): raise Exception(response.json())
    print(response.json())

def SPKReg(h,s,x,y):
    mes = {'ID':stuID, 'H': h, 'S': s, 'SPKPUB.X': x, 'SPKPUB.Y': y}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "SPKReg"), json = mes)		
    if((response.ok) == False): 
        print(response.json())
    else: 
        res = response.json()
        return res['SPKPUB.X'], res['SPKPUB.Y'], res['H'], res['S']

def OTKReg(keyID,x,y,hmac):
    mes = {'ID':stuID, 'KEYID': keyID, 'OTKI.X': x, 'OTKI.Y': y, 'HMACI': hmac}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "OTKReg"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True


def ResetIK(rcode):
    mes = {'ID':stuID, 'RCODE': rcode}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetIK"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True

def ResetSPK(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetSPK"), json = mes)		
    print(response.json())
    if((response.ok) == False): return False
    else: return True

def ResetOTK(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.delete('{}/{}'.format(API_URL, "ResetOTK"), json = mes)		
    print(response.json())

def PseudoSendMsgPH3(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "PseudoSendMsgPH3"), json = mes)		
    print(response.json())

def ReqMsg(h,s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.get('{}/{}'.format(API_URL, "ReqMsg"), json = mes)	
    print(response.json())	
    if((response.ok) == True): 
        res = response.json()
        return res["IDB"], res["OTKID"], res["MSGID"], res["MSG"], res["EK.X"], res["EK.Y"]
    
def SendMsg(idA, idB, otkid, msgid, msg, ekx, eky):
    mes = {"IDA":idA, "IDB":idB, "OTKID": int(otkid), "MSGID": msgid, "MSG": msg, "EK.X": ekx, "EK.Y": eky}  #duzeltme: otkID --> otkid
    print("Sending message is: ", mes)
    response = requests.put('{}/{}'.format(API_URL, "SendMSG"), json = mes)
    print(response.json())    
        
def reqOTKB(stuID, stuIDB, h, s):
    OTK_request_msg = {'IDA': stuID, 'IDB':stuIDB, 'S': s, 'H': h}
    print("Requesting party B's OTK ...")
    response = requests.get('{}/{}'.format(API_URL, "ReqOTK"), json = OTK_request_msg)
    print(response.json()) 
    if((response.ok) == True):
        print(response.json()) 
        res = response.json()
        return res['KEYID'], res['OTK.X'], res['OTK.Y']      
    else:
        return -1, 0, 0

def Status(stuID, h, s):
    mes = {'ID':stuID, 'H': h, 'S': s}
    print("Sending message is: ", mes)
    response = requests.get('{}/{}'.format(API_URL, "Status"), json = mes)	
    print(response.json())
    if (response.ok == True):
        res = response.json()
        return res['numMSG'], res['numOTK'], res['StatusMSG']	

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

#3.5 Status Control

stuID_byte = stuID.to_bytes((stuID.bit_length()+7)//8, byteorder = 'big')
(h,s) = Signature_Generation(stuID_byte)
ResetOTK(h,s)

print("\n")
numMsg, numOTK, statusMsg = Status(stuID, h, s)

#Hard coded kHMAC from phase 1 (Elif)
kHMAC = b'\xf3/\xa2zH\x16\xa7\x0f\xe7\x82\xb9$\x8aA|\xa8Nv\xad\xd8\xccVr\x97"\xe5\x93\x88\xac\x8b\xcbs'
#(Metehan)
#kHMAC = b'\\?t\x1d\xdb\x14\x89\xdb\x07@\x90\x93B\xbe.\xf434\x8f\xd8M\x08\xb9P\xc6\xe3@\xf7D@\xcf\xa6'

#Registration of OTKs

print("\nCreating OTKs starting from index 0...\n")

OTKs = {}
for i in range(10):
    (otkAPri, otkAPub) = Key_Generation()

    otkAPubx = otkAPub.x.to_bytes((otkAPub.x.bit_length()+7)//8, byteorder = 'big')
    otkAPuby = otkAPub.y.to_bytes((otkAPub.y.bit_length()+7)//8, byteorder = 'big')
    concatenated = otkAPubx + otkAPuby

    #Generation HMAC value
    HMACval= HMAC.new(kHMAC, concatenated, SHA256)
    OTKReg(i,otkAPub.x,otkAPub.y,HMACval.hexdigest())
    OTKs[i] = [otkAPri, otkAPub.x, otkAPub.y]

print("\n")
print(OTKs)
print("\n")


#requesting messages from the pseudo client
PseudoSendMsgPH3(h,s)

#Checking the status again
print("\nChecking the status of the inbox and keys...\n")
numMsg, numOTK, statusMsg = Status(stuID, h, s)
print("\n\n")
#Downloading messages
#downloading the messages

#Boolean value to control is Ks calculated or not for KDF chaing
is_Ks_calculated = False

plaintexts = []

for i in range(5):
    idb, otkid, msgid, msg, ekx, eky = ReqMsg(h, s)

    #print("\nConverting message to bytes to decrypt it...\n")
    message = msg.to_bytes((msg.bit_length()+7)//8, byteorder = 'big')

    nonce = message[:8]
    ciphertext = message[8:len(message)-32]
    MAC = message[len(ciphertext)+8:]
    
    
    # SESSION KEY AND KEY DERIVATION
    OTK_A_Pri = OTKs[otkid][0]
    EK_B_Pub = Point(ekx,eky,curve)
    
    T = OTK_A_Pri*EK_B_Pub
    #print("T is:\n{}\n".format(T))
    tx = T.x.to_bytes((T.x.bit_length()+7)//8, byteorder = 'big')
    ty = T.y.to_bytes((T.y.bit_length()+7)//8, byteorder = 'big')
    U = tx+ty+b'MadMadWorld'
    #print("U is:\n{}\n".format(U))
    Ks = SHA3_256.new(U).digest()
    #print("Ks is:\n{}\n".format(Ks))

    Kenc = 0
    Khmac = 0
    Kkdf = Ks
    for i in range(msgid):
        Kenc = SHA3_256.new(Kkdf+b'LeaveMeAlone').digest()
        Khmac = SHA3_256.new(Kenc+b'GlovesAndSteeringWheel').digest()
        Kkdf = SHA3_256.new(Khmac+b'YouWillNotHaveTheDrink').digest()

    cipher = AES.new(Kenc, AES.MODE_CTR, nonce=nonce)
    ptext = cipher.decrypt(ciphertext)
    plaintext = ptext.decode('utf-8')
    print("\n"+plaintext+"\n-----------------------------------------------------------------\n")
    plaintexts.append(plaintext)


#3.4 Sending Messages 
#ONLY ONE MESSAGE 

print("\nSending message to my friend with id " + str(stuIDB) + ".")
print("\nSigning The stuIDB of party B with my private IK")
stuIDB_byte = stuIDB.to_bytes((stuIDB.bit_length()+7)//8, byteorder = 'big')
(hB,sB) = Signature_Generation(stuIDB_byte)

#Generating Ephemeral key
EK, EKPub = Key_Generation()

#Requesting OTK's of the receiver
KeyID, OTKx, OTKy = reqOTKB(stuID, stuIDB, hB, sB)
OTKB = Point(OTKx, OTKy, curve)     
print("\nEK:", EK)
print("OTKB:", OTKB, "\n")

#Generating session key using my EK and my friends Public OTK/ Phase 3...
T = OTKB*EK
print("T is:\n{}\n".format(T))
tx = T.x.to_bytes((T.x.bit_length()+7)//8, byteorder = 'big')
ty = T.y.to_bytes((T.y.bit_length()+7)//8, byteorder = 'big')
U = tx+ty+b'MadMadWorld'
print("U is:\n{}\n".format(U))
Ks = SHA3_256.new(U).digest()
print("Ks is:\n{}\n".format(Ks))

#Generating the KDF chain for the encryption and the MAC value generation
Kenc = 0
Khmac = 0
Kkdf = Ks
for i in range(1):    #to send only one message
    Kenc = SHA3_256.new(Kkdf+b'LeaveMeAlone').digest()
    Khmac = SHA3_256.new(Kenc+b'GlovesAndSteeringWheel').digest()
    Kkdf = SHA3_256.new(Khmac+b'YouWillNotHaveTheDrink').digest()

    print("Kenc{} is:\n{}\n".format(i+1,Kenc))
    print("Khmac{} is:\n{}\n".format(i+1,Kenc))
    print("Kkdf{} is:\n{}\n".format(i+1,Kenc))

#Encryption
msgToBeSend = b"Hello darkness my old friend"  #Change this as you wish
print("My message is:", msgToBeSend)

cipher = AES.new(Kenc, AES.MODE_CTR)
message_encrypted = cipher.encrypt(msgToBeSend)
hmac = HMAC.new(Khmac, message_encrypted, SHA256).digest()
ciphertext = cipher.nonce + message_encrypted + hmac
ciphertext = int.from_bytes(ciphertext, byteorder='big')

SendMsg(stuID, stuIDB, KeyID, 1, ciphertext, EKPub.x, EKPub.y)




#3.6 Sending messages to pseudo-clients for grading

print("\nSending messages to pseudo-clients for grading\n")

pseudoClientID_byte = pseudoClientID.to_bytes((pseudoClientID.bit_length()+7)//8, byteorder = 'big')
(hB,sB) = Signature_Generation(pseudoClientID_byte)

#Requesting OTK's of the receiver
KeyID, OTKx, OTKy = reqOTKB(stuID, pseudoClientID, hB, sB)
OTKB = Point(OTKx, OTKy, curve)    

msgIDToBeSend = 1
for i in plaintexts:

    #Generating Ephemeral key
    EK, EKPub = Key_Generation()
    print("Private part of my ephemeral key:", EK)

    #T, U, Ks, Kenc, khmac

    T = OTKB*EK
    print("T is:\n{}\n".format(T))
    tx = T.x.to_bytes((T.x.bit_length()+7)//8, byteorder = 'big')
    ty = T.y.to_bytes((T.y.bit_length()+7)//8, byteorder = 'big')
    U = tx+ty+b'MadMadWorld'
    print("U is:\n{}\n".format(U))
    Ks = SHA3_256.new(U).digest()
    print("Ks is:\n{}\n".format(Ks))

    #Generating the KDF chain for the encryption and the MAC value generation
    Kenc = 0
    Khmac = 0
    Kkdf = Ks
    for j in range(msgIDToBeSend):    
        Kenc = SHA3_256.new(Kkdf+b'LeaveMeAlone').digest()
        Khmac = SHA3_256.new(Kenc+b'GlovesAndSteeringWheel').digest()
        Kkdf = SHA3_256.new(Khmac+b'YouWillNotHaveTheDrink').digest()

        print("Kenc{} is:\n{}\n".format(j+1,Kenc))
        print("Khmac{} is:\n{}\n".format(j+1,Kenc))
        print("Kkdf{} is:\n{}\n".format(j+1,Kenc))



    i_bytes = bytes(str(i), 'utf-8')
    cipher = AES.new(Kenc, AES.MODE_CTR)
    i_encrypted = cipher.encrypt(i_bytes)
    hmac = HMAC.new(Khmac, i_encrypted, digestmod=SHA256).digest()
    ciphertext = cipher.nonce + i_encrypted + hmac
    ciphertext = int.from_bytes(ciphertext, byteorder='big')

    SendMsg(stuID, pseudoClientID, KeyID, msgIDToBeSend, ciphertext, EKPub.x, EKPub.y)
    msgIDToBeSend += 1
    print("\n---------------------------------------------------------------------\n")
