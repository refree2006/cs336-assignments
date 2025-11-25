# CS336 Assignment 1 Writeup (Self-study)
## rfree2006

---
## 2.1 The Unicode Standard

### Problem (unicode1): Understanding Unicode (1 point)

**(a)** What Unicode character does `chr(0)` return? 
```
# Test the code with python
c = chr(0)
print("c:", c)
print("ord(c):", ord(c))

>>>
c: 
ord(c): 0
```
**Answer:** 
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

>>>
repr(c) = '\x00'
print(c) ->
<- end
repr(s) = 'A\x00B'
printed: AB
len(s) = 3
```
**Answer:** 
    In repr it appears as the escape sequence '\x00', but when printed it produces an invisible character and looks like nothing is shown.

    在 repr 中它显示为转义序列 '\x00'，而直接打印时是一个不可见的控制字符，看起来好像什么都没输出。

**(c)** What happens when this character occurs in text?  
```
c = chr(0)

print("1.", c)
print("2.", "this is a test" + c + "string")
print("3.", repr("this is a test" + c + "string"))
print("4. len:", len("this is a test" + c + "string"))

>>>
1. 
2. this is a teststring
3. 'this is a test\x00string'
4. len: 21
```
**Answer:** 
    When inserted into a string it becomes an invisible character between the surrounding text: the printed string looks normal , but repr shows \x00 and the length increases by one.

    当它出现在字符串中时，会作为中间的一个不可见字符存在，打印出来的文本看起来正常，但 repr 会显示 \x00，而且字符串长度会多 1。

---

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

>>> 
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
**Answer:** 
    "Shorter sequences, more efficient training": UTF-8 is more space-saving (especially for English/ASCII content, one byte and one character), and when including Chinese/emoji, UTF-8 is a longer encoding, but it is still much shorter than UTF-16/32 overall. 
    "Simpler and more compatible": Moreover, almost all real-world corpora are UTF-8 bytes, making it easier and more compatible to build a tokenizer directly on UTF-8 bytes.

    “序列更短，训练更高效”：UTF-8 更节省空间（尤其是英文/ASCII 内容，一字节一字符），包含中文 / emoji 的时候，UTF-8 是变长编码，但依然整体比 UTF-16/32 短很多；
    “更简单、更兼容”：而且现实世界语料几乎都是 UTF-8 bytes，直接在 UTF-8 bytes 上建 tokenizer 更简单、更兼容。

**（b）** Consider the following (incorrect) function, which is intended to decode a UTF-8 byte string into
a Unicode string. Why is this function incorrect? Provide an example of an input byte string
that yields incorrect results.
```
# Provide an example of an input byte string that yields incorrect results.
def decode_utf8_bytes_to_str_wrong(bytestring: bytes):
return "".join([bytes([b]).decode("utf-8") for b in bytestring])

>>> decode_utf8_bytes_to_str_wrong("hello".encode("utf-8"))
'hello'
```
```
def decode_utf8_bytes_to_str_wrong(bytestring: bytes) -> str:
    return "".join(bytes([b]).decode("utf-8") for b in bytestring)

def decode_utf8_bytes_to_str_ok(bytestring: bytes) -> str:
    return bytestring.decode("utf-8")

# ASCII
s_ascii = "hello"
b_ascii = s_ascii.encode("utf-8")
print("ASCII bytes:", b_ascii)
print("wrong:", decode_utf8_bytes_to_str_wrong(b_ascii))
print(" ok  :", decode_utf8_bytes_to_str_ok(b_ascii))

# non-ASCII 
s_non = "你好"           # 或者 "🙂" 之类
b_non = s_non.encode("utf-8")
print("\nnon-ASCII bytes:", b_non)
print("wrong:", decode_utf8_bytes_to_str_wrong(b_non))
print(" ok  :", decode_utf8_bytes_to_str_ok(b_non))

>>>
ASCII bytes: b'hello'
wrong: hello
 ok  : hello

non-ASCII bytes: b'\xe4\xbd\xa0\xe5\xa5\xbd'
Traceback (most recent call last):
  File "e:\Vscode_project\python\ceshi.py", line 18, in <module>
    print("wrong:", decode_utf8_bytes_to_str_wrong(b_non))
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "e:\Vscode_project\python\ceshi.py", line 2, in decode_utf8_bytes_to_str_wrong
    return "".join(bytes([b]).decode("utf-8") for b in bytestring)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "e:\Vscode_project\python\ceshi.py", line 2, in <genexpr>
    return "".join(bytes([b]).decode("utf-8") for b in bytestring)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe4 in position 0: unexpected end of data
```
**Explanation:**
    For "hello", both output is the same (because ASCII is single byte in UTF-8);
    For "你好" / emoji characters that require a multi-byte UTF-8 sequence,"decode_utf8_bytes_to_str_ok" gets the correct string; "decode_utf8_bytes_to_str_wrong" either reports an error or becomes the result of confusion.

**Answer:**

Error examples:
    s_non = "你好"/"🙂"/"é"

Reason:
    This function decodes each individual byte as a full UTF-8 character, and the correct approach should be to decode the entire byte string together in UTF-8. When multi-byte characters are taken apart, errors occur.

    这个函数把每个 单独的字节 当成一个完整的 UTF-8 字符去解码，而正确的做法应该是把整个字节串一起按 UTF-8 解码。多字节字符被拆开，就会出错。

**（c）** Give a two byte sequence that does not decode to any Unicode character(s).
```
candidates = [
    bytes([0xC3, 0x28]),
    bytes([0x80, 0x80]),
    bytes([0xFF, 0xFF]),
]

