Rho=set()
count=1
x=1
for c in range(1,100):
  while(count):
    for i in range(0,2**2):
      y=x+c #生成函数
      x=y
      y_byte=str_to_byte(str(y))
      y_EN = sm3.sm3_hash(func.bytes_to_list(y_byte))[0:2] #SM3加密
      if(y_EN in Rho):
        print("得到碰撞长度",(c-1)*(2**2)+i)
        count=0
        break
      else:
        Rho.add(y_EN)
