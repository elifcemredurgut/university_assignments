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

stuID =  26493  ## Change this to your ID number
stuIDB = 26751  ## ID of the receiver
pseudoClientID = 18007

curve = Curve.get_curve('secp256k1')
n = curve.order
p = curve.field
P = curve.generator

#Identity Keys
sA = 47243020609973021474827924840267021235853018440201017618287879379011063682130
qA= Point(0xdd61076e05e83c087835545f4163e1f00b040437a5fc678d49a65a39dee8a3e1 , 0x32503aa7646ae52257343ca31977ec36eab27b23caa67b272acf78bb006985a2, curve)


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
#ResetOTK(h,s)

print("\n")
numMsg, numOTK, statusMsg = Status(stuID, h, s)

#Hard coded kHMAC from phase 1
kHMAC = b'\xf3/\xa2zH\x16\xa7\x0f\xe7\x82\xb9$\x8aA|\xa8Nv\xad\xd8\xccVr\x97"\xe5\x93\x88\xac\x8b\xcbs'




idb, otkid, msgid, msg, ekx, eky = ReqMsg(h, s)
#messages.append([idb,otkid,msgid,msg,ekx,eky])

print("Converting message to bytes to decrypt it...")
message = msg.to_bytes((msg.bit_length()+7)//8, byteorder = 'big')
print("Converted message is:")
print(message)

# message_bytes = nonce + cipher + MAC
print("Seperate nonce, ciphertext and hmac parts")
nonce = message[:8]
ciphertext = message[8:len(message)-32]
MAC = message[len(ciphertext)+8:]


OTKs = {0: [115722498879600095935899000811621748189311708804290919611659524324008130380653, 105671506171152838466931315670204025409185259773623379202421443511830471438202, 85819459653273628357221638675164966849927422217939513805366740861843742172991], 1: [36559351615636690913437816699028050472000043855298358312873464039553967420849, 75830900899470473285213438746956907571630015496588634947952033980358799717541, 62722992767388357736891339993280935966320801990591733515935631650903920278205], 2: [33462875238521355438956817747331927335310767389735764320333341762857367536398, 72579650360809951059501677393218369927879679421744010952066343658978558584875, 21385242235405918749773202535701158363952801673728597313405445914795830981647], 3: [51903196870122984925761116850736226151723793025345434783362664008423037910097, 67790171518513948127230800645855454831841255400473092419430658010493225079588, 61049500917454929832108488092387631624540333201956034804328378324315725112799], 4: [21028466067043891015785279460133443744415305815071635318067927336298766984986, 50935337054567603074419727419614423958784110766560067509166421514949649776355, 73671516662126804827493071824673487582011244241571791058383812735685891206146], 5: [44205318934905044514323887968176899601927119020319869519011277535561867991819, 99418334360955524975893805556719302701466490581342051386959885140585451385801, 105508231289104192361085852710372404297465067147430989178901737383570631680534], 6: [31888863574108150841208892381291541783355399642747439953923875575868216443217, 90375650203227415934674983239533434701682488200924752543170055151313753371825, 8976773900696897078672075478592361441785164284974894578188866689100775185714], 7: [94495537906625832047910936511698386888130224879218554886851535867838758470890, 80845518827875979706339670009192195120046287413723057916145076009471284093670, 69987853308489263506374724518281937306383311689392859993618014483934719256727], 8: [4972122748525267969332529775703555852038358510142106843115592404266337685457, 64772258822555774226574662096057262884512129228373368167856967924651478209623, 76452301438039986768123766586438567629343612798625921611921386515297375034333], 9: [113351506652327049737987120682656216609842921754124497107327375209796774158444, 50070263156546222017721562261830745053986307290779010064859446316302968679139, 28500499984781144240457488687762120877548594183891529704220968285296072168513]}

# SESSION KEY AND KEY DERIVATION
OTK_A_Pri = OTKs[otkid][0]
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
    print(plaintext)
