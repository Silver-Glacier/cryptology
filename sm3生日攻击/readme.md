# 生日攻击

生日攻击是一种密码学攻击手段，所利用的是概率论中生日问题的数学原理。这种攻击手段可用于滥用两个或多个集团之间的通信。此攻击依赖于在随机攻击中的高碰撞概率和固定置换次数（鸽巢原理）。使用生日攻击，攻击者可在中找到散列函数碰撞，为原像抗性安全性。
![成果截图](https://github.com/Silver-Glacier/cryptology/blob/main/sm3%E7%94%9F%E6%97%A5%E6%94%BB%E5%87%BB/png1.png)

碰撞成功结果

![成果截图](https://github.com/Silver-Glacier/cryptology/blob/main/sm3%E7%94%9F%E6%97%A5%E6%94%BB%E5%87%BB/png2.png)


核心代码部分

```python
if __name__ ==  '__main__':
    iv='7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
    plain = input("请输入明文：")
    B=strtobin(plain)
    for b in B:
        if b!='':
            iv=cf(iv,b)
            result=iv
    print(result)

for i in range(20):
    for _ in diclist:
        iv='7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
        test=testlist+_
        plain=test
        B=strtobin(plain)
        for b in B:
            if b!='':
                iv=cf(iv,b)
                if iv==result:
                    print("明文：",plain,"结果：",iv)
                    quit()
    testlist+=diclist[i]
```
