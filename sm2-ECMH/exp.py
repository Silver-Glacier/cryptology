import math
import random
from gmssl import sm3,func

def module(a, n):  
    if math.isinf(a):
        return float('inf')
    else:
        return a % n

def modular(a, b, n):
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
            l = modular(Q[1] - P[1], Q[0] - P[0], p)
        else:
            l = modular(3 * P[0] ** 2 + a, 2 * P[1], p)
        X = module(l ** 2 - P[0] - Q[0], p)
        Y = module(l * (P[0] - X) - P[1], p)
        Z = [X, Y]
    return Z

def mulytipy(k, P, a, p):  
    tmp = bin(k).replace('0b', '')  
    l = len(tmp) - 1
    Z = P
    if l > 0:
        k = k - 2 ** l
        while l > 0:
            Z = add(Z, Z, a, p)
            l -= 1
        if k > 0:
            Z = add(Z, mulytipy(k, P, a, p), a, p)
    return Z

def keygen(a, p, n, G):
    d = random.randint(1, n - 2)
    k = mulytipy(d, G, a, p)
    return d, k

def isQR(n,p):
    return pow(n, (p - 1) // 2, p)

def QR(n,p):
    assert isQR(n, p) == 1
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    for z in range(2, p):
        if isQR(z, p) == p - 1:
            c = pow(z, q, p)
            break
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    if t % p == 1:
        return r
    else:
        i = 0
        while t % p != 1:
            temp = pow(t, 2 ** (i + 1), p)
            i += 1
            if temp % p == 1:
                b = pow(c, 2 ** (m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0
        return r

def _hash(S):
    res = [float("inf"), float("inf")]
    for k in S:
        x = int(sm3.sm3_hash(func.bytes_to_list(k)), 16)
        tmp = module(x ** 2 + a * x + b, p)
        y = QR(tmp, p)
        res = add(res, [x, y], a, p)
    return res


if __name__ == '__main__':
    p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    x = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    y = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    g = [x, y]
    [d,k]=keygen(a,p,n,g)
    print("d:",d)
    print("k:",k)

    s = (b'1234',b'5678')
    r = _hash(s)
    print("hash :",r)
