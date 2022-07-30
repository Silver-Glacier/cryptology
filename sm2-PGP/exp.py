import math
import base64
import random
from gmssl import sm2
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

def epoint_mod(a, n):  
    if math.isinf(a):
        return float('inf')
    else:
        return a % n

def epoint_modmult(a, b, n):
    if b == 0:
        r = float('inf')
    elif a == 0:
        r = 0
    else:
        t = bin(n - 2).replace('0b', '')
        y = 1
        i = 0
        while i < len(t):  
            y = (y ** 2) % n 
            if t[i] == '1':
                y = (y * b) % n
            i += 1
        r = (y * a) % n
    return r

def add(P, Q, a, p):
    if (math.isinf(P[0]) or math.isinf(P[1])) and (~math.isinf(Q[0]) and ~math.isinf(Q[1])):  
        Z = Q
    elif (~math.isinf(P[0]) and ~math.isinf(P[1])) and (math.isinf(Q[0]) or math.isinf(Q[1])): 
        Z = P
    elif (math.isinf(P[0]) or math.isinf(P[1])) and (math.isinf(Q[0]) or math.isinf(Q[1])):  
        Z = [float('inf'), float('inf')]
    else:
        if P != Q:
            l = epoint_modmult(Q[1] - P[1], Q[0] - P[0], p)
        else:
            l = epoint_modmult(3 * P[0] ** 2 + a, 2 * P[1], p)
        X = epoint_mod(l ** 2 - P[0] - Q[0], p)
        Y = epoint_mod(l * (P[0] - X) - P[1], p)
        Z = [X, Y]
    return Z


def multipy(k, P, a, p):  
    tmp = bin(k).replace('0b', '')  
    l = len(tmp) - 1
    Z = P
    if l > 0:
        k = k - 2 ** l
        while l > 0:
            Z = add(Z, Z, a, p)
            l -= 1
        if k > 0:
            Z = add(Z, multipy(k, P, a, p), a, p)
    return Z

def key(a, p, n, G):
    d = random.randint(1, n - 2)
    k = multipy(d, G, a, p)
    return d, k


def encrypt(m,k):
    l = 16
    n = len(m)
    if n % l != 0:
        num = l - (n % l)
    else:
        num = 0
    m = m + ('\0' * num)
    #str->bytes
    m = str.encode(m)
    k = str.encode(k)
    print("Message：\n", base64.b16encode(m))
    print("Key：\n", base64.b16encode(k))
    
    SM4 = CryptSM4()
    SM4.set_key(k, SM4_ENCRYPT)
    c1 = SM4.crypt_ecb(m)
    
    c2 = sm2_crypt.encrypt(k)
    print("message：\n", base64.b16encode(c1))
    print("Encryptkey：\n",base64.b16encode(c2))
    return c1, c2

def decrypt(c1,c2):
    k = sm2_crypt.decrypt(c2)
    SM4 = CryptSM4()
    SM4.set_key(k, SM4_DECRYPT)
    m = SM4.crypt_ecb(c1)
    
    print("Decrypt_key：\n", base64.b16encode(k))
    print("message：\n", base64.b16encode(m))

if __name__ == '__main__':
    p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    x = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    y = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    g = [x, y]
    [d,k]=key(a,p,n,g)
    
    sk = hex(d)[2:]
    pk = hex(k[0])[2:] + hex(k[1])[2:]

    sm2_crypt = sm2.CryptSM2(public_key=pk, private_key=sk)
    
    m = "hello,world!"
    
    k = hex(random.randint(2 ** 127, 2 ** 128))[2:]
    
    r1, r2 = encrypt(m, k)
    decrypt(r1, r2)
