import random

# variable for rsa
p = 19
q = 29
n = p * q
phi_n = (p-1) * (q-1)
pubKeyList = list()

# gcd
def gcd(x, y):
    while (y):
        x, y = y, x % y
    return abs(x)


# list all possible public key
for i in range(2, phi_n):
    if (gcd(i, phi_n) == 1):
        pubKeyList.append(i)

# set rsa key for the client
e = random.choice(pubKeyList)   # pubkey
d = 0                           # prkey
while ((d * e) % phi_n != 1):
    d += 1
pubKey = (e, n)
prKey = d

# result for x^y mod p
def modularExp(x, y, p):
    res = 1

    while(y>0):
        if ((y & 1) != 0):
            res = (res * x)%p
 
        y = y >> 1
        x = x * x 
 
    return res % p

# rsa encryption
def rsa_encrypt(message, pubKey):
    print(f"Encrypt {message}:")
    pt = message
    ct = str()
    ptList = []
    ctList = []
    blockSize = n
    # print(f"Message = {binToDec(pt)}")

    # for each character
    for char in pt:
        ptNum = ord(char)
        ptList = [ptNum] + ptList
        ctNum = modularExp(ptNum, pubKey, blockSize)
        ctList = [ctNum] + ctList
        ct = chr(ctNum) + ct

    print("Before encryption:")
    #print(f"In decimal: {ptList}")
    print(f"In ascii: {pt}")
    print("After encryption:")
    #print(f"In decimal: {ctList}")
    print(f"In ascii: {ct}")

    return ct

# rsa decryption
def rsa_decrypt(message, prKey):
    print(f"Decrypt {message}:")
    ct = message
    pt = str()
    ptList = []
    ctList = []
    blockSize = n

    # for each character
    for char in ct:
        ctNum = ord(char)
        ctList = [ctNum] + ctList
        ptNum = modularExp(ctNum, prKey, blockSize)
        ptList = [ptNum] + ptList
        pt = chr(ptNum) + pt
    
    print("Before decryption:")
    #print(f"In decimal: {ctList}")
    print(f"In ascii: {ct}")
    print("After decryption:")
    #print(f"In decimal: {ptList}")
    print(f"In ascii: {pt}")

    return pt
