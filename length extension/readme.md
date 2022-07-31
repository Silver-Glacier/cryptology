 # 长度扩展攻击
 
 长度扩展攻击（length extension attack），是指针对某些允许包含额外信息的加密散列函数的攻击手段。对于满足以下条件的散列函数，都可以作为攻击对象：

       ① 加密前将待加密的明文按一定规则填充到固定长度（例如512或1024比特）的倍数；

       ② 按照该固定长度，将明文分块加密，并用前一个块的加密结果，作为下一块加密的初始向量（Initial Vector）。

成果展示

## 实现思路
随机生成了一个浮点数作为secret，并计算得到了hash值。要得到第一次加密之后8个向量的值，只需要将hash值按8字节分组，并把每组的值转换成int类型(因为python库的sm3实现中向量值是用int型存储的)。

得到了向量值后，便可以开始构造消息。由于我们不需要知道secret的值，只知道secret的长度，所以secret部分可以用等长的任意字符代替(我这里用的是’a')。随后进行padding，得到64字节的消息，再将附加信息放在后面，消息就构造完成了。

接着进行加密，由于此时只需要对附加的消息进行加密，所以我修改了一下sm3的函数实现，增加了一个new_v参数，表示更新之后的向量值。此外这次加密的次数要比之前少一次，从消息的第64字节开始加密，即可得到hash值。
```python
group_count = round(len(msg) / 64) - 1	# 加密次数

    B = []
    for i in range(0, group_count):
        B.append(msg[(i + 1)*64:(i+2)*64])	# 从第64字节开始加密

    V = []
    V.append(new_v)	 # 用更新后的向量值作为初始值
    for i in range(0, group_count):
        V.append(sm3_cf(V[i], B[i]))
```        

![成果截图](https://github.com/Silver-Glacier/cryptology/blob/main/length%20extension/png1.png)

[部分代码引用](https://github.com/hjzin/SM3LengthExtensionAttack)
