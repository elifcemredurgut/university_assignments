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

stuID =  26751  ## ID of the receiver
stuIDB = 26493  ## ID of the sender
pseudoClientID = 18007

curve = Curve.get_curve('secp256k1')
n = curve.order
p = curve.field
P = curve.generator

#Identity Keys
#sA = 47243020609973021474827924840267021235853018440201017618287879379011063682130
#qA= Point(0xdd61076e05e83c087835545f4163e1f00b040437a5fc678d49a65a39dee8a3e1 , 0x32503aa7646ae52257343ca31977ec36eab27b23caa67b272acf78bb006985a2, curve)

#Identity Keys (Metehan)
sA = 74784421138790515375402862622676614617121382749600498455611505624377150548522
qA =  Point(0x8ecd0d9cd6adcd046f48407fceeac6d8b14496940f6877cab4e0aa340163915d , 0xfe5ffab658f4236ba5f518a53115ada1e2c4dfb94d587508dd29ac88986f6193, curve)


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

stuID_byte = stuID.to_bytes((stuID.bit_length()+7)//8, byteorder = 'big')
(h,s) = Signature_Generation(stuID_byte)

idb, otkid, msgid, msg, ekx, eky = ReqMsg(h, s)
#print("\nidb=",idb,"\notkid=",otkid,"\nmsgid=", msgid,"\nmsg=",msg,"\nekx=",ekx,"\neky=",eky)


#verify
"""
idb= 26493
otkid= 3
msgid= 1
msg= 628457776553551599634692977838400299455026912843359179111849793007478758563009025182320104611009779037804039900147092821622
ekx= 27297927273496615893879424356802759052189493681901716624420302428242833452386
eky= 93928436732934056098721251836019138223072952057613093602096389944111036257465
"""
#OTKs = {0: [104641445773036211833705796430301999703162097851753287023800363214929625118393, 54257242329742095659959696494991800846033959707550380602894973942755189376883, 29520248282745429094814363408538374706965246617905043406813930957686215884113], 1: [95283888995075637525527681471754477445033833834683991004660964788759284766748, 109158072270539447682074059836149119384354145392428523171523273591612936333902, 113315336201638637692488091780255343864277113248854408411922510591364531070343], 2: [112322574326460067512696245601665620233691413846962326207003000511632178595451, 93574715783215291670031998829590768140882508287218975691911201538154623896354, 24895902975248125202873932040133691486857206791167346682484688912992081258870], 3: [101529239967122130300826724166794624369206995443192023735492370410944729965731, 17254376656510016895056436812852546202886679522104723109612980740119263047469, 40862249543808042019254406441795064744257919789516248597654359171627326818910], 4: [85773471502206871033147171550191633795034619865019183664020858729241871933133, 110590457566027462512312109731683522103795012722940130596214498285914584837120, 77717484938535552163607311894041619768931070427021839264842632440027612172771], 5: [3311628641880593677501593050618861078804276730737284646004702339094335282981, 58365097493949301735561106324066987023709971368210906504502557758247138620107, 10585705024469993346349620251149322173687414237537813807120009447432945138635], 6: [26041752326838132159203852450777955723060044410324054502689664782801473793984, 69291682665278454932607377988422984670492828735194216613544419355184024839046, 62907911814525829252207628745648488025145749742676111391086132751023979078857], 7: [86484371107622138375178310897787291987157394957590510757539243112936632055719, 11104789657123880302516645126878218726877014212180448396904183910710055881501, 40487437526887410062764176355453409268493541498397382063756039214744098928671], 8: [59542248200249630965773567298396456044125171298202967053684555801272560884985, 94130563166091372403388415992823007495952757508639154425751766466312289767147, 90083357310397600596005262253765190169101397352415414026232684431505554772280], 9: [95069749155796678351039427015155141512175400014615384500592191223481854968080, 91266954315381877869095938186971411908607504548907113320902295161757806990178, 110727129505738046863101699453454188083439471215266350380631052871693327527904]}
#Metehan
OTKs = {0: [13099967356904653229887255386233545819426977680545643033041326490289539695030, 75218847671381220769305646305969693682483329813586357677257673572566408140630, 108768424197191200838213799734509798016692081253442899747599781053296536629483], 1: [96606906399427494005219345247642907684363520875303659188186641459842486619583, 53078196297888769840898621520283535320778034793700452835093195071666531833197, 82082776837174189266520815491561337891976398406110330445922375460036949867619], 2: [28531475674953154814622991751515248946653331686866735274115330053091222445933, 65385876310188223176280793576347189852363308683029730966377641012705565905841, 79613863190887053026814030636281126657349088163313949564023267054209380478809], 3: [74837020239290653172318681785032442845028566563325751976569453480420271046372, 573628197025306997283289354856473469796541667118798654756011673155627121226, 14917398219705790256508687997482277198818032244722836296490235462555261508743], 4: [89183232527322987991917845146056908998427582169512811955410441485232389749940, 26632705908876436711872727679219298771955744764746901779030217912904095013814, 112655726753349982509170445582477891197544015272537657056043703387973424027940], 5: [13540762459165951409847206175784360356493299188071962666385056197468992956107, 4365826332885473226626133360748933271361665686341117191937677442292117144056, 38284451854584208350755577874219845087631161344911711432460331140656973624936], 6: [16109894964692391732833521204206292370281028948945336273877076278567299749308, 31862687157648443735157001260961073923245582442244731097201276956226731211174, 101707979705734736037292249440447022131653902000881270816852789627650660209102], 7: [43674871767208866392048276561105063744112440112512294642685105111145540174435, 63018171283529348424629058216138039692992349044354425627867612981682236744040, 113426609334710129831749272395737669928232633024836626918418397626947448150594], 8: [10924816805458787272456977475261851456945637732606441402988604386993500145197, 36522550577040355151705406770499580664232392908455076787025945491265432139562, 27814308989457687108636709408730033510206803635994698377159694802431961349627], 9: [3179609524174124422541996709150342959902345259728383203534370301693159370029, 52996421161112085680461870870334064599636898767707313095697160177484737788255, 53372330078204836004441449383195257204783365320271437284897982511647615949712]}
message = msg.to_bytes((msg.bit_length()+7)//8, byteorder = 'big')

nonce = message[:8]
ciphertext = message[8:len(message)-32]
MAC = message[len(ciphertext)+8:]

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

else:
    print("\nHmac couldn't be verified")