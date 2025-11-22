# CS336 Assignment 1 Writeup (Self-study)
## rfree2006

## 2.1 The Unicode Standard

### Problem (unicode1): Understanding Unicode (1 point)

**(a)** What Unicode character does `chr(0)` return? 
```
# Test the code with python
c = chr(0)
print("c:", c)
print("ord(c):", ord(c))
```
```
output:
c: 
ord(c): 0
```
**answer:** 
chr(0) returns the Unicode character U+0000, the NULL control character.
chr(0) 返回的是 Unicode 码位 U+0000 的空字符（NULL 控制字符）。

**(b)** How does this character’s string representation (`__repr__()`) differ from its printed representation?  
```
c = chr(0)

print("repr(c) =", repr(c))
print("print(c) ->", end="")
print(c)
print("<- end")

s = "A" + c + "B"
print("repr(s) =", repr(s))
print("printed:", s)
print("len(s) =", len(s))
```
```
output:
repr(c) = '\x00'
print(c) ->
<- end
repr(s) = 'A\x00B'
printed: AB
len(s) = 3
```
**answer:** 
In repr it appears as the escape sequence '\x00', but when printed it produces an invisible character and looks like nothing is shown.
在 repr 中它显示为转义序列 '\x00'，而直接打印时是一个不可见的控制字符，看起来好像什么都没输出。

**(c)** What happens when this character occurs in text?  
```
c = chr(0)

print("1.", c)
print("2.", "this is a test" + c + "string")
print("3.", repr("this is a test" + c + "string"))
print("4. len:", len("this is a test" + c + "string"))
```
```
output:
1. 
2. this is a teststring
3. 'this is a test\x00string'
4. len: 21
```
**answer:** 
When inserted into a string it becomes an invisible character between the surrounding text: the printed string looks normal , but repr shows \x00 and the length increases by one.
当它出现在字符串中时，会作为中间的一个不可见字符存在，打印出来的文本看起来正常，但 repr 会显示 \x00，而且字符串长度会多 1。

## 2.2 Unicode Encodings

### Problem (unicode2): Unicode Encodings (3 points)
**(a)** What are some reasons to prefer training our tokenizer on UTF-8 encoded bytes, rather than
UTF-16 or UTF-32? It may be helpful to compare the output of these encodings for various
input strings.
```
# The question prompts us to "compare the encoded outputs of various input strings", so we try several different forms of input "such as Chinese, words, emojis, etc." to observe the differences.
# 问题中提示我们”去比较各种输入字符串的这些编码的输出“，由此我们多去尝试几种不同形式的输入“像中文，单词，表情符等等“观察差异。

texts = ["hello", "你好", "🙂", "A你好🙂B"]

for s in texts:
    b8  = s.encode("utf-8")
    b16 = s.encode("utf-16")
    b32 = s.encode("utf-32")
    print("text:", repr(s))
    print(" utf-8 :", b8,  "len =", len(b8))
    print(" utf-16:", b16, "len =", len(b16))
    print(" utf-32:", b32, "len =", len(b32))
    print()
```
```
output:
text: 'hello'
 utf-8 : b'hello' len = 5
 utf-16: b'\xff\xfeh\x00e\x00l\x00l\x00o\x00' len = 12
 utf-32: b'\xff\xfe\x00\x00h\x00\x00\x00e\x00\x00\x00l\x00\x00\x00l\x00\x00\x00o\x00\x00\x00' len = 24

text: '你好'
 utf-8 : b'\xe4\xbd\xa0\xe5\xa5\xbd' len = 6
 utf-16: b'\xff\xfe`O}Y' len = 6
 utf-32: b'\xff\xfe\x00\x00`O\x00\x00}Y\x00\x00' len = 12

text: '🙂'
 utf-8 : b'\xf0\x9f\x99\x82' len = 4
 utf-16: b'\xff\xfe=\xd8B\xde' len = 6
 utf-32: b'\xff\xfe\x00\x00B\xf6\x01\x00' len = 8

text: 'A你好🙂B'
 utf-8 : b'A\xe4\xbd\xa0\xe5\xa5\xbd\xf0\x9f\x99\x82B' len = 12
 utf-16: b'\xff\xfeA\x00`O}Y=\xd8B\xdeB\x00' len = 14
 utf-32: b'\xff\xfe\x00\x00A\x00\x00\x00`O\x00\x00}Y\x00\x00B\xf6\x01\x00B\x00\x00\x00' len = 24
```
**answer:** 