for b in candidates:
    print("testing:", b)
    try:
        print(" decoded:", b.decode("utf-8"))
    except UnicodeDecodeError as e:
        print(" UnicodeDecodeError:", e)
    print()

>>>
    testing: b'\xc3('
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc3 in position 0: invalid continuation byte

    testing: b'\x80\x80'
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte

    testing: b'\xff\xff'
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```
**Answer:**

Error examples: bytes([0xC3, 0x28]).

Reason: 
*UTF-8 define:*
    The first byte of the two-byte character should be 110xxxxx ,
    The second byte must be 10xxxxxx;
    
    *UTF-8 编码规则：*
    两字节字符首字节应是 110xxxxx,
    第二个字节必须是 10xxxxxx；

---

## 2.4 BPE Tokenizer Training

### Example (bpe_example): BPE training example
You can find a simple code implementation of the experiment under this path： 

你可以找到实验的简易代码实现在该路径下：
`cs336-assignments/a1-basics/exp/bpe_example.py`
你可以找到实验的简易代码实现在该路径下：

```
# The relevant results are as follows：
# 相关运行结果如下：
python a1-basics/exp/bpe_example.py

>>>
word_counts: Counter({'low': 5, 'newest': 5, 'widest': 3, 'lower': 2, 'and': 1, 'the': 1, 'vocabulary': 1, 'has': 1, 'a': 1, 'special': 1, 'token': 1, '<endoftext>.': 1})
word_tokens:
  low -> (b'l', b'o', b'w')
  lower -> (b'l', b'o', b'w', b'e', b'r')
  widest -> (b'w', b'i', b'd', b'e', b's', b't')
  newest -> (b'n', b'e', b'w', b'e', b's', b't')
  and -> (b'a', b'n', b'd')
  the -> (b't', b'h', b'e')
  vocabulary -> (b'v', b'o', b'c', b'a', b'b', b'u', b'l', b'a', b'r', b'y')
  has -> (b'h', b'a', b's')
  a -> (b'a',)
  special -> (b's', b'p', b'e', b'c', b'i', b'a', b'l')
  token -> (b't', b'o', b'k', b'e', b'n')
  <endoftext>. -> (b'<', b'e', b'n', b'd', b'o', b'f', b't', b'e', b'x', b't', b'>', b'.')

pair_counts:
 (<, e) -> 1
 (>, .) -> 1
 (a, b) -> 1
 (a, l) -> 1
 (a, n) -> 1
 (a, r) -> 1
 (a, s) -> 1
 (b, u) -> 1
 (c, a) -> 1
 (c, i) -> 1
 (d, e) -> 3
 (d, o) -> 1
 (e, c) -> 1
 (e, n) -> 2
 (e, r) -> 2
 (e, s) -> 8
 (e, w) -> 5
 (e, x) -> 1
 (f, t) -> 1
 (h, a) -> 1
 (h, e) -> 1
 (i, a) -> 1
 (i, d) -> 3
 (k, e) -> 1
 (l, a) -> 1
 (l, o) -> 7
 (n, d) -> 2
 (n, e) -> 5
 (o, c) -> 1
 (o, f) -> 1
 (o, k) -> 1
 (o, w) -> 7
 (p, e) -> 1
 (r, y) -> 1
 (s, p) -> 1
 (s, t) -> 8
 (t, >) -> 1
 (t, e) -> 1
 (t, h) -> 1
 (t, o) -> 1
 (u, l) -> 1
 (v, o) -> 1
 (w, e) -> 7
 (w, i) -> 3
 (x, t) -> 1

Best pair to merge: (b's', b't') freq: 8
  as chars: s t

newest tokens before: (b'n', b'e', b'w', b'e', b's', b't')
newest tokens after merge 's','t': (b'n', b'e', b'w', b'e', b'st')

Merges sequence:
  s t
  e st
  o w
  l ow
  w est
  n e

Final tokens per word:
  low -> ['low']
  lower -> ['low', 'e', 'r']
  widest -> ['w', 'i', 'd', 'est']
  newest -> ['ne', 'west']
  and -> ['a', 'n', 'd']
  the -> ['t', 'h', 'e']
  vocabulary -> ['v', 'o', 'c', 'a', 'b', 'u', 'l', 'a', 'r', 'y']
  has -> ['h', 'a', 's']
  a -> ['a']
  special -> ['s', 'p', 'e', 'c', 'i', 'a', 'l']
  token -> ['t', 'o', 'k', 'e', 'n']
  <endoftext>. -> ['<', 'e', 'n', 'd', 'o', 'f', 't', 'e', 'x', 't', '>', '.']

Tokenization of 'newest': ['ne', 'west']
```

---