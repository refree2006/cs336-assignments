# CS336 Assignment 1 Writeup (Self-study)
## rfree2006

## 2.1 The Unicode Standard

**(a)** What Unicode character does `chr(0)` return? 
chr(0) returns the Unicode character U+0000, the NULL control character.
chr(0) 返回的是 Unicode 码位 U+0000 的空字符（NULL 控制字符）。

**(b)** How does this character’s string representation (`__repr__()`) differ from its printed representation?  
In repr it appears as the escape sequence '\x00', but when printed it produces an invisible character and looks like nothing is shown.
在 repr 中它显示为转义序列 '\x00'，而直接打印时是一个不可见的控制字符，看起来好像什么都没输出。

**(c)** What happens when this character occurs in text?  
When inserted into a string it becomes an invisible character between the surrounding text: the printed string looks normal , but repr shows \x00 and the length increases by one.
当它出现在字符串中时，会作为中间的一个不可见字符存在，打印出来的文本看起来正常，但 repr 会显示 \x00，而且字符串长度会多 1。
