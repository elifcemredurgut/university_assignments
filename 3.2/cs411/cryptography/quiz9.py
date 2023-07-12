from ecpy.curves     import Curve,Point
from ecpy.keys       import ECPublicKey, ECPrivateKey
from ecpy.ecdsa      import ECDSA
from Crypto import Random
from Crypto.Hash import SHA3_256
import random

# the curve

E = Curve.get_curve('secp256k1')
n = E.order
P = E.generator

sA = 15688923813051339579899514306561009754847244425850270395713426399738846698385
sB = 87887250479317705195691589147779731728113271531260221672657305273211799197041

#Missing Line
KAB = sA*sB*P
#Missing Line

K = SHA3_256.new(KAB.x.to_bytes((KAB.x.bit_length() + 7) // 8, byteorder='big')+b'ECDH Key Exchange')

print("K: ", K.hexdigest())