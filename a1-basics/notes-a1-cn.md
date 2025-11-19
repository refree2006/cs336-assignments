> 目标：写完这份作业之后，我要做到：
> - 能用自己的话解释 GPT 模型的结构和每一层的作用
> - 能从纯文本语料出发训练出一个小语言模型
> - 能看懂并修改训练 loop、loss、optimizer 等代码

---

## 0. A1 在整个课程中的位置

- CS336 大图景：预训练 → 系统加速 → scaling laws → 数据 → 对齐 & RL
- A1 对应的是“预训练 + 模型基础”的部分：
  - Tokenizer
  - Transformer 架构
  - 训练流程

---

## 1. Tokenizer（BPE）

### 1.1 BPE 的核心思想（用自己的话）

（这里以后写：比如从字符级开始、统计 pair 频率、反复 merge 等）

### 1.2 实现细节 & 踩坑记录

- 文件：`../assignment1-basics/src/.../tokenizer_xxx.py`
- 单测：`test_tokenizer_xxx.py`
- 遇到的问题：
  - [ ] 例如：decode 后和原文本不一致的原因？
  - [ ] 哪一步的 merge 逻辑容易写错？

---

## 2. Transformer 模型

### 2.1 模块拆分

- RMSNorm 是什么？和 LayerNorm 的差异？
- SwiGLU 和标准 FFN 的区别？
- RoPE 位置编码的直观理解？
- Multi-head Self-Attention 的输入/输出维度关系？

### 2.2 代码实现路径

- 关键文件路径记录（哪一层在哪个 `.py` 里）
- 单元测试如何覆盖这些模块

### 2.3 Debug 记录

- 报错示例 + 我是如何定位的
- 用 print / assert / 简单输入手算的地方

---

## 3. 训练循环与实验

### 3.1 TinyStories 实验记录

- 模型配置（层数、d_model、heads、context length、batch size、lr 等）
- 训练 loss / valid loss 曲线（可以贴图路径）
- 调参过程：我尝试了哪些超参数组合，效果如何

### 3.2 OWT 子集 + leaderboard 对齐

- 使用的模型配置（要兼顾效果与 1.5 小时 H100 限制）
- 最终 valid loss（context length = 512）
- 学习曲线
- 后续可以改进的方向

---

## 4. 总结与反思

- 我对 Transformer 的理解有哪些“从模糊到清晰”的变化？
- 哪些细节（比如 RoPE、RMSNorm）最容易在实现中踩坑？
- 这次作业对我后面做自己模型（红外超分 / 视频定位）有什么启发？