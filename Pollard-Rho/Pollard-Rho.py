from gmpy2 import invert #求逆元模块

# p,a,b=383,2,228
# n=191
#测试用例

print("a^x==b mod p\n求x=log a (b)\n")
p=int(input('输入p='))
a=int(input('输入a='))
b=int(input('输入b='))
n=int(input('输入阶数n='))

def fun_x(x):
    #输入x[i]返回x[i+1]
    if (x % 3 ==1):
        x_next = x * b % p
    elif(x % 3 ==0):
        x_next = x ** 2 % p
    elif(x % 3 == 2):
        x_next = x * a % p
    return x_next

def fun_a(a,x):
    #输入a[i],x[i],返回a[i+1]
    if (x % 3 ==1):
        a_next = a
    elif(x % 3 ==0):
        a_next = a * 2 % (n)
    elif(x % 3 == 2):
        a_next = (a + 1) % n
    return a_next

def fun_b(b,x):
    #输入b[i],x[i],返回b[i+1]
    if (x % 3 ==1):
        b_next = (b + 1) % n
    elif(x % 3 ==0):
        b_next = b * 2 % n
    elif(x % 3 == 2):
        b_next = b
    return b_next

xn=[1]
an=[0]
bn=[0]
i=0

while True:
    #找出x[i]=x[2i]对应的i，用flag存储对应的2i的值而不是i，所以下面的第64行，range的第二个参数是flag*0.5+1
    xn.append(fun_x(xn[i]))
    if i >3 and i%2 ==0 and xn[i]==xn[int(0.5*i)]:
        print('i=',i,'\t','x[i]=x[2i]=',xn[i],'\n')
        break
    i += 1
    #print(i,xn[i])

flag = i

for i in range(flag):
    #求出数列an、bn
    an.append(fun_a(an[i],xn[i]))
    bn.append(fun_b(bn[i],xn[i]))

print('{:<5}{:<5}{:<5}{:<5}{:<5}{:<5}{:<5}'.format("i","x[i]","a[i]",'bi','x2i','a2i','b2i'))

for j in range(1,int(flag*0.5)+1):
    print('{:<5}{:<5}{:<5}{:<5}{:<5}{:<5}{:<5}'.format(j,xn[j],an[j],bn[j],xn[2*j],an[2*j],bn[2*j]))

r = (bn[int(flag*0.5)]-bn[flag] )%n
rr = invert(r,n) # 这是r的逆
x= (rr * (an[flag]-an[int(flag*0.5)] ))% n
print('\n离散对数为x=',x)
