# MPT
Patricia Merkle Trie提供了一个加密认证的数据结构，可用于存储所有（键，值）的绑定关系。

Patricia Merkle Tries是完全确定的，这意味着具有相同（键，值）绑定的Trie被保证是相同的，直到最后一个字节。这意味着它们有相同的根哈希，为插入、查找和删除提供了O(log(n))效率的圣杯。此外，它们比更复杂的基于比较的替代方案（如红黑树）更容易理解和编码。
### BASIC RADIX TRIES
In a basic radix trie, every node looks as follows:
```
[i0, i1 ... in, value]
```

其中i0 ... in代表字母表的符号（通常是二进制或十六进制），value是节点的终端值，i0 ... in槽中的值要么是NULL，要么是指向其他节点的指针（在我们的例子中是哈希值）。这就形成了一个基本的（键，值）存储。例如，如果你对三段式中当前映射到dog的值感兴趣，你会首先将dog转换成字母（给出64 6f 67），然后沿着这个路径下降三段式，直到找到该值。也就是说，你会先在一个平坦的键/值数据库中查找根哈希，以找到三角形的根节点（这是一个指向其他节点的键的数组），使用索引6的值作为键（并在平坦的键/值数据库中查找它），以获得一级的节点，然后挑选其中的索引4来查找下一个值，然后挑选其中的索引6，以此类推，直到，一旦你遵循路径。根->6->4->6->15->6->7，你就可以查找你所拥有的节点的值并返回结果。

在 "三角形 "中查找东西和底层的平面键/值 "DB "之间是有区别的。它们都定义了键/值的安排，但是底层DB可以对一个键进行传统的1步查询。在 trie 中查询一个键需要多次底层 DB 查询以获得上述的最终值。让我们把后者称为路径，以消除歧义。

radix tries的更新和删除操作很简单，可以大致定义如下。

```
def update(node,path,value):
        if path == '':
            curnode = db.get(node) if node else [ NULL ] * 17
            newnode = curnode.copy()
            newnode[-1] = value
        else:
            curnode = db.get(node) if node else [ NULL ] * 17
            newnode = curnode.copy()
            newindex = update(curnode[path[0]],path[1:],value)
            newnode[path[0]] = newindex
        db.put(hash(newnode),newnode)
        return hash(newnode)

    def delete(node,path):
        if node is NULL:
            return NULL
        else:
            curnode = db.get(node)
            newnode = curnode.copy()
            if path == '':
                newnode[-1] = NULL
            else:
                newindex = delete(curnode[path[0]],path[1:])
                newnode[path[0]] = newindex

            if len(filter(x -> x is not NULL, newnode)) == 0:
                return NULL
            else:
                db.put(hash(newnode),newnode)
                return hash(newnode)

```

Radix trie的 "Merkle "部分产生于这样一个事实：一个节点的确定性加密哈希被用作节点的指针（对于key/value DB中的每一次查找，key == keccak256(rlp(value))），而不是像在C语言实现的更传统的trie中可能发生的一些32位或64位内存位置。这为数据结构提供了一种加密认证形式；如果一个给定的trie的根哈希值是公开的，那么任何人都可以通过提供连接特定值到树根的每个节点的哈希值来证明该trie在特定路径上有一个特定的值。攻击者不可能提供一个不存在的（路径，值）对的证明，因为根哈希值最终是基于它下面的所有哈希值，所以任何修改都会改变根哈希值。

如上所述，在一次一个小数点地遍历路径时，大多数节点包含一个17元素的数组。一个索引表示路径中下一个十六进制字符（nibble）所持有的每个可能的值，还有一个索引表示如果路径已经被完全遍历，则持有最终的目标值。这些17元素数组的节点被称为分支节点。

### MERKLE PATRICIA TRIE

Merkle Patricia试图通过给数据结构增加一些额外的复杂性来解决低效率问题。Merkle Patricia trie中的一个节点是以下之一。

NULL (表示为空字符串)
```
分支 一个17项的节点 [ v0 ... v15, vt ] 。
叶 一个2项节点 [ encodedPath, value ] 。
扩展 一个2项节点 [ encodedPath, key ] 。
```
在64个字符的路径中，在穿越三角形的前几层后，你将不可避免地到达一个节点，在这个节点上至少有一部分是不存在分歧路径的。如果要求这样的节点除了目标索引（路径中的下一个位点）外，每个索引（16个十六进制字符中的每一个）都有空值，那就太天真了。相反，我们通过设置形式为[ encodedPath, key ]的扩展节点来简化下降过程，其中encodedPath包含了向前跳过的 "部分路径"（使用下面描述的紧凑编码），而key是用于下一个db的查找。

在叶子节点的情况下，可以通过encodedPath的第一个nibble中的标志来确定，上面的情况发生了，也是要提前跳过的 "部分路径 "完成了一个路径的全部剩余部分。在这种情况下，值就是目标值本身。

然而，上面的优化引入了一些不明确的地方。

当以nibbles为单位遍历路径时，我们最终可能会有奇数的nibbles需要遍历，但是因为所有的数据都是以字节格式存储的，所以不可能区分，比如说nibble 1，和nibble 01（两者都必须存储为<01>）。为了指定奇数长度，部分路径的前缀是一个标志


每个区块都有自己的Receipts trie。这里的路径是：rlp(transactionIndex)。transactionIndex是它在所开采的区块中的索引。Receipts trie从不更新。与Transactions trie类似，也有当前和遗留的收据。要在Receipts trie中查询一个特定的收据，需要其区块中的交易索引、收据有效载荷和交易类型。返回的收据可以是Receipt类型，定义为交易类型和交易有效载荷的集合，也可以是LegacyReceipt类型，定义为rlp（[status, cumulativeGasUsed, logsBloom, logs]）。
