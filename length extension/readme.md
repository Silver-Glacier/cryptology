 # 长度扩展攻击
 
 长度扩展攻击（length extension attack），是指针对某些允许包含额外信息的加密散列函数的攻击手段。对于满足以下条件的散列函数，都可以作为攻击对象：

       ① 加密前将待加密的明文按一定规则填充到固定长度（例如512或1024比特）的倍数；

       ② 按照该固定长度，将明文分块加密，并用前一个块的加密结果，作为下一块加密的初始向量（Initial Vector）。

成果展示

![成果截图](https://github.com/Silver-Glacier/cryptology/blob/main/length%20extension/png1.png)

[部分代码引用](https://github.com/hjzin/SM3LengthExtensionAttack)
