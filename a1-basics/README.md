# Assignment 1 - Basics

## 1. 作业目标

- 从零实现一个 Transformer 语言模型：
  - 实现 BPE tokenizer
  - 实现 Decoder-only Transformer（RoPE、RMSNorm、SwiGLU 等）
  - 写完整的训练循环（AdamW、LR schedule、梯度裁剪）
- 在 TinyStories / OpenWebText 子集上训练模型并评估 validation loss
- 尝试向官方 leaderboard 提交结果（Global leaderboard）

> 实际代码实现位置：本地 `../assignment1-basics/`

---

## 2. 本目录结构

- `notes-a1-cn.md`：中文学习笔记与踩坑记录
- `notes-a1-en.md`：英文简要总结
- `exp/`：与 A1 相关的实验脚本和日志（如训练 TinyStories/OWT 的脚本）
- `a1-writeup.md`：unicode1 / unicode2 / tokenizer_experiments ...

```text
a1-basics/
├── README.md
├── notes-a1-cn.md
├── notes-a1-en.md   (optional)
├── a1-writeup.md
└── exp/
    ├── train_tinystories.py (plan)
    ├── train_owt_for_lb.py  (plan)
    └── logs/                (loss 曲线等)
