# a1-basics/exp/2.4 BPE Tokenizer Training_bpe_example.py
from collections import Counter
from collections import defaultdict

# 1. 准备语料信息（PDF 里的那段 low / lower / widest / newest + <endoftext>）

corpus = """low low low low low
lower lower widest widest widest
newest newest newest newest newest
and the vocabulary has a special token <endoftext>.
"""

SPECIAL = "<endoftext>"

# 2. 初始化 vocab：先有 SPECIAL，再加 256 个 byte token


# 3. 预分词：这个 toy 例子里就用空格 split

words = corpus.strip().split()
word_counts = Counter(words) # 统计每个单词出现次数
print("word_counts:", word_counts) # 得到 {b"low":5, b"lower":2, ...} 的频数表


# 4. 把每个词转成 UTF-8 bytes：

def word_to_tokens_bytes(word : str):
    b = word.encode("utf-8")          # 比如 b"low"
    return tuple(bytes([x]) for x in b)   # (b'l', b'o', b'w')

word_tokens = {w: word_to_tokens_bytes(w) for w in word_counts.keys()}
print("word_tokens:")
for w, toks in word_tokens.items():
    print(" ", w, "->", toks)


# 5. 循环：
#    - 找出出现次数最多的 pair（ties 用字典序最大那个）
#    - 把这个 pair merge 成一个新的 token
#    - 更新“词”的表示，重复几轮，直到得到 PDF 示例里的结果

def get_pair_counts(word_tokens: dict[str, tuple[bytes, ...]],
                    word_counts: Counter) -> dict[tuple[bytes, bytes], int]:
    pair_counts = defaultdict(int)
    for word, freq in word_counts.items():
        tokens = word_tokens[word]
        # 相邻 pair： (t0, t1), (t1, t2), ...
        for a, b in zip(tokens, tokens[1:]):
            pair_counts[(a, b)] += freq
    return pair_counts

pair_counts = get_pair_counts(word_tokens, word_counts)
print("\npair_counts:")
for (a, b), c in sorted(pair_counts.items(),
                        key=lambda item: (item[0][0], item[0][1])):
    print(f" ({a.decode()}, {b.decode()}) -> {c}")

best_pair, best_freq = max(
    pair_counts.items(),
    key=lambda item: (item[1], item[0])  # 先比频数，再比 pair 字典序，作业中提到优先选字典序更大的那一对（PDF2.4中）
)
print("\nBest pair to merge:", best_pair, "freq:", best_freq)
print("  as chars:", best_pair[0].decode(), best_pair[1].decode())

def merge_pair(tokens: tuple[bytes, ...],
               pair: tuple[bytes, bytes]) -> tuple[bytes, ...]:
    a, b = pair
    i = 0
    new_tokens: list[bytes] = []
    while i < len(tokens):
        # 检查当前位置和下一个位置是否匹配 (a, b)
        if i < len(tokens) - 1 and tokens[i] == a and tokens[i + 1] == b:
            new_tokens.append(a + b)   # 合并成一个新 token
            i += 2                     # 跳过两个位置
        else:
            new_tokens.append(tokens[i])
            i += 1
    return tuple(new_tokens)
example = word_tokens["newest"]
print("\nnewest tokens before:", example)
print("newest tokens after merge 's','t':",
      merge_pair(example, best_pair))


# 6. 最后打印：
#    - merges 序列
#    - 单词 "newest" tokenized 成什么（应该和 PDF 一样）

def run_bpe(word_counts: Counter,
            num_merges: int = 6):
    # 初始：每个词都是单字节 token 序列
    word_tokens = {w: word_to_tokens_bytes(w) for w in word_counts}
    merges: list[tuple[bytes, bytes]] = []

    for _ in range(num_merges):
        pair_counts = get_pair_counts(word_tokens, word_counts)
        best_pair, freq = max(pair_counts.items(),
                              key=lambda item: (item[1], item[0]))
        merges.append(best_pair)

        # 在所有词上做 merge
        for w in word_tokens:
            word_tokens[w] = merge_pair(word_tokens[w], best_pair)

    return merges, word_tokens

# 跑 6 次 merge（和 PDF 例子一致）
merges, final_tokens = run_bpe(word_counts, num_merges=6)

print("\nMerges sequence:")
for a, b in merges:
    print(" ", a.decode(), b.decode())

print("\nFinal tokens per word:")
for w, toks in final_tokens.items():
    print(" ", w, "->", [t.decode() for t in toks])

print("\nTokenization of 'newest':",
      [t.decode() for t in final_tokens["newest"]])
