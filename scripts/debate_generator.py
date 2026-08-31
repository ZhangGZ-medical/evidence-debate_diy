#!/usr/bin/env python3
"""
Evidence Debate — 迭代攻防生成脚本

用途：阶段 3（迭代攻防）
输入：证据矩阵（all_records_graded.json）、攻防轮次配置
输出：每轮攻防的独立文件（R{开始}-{结束}_攻防.md）

使用方法：
    python debate_generator.py --evidence all_records_graded.json --rounds 40 --output ./05_辩论轮次/
"""

import argparse
import json
from pathlib import Path


def generate_round(round_num, evidence, prev_rounds):
    """生成单轮攻防"""
    # 这里是一个模板，实际需要根据具体任务定制
    # 每轮的结构：反方主攻 → 正方反驳 → 再质疑 → 新浮现争点 → 判决
    
    round_md = f"""# 第 {round_num} 轮攻防

> 轮次：R{round_num}
> 证据基础：{len(evidence)} 条候选（全文级 + 摘要级 + 注册库）

---

## 反方主攻

[根据证据矩阵中的关键数据，提出质疑]

### 质疑 1：[质疑标题]

[质疑内容，引用具体数据]

### 质疑 2：[质疑标题]

[质疑内容，引用具体数据]

---

## 正方反驳

[针对反方的质疑，提出反驳]

### 反驳 1：[反驳标题]

[反驳内容，引用具体数据]

### 反驳 2：[反驳标题]

[反驳内容，引用具体数据]

---

## 再质疑（反方）

[针对正方的反驳，提出再质疑]

### 再质疑 1：[再质疑标题]

[再质疑内容，引用具体数据]

---

## 新浮现争点（R{round_num}→R{round_num+1}）

[从上轮的反驳中长出的新争点]

**新争点**：[新争点标题]

[新争点内容]

---

## 判决

| 项目 | 判定 |
|---|---|
| **可达概率** | [X–Y%] |
| **GRADE 等级** | [高/中/低/极低] |
| **降级因素** | [触发的降级因素] |
| **升级因素** | [触发的升级因素] |
| **可证伪条件** | [明确的检验条件] |

**判决**：[判决内容]

---

## 关键数据点

| 数据点 | 数值 | 来源 | 证据等级 |
|---|---|---|---|
| [数据点 1] | [数值] | [来源] | [全文/摘要级/注册库] |
| [数据点 2] | [数值] | [来源] | [全文/摘要级/注册库] |

---

## 引用

[本伦引用的文献，标注获取状态]
"""
    return round_md


def main():
    parser = argparse.ArgumentParser(description='Evidence Debate — 迭代攻防生成')
    parser.add_argument('--evidence', required=True, help='证据矩阵 JSON 文件')
    parser.add_argument('--rounds', type=int, default=40, help='攻防轮次')
    parser.add_argument('--output', required=True, help='输出目录')
    args = parser.parse_args()
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 读取证据矩阵
    with open(args.evidence, encoding='utf-8') as f:
        evidence = json.load(f)
    
    print(f'=== 迭代攻防生成 ===')
    print(f'证据矩阵: {len(evidence)} 条候选')
    print(f'攻防轮次: {args.rounds} 轮')
    
    # 生成每轮攻防
    prev_rounds = []
    for round_num in range(1, args.rounds + 1):
        round_md = generate_round(round_num, evidence, prev_rounds)
        
        # 保存到文件（按 10 轮一组）
        group_start = ((round_num - 1) // 10) * 10 + 1
        group_end = min(group_start + 9, args.rounds)
        group_file = output_dir / f'R{group_start}-R{group_end}_攻防.md'
        
        # 追加到组文件
        mode = 'a' if group_file.exists() else 'w'
        with open(group_file, mode, encoding='utf-8') as f:
            if mode == 'w':
                f.write(f'# 第 {group_start}–{group_end} 轮攻防辩论\n\n')
            f.write(round_md)
            f.write('\n\n---\n\n')
        
        prev_rounds.append(round_num)
        
        if round_num % 10 == 0:
            print(f'  已完成: R{group_start}-R{group_end}')
    
    print(f'\n=== 完成 ===')
    print(f'输出目录: {output_dir}')
    print(f'生成文件: R1-R{args.rounds}_攻防.md（按 10 轮一组）')


if __name__ == '__main__':
    main()
