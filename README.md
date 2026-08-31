# Evidence Debate Skill — 对抗式循证辩论工作流

> 版本：v1.0 | 创建日期：2026-08-31
> 来源项目：761TEL 两条 NSC 管线临床疗效可达性评估（40 轮攻防、180 条候选、90 篇全文级）

---

## 这个 Skill 是什么

**对抗式循证辩论工作流**——从证据穷尽、全文获取、迭代攻防到证据分级、多版本交付的完整方法论。

**核心特点**：
- **穷尽可靠文献**：不是"找几篇代表性的"，而是"穷尽所有相关的"
- **全文级证据优先**：能下载全文的必须下载全文，不能下载全文的只能用摘要中明确说明的数据
- **迭代攻防**：每轮反方主攻→正方反驳→新浮现争点→判决，直到收敛
- **GRADE 证据分级**：每条结论都标注证据确定性等级，不是"有效/无效"的二元判断
- **可证伪条件**：每个判决都给出"什么情况下这个判决会被推翻"的明确条件
- **多版本交付**：完整演化版（内部决策）+ 精简结论版（对外汇报）

---

## 安装

### 前置要求

| 项目 | 要求 | 说明 |
|---|---|---|
| **Python** | 3.10+ | 推荐 3.13.12（managed） |
| **Git** | 任意版本 | 用于克隆依赖仓库 |
| **网络** | 可访问 GitHub | 克隆依赖技能 |

**技能安装根目录**：`~/.workbuddy/skills/`

### 一键安装（推荐）

```bash
# 设置技能根目录
SKILLS_ROOT="$HOME/.workbuddy/skills"
mkdir -p "$SKILLS_ROOT" && cd "$SKILLS_ROOT"

# 1. 安装本技能
git clone https://github.com/ZhangGZ-medical/evidence-debate_diy.git

# 2. 安装全部依赖技能
git clone https://github.com/ZhangGZ-medical/ms-search-lit.git            # 核心：PubMed 检索
git clone https://github.com/ZhangGZ-medical/ms-fulltext-retrieval.git     # 核心：Europe PMC 全文获取
git clone https://github.com/ZhangGZ-medical/md2docx_diy.git               # 核心：MD → DOCX 转换
git clone https://github.com/ZhangGZ-medical/agent-review_diy.git          # 可选：五维审查
git clone https://github.com/ZhangGZ-medical/fable5-workflow_diy.git       # 可选：工作流编排

echo "安装完成"
```

### 手动安装

如果只需要最小可用配置，安装**三个核心依赖**即可：

| 技能 | GitHub 地址 | 必需性 |
|---|---|---|
| **ms-search-lit** | https://github.com/ZhangGZ-medical/ms-search-lit | ✅ 必需 |
| **ms-fulltext-retrieval** | https://github.com/ZhangGZ-medical/ms-fulltext-retrieval | ✅ 必需 |
| **md2docx_diy** | https://github.com/ZhangGZ-medical/md2docx_diy | ✅ 必需 |
| agent-review_diy | https://github.com/ZhangGZ-medical/agent-review_diy | ⭕ 可选（推荐） |
| fable5-workflow_diy | https://github.com/ZhangGZ-medical/fable5-workflow_diy | ⭕ 可选（推荐） |

```bash
cd "$HOME/.workbuddy/skills"
git clone <上表中的地址>
```

### 安装后目录结构

```
~/.workbuddy/skills/
├── evidence-debate_diy/          # 本技能
│   ├── SKILL.md
│   ├── README.md
│   ├── references/
│   └── scripts/
├── ms-search-lit/                # 依赖 1（核心）
│   └── references/
│       ├── pubmed_eutils.sh
│       ├── parse_pubmed.py
│       └── snowball.py
├── ms-fulltext-retrieval/        # 依赖 2（核心）
│   ├── fetch_oa.py
│   ├── pdf_to_md.py
│   └── references/
│       ├── epmc_search.py
│       ├── jats_to_text.py
│       ├── ctr_fetch.py
│       └── find_available_pdf.js
├── md2docx_diy/                  # 依赖 3（核心）
│   └── md2docx_diy.py
├── agent-review_diy/             # 依赖 4（可选）
└── fable5-workflow_diy/          # 依赖 5（可选）
```

### Python 依赖安装

```bash
PY="C:/Users/G1381/.workbuddy/binaries/python/versions/3.13.12/python.exe"

# PDF 处理（ms-fulltext-retrieval 的 pdf_to_md.py 需要）
"$PY" -m pip install pymupdf

# PDF → Markdown（可选，AGPL-3.0）
"$PY" -m pip install pymupdf4llm
```

> **注意**：`fetch_oa.py` 与 `references/` 下的脚本（`epmc_search.py`、`jats_to_text.py`、`ctr_fetch.py`）均为 **stdlib only**，无需额外依赖。
> 只有 `pdf_to_md.py` 需要 `pymupdf4llm`。

### 验证安装

```bash
SKILLS_ROOT="$HOME/.workbuddy/skills"

# 检查目录
for D in evidence-debate_diy ms-search-lit ms-fulltext-retrieval md2docx_diy; do
    [ -d "$SKILLS_ROOT/$D" ] && echo "[OK]   $D" || echo "[MISS] $D"
done

# 检查关键脚本
for F in \
  "$SKILLS_ROOT/ms-search-lit/references/pubmed_eutils.sh" \
  "$SKILLS_ROOT/ms-search-lit/references/parse_pubmed.py" \
  "$SKILLS_ROOT/ms-fulltext-retrieval/references/epmc_search.py" \
  "$SKILLS_ROOT/ms-fulltext-retrieval/references/jats_to_text.py" \
  "$SKILLS_ROOT/ms-fulltext-retrieval/references/ctr_fetch.py" \
  "$SKILLS_ROOT/md2docx_diy/md2docx_diy.py"; do
    [ -f "$F" ] && echo "[OK]   $(basename $F)" || echo "[MISS] $(basename $F)"
done
```

**全部显示 `[OK]` 即安装成功。**

### 功能自检

```bash
PY="C:/Users/G1381/.workbuddy/binaries/python/versions/3.13.12/python.exe"
S="$HOME/.workbuddy/skills/ms-fulltext-retrieval"

# 测试 Europe PMC 检索
"$PY" "$S/references/epmc_search.py" search 'HAS_FT:Y AND OPEN_ACCESS:Y AND "chronic stroke"' -n 3

# 测试注册库取数
"$PY" "$S/references/ctr_fetch.py" NCT02448641
```

---

## 依赖关系

### 核心依赖技能（必须）

| 技能 | 用途 | GitHub 地址 |
|---|---|---|
| **ms-search-lit** | PubMed E-utilities 全量检索 | https://github.com/ZhangGZ-medical/ms-search-lit |
| **ms-fulltext-retrieval** | Europe PMC 全文获取、JATS 解析、注册库取数 | https://github.com/ZhangGZ-medical/ms-fulltext-retrieval |
| **md2docx_diy** | Markdown → DOCX 转换（纵向 A4） | https://github.com/ZhangGZ-medical/md2docx_diy |

### 可选依赖技能（推荐）

| 技能 | 用途 | GitHub 地址 |
|---|---|---|
| **agent-review_diy** | 五维审查（事实性/完整性/逻辑一致性/格式合规/AI 味） | https://github.com/ZhangGZ-medical/agent-review_diy |
| **fable5-workflow_diy** | 工作流编排（阶段 0–6） | https://github.com/ZhangGZ-medical/fable5-workflow_diy |

### 关键脚本依赖

| 脚本 | 用途 | 所属技能 |
|---|---|---|
| `pubmed_eutils.sh` | PubMed E-utilities 检索 | ms-search-lit |
| `parse_pubmed.py` | PubMed 结果解析 | ms-search-lit |
| `snowball.py` | 引文网络滚雪球扩展 | ms-search-lit |
| `epmc_search.py` | Europe PMC 检索与全文下载 | ms-fulltext-retrieval |
| `jats_to_text.py` | JATS XML → 纯文本转换 | ms-fulltext-retrieval |
| `ctr_fetch.py` | ClinicalTrials.gov 注册库取数 | ms-fulltext-retrieval |
| `fetch_oa.py` | OA 级联 PDF 下载（传统通道） | ms-fulltext-retrieval |
| `md2docx_diy.py` | Markdown → DOCX 转换 | md2docx_diy |

### 运行环境

| 项目 | 要求 |
|---|---|
| **Python** | 3.10+（推荐 3.13.12 managed） |
| **Python 包** | `pymupdf`（必需）、`pymupdf4llm`（可选） |
| **网络服务** | Europe PMC（`www.ebi.ac.uk`）、ClinicalTrials.gov（`clinicaltrials.gov`）、PubMed（`eutils.ncbi.nlm.nih.gov`） |
| **磁盘空间** | <100 MB（180 篇全文 XML 约 20–30 MB） |

---

## 快速开始

### 1. 准备维度分解

创建 `dimensions.json`，定义检索维度：

```json
{
  "IA_NSC_stroke": "intra-arterial neural stem cell stroke",
  "IC_NSC_chronic": "intracerebral neural stem cell chronic stroke transplant",
  "FMMS_placebo": "Fugl-Meyer chronic stroke sham placebo",
  "DTI_CST": "diffusion tensor imaging corticospinal tract stroke recovery prediction",
  "homing": "neural stem cell homing ischemic stroke migration",
  "synaptic": "neural stem cell synaptic integration circuit reconstruction",
  "exosome": "neural stem cell exosome extracellular vesicle stroke therapy",
  "cochrane": "Cochrane stem cell ischemic stroke systematic review"
}
```

参考：`scripts/dimensions_example.json`

### 2. 执行证据穷尽与全文获取

```bash
PY="C:/Users/G1381/.workbuddy/binaries/python/versions/3.13.12/python.exe"

"$PY" scripts/evidence_exhaust.py \
  --dimensions dimensions.json \
  --output ./output/ \
  --retmax 50
```

**输出**：
- `output/01_全文_JATS/`：下载的全文 XML
- `output/02_解析文本/`：解析后的纯文本
- `output/04_证据矩阵/`：候选清单、分级结果

### 3. 执行迭代攻防

```bash
"$PY" scripts/debate_generator.py \
  --evidence output/04_证据矩阵/all_records_graded.json \
  --rounds 40 \
  --output output/05_辩论轮次/
```

**输出**：`output/05_辩论轮次/R1-R10_攻防.md` 等（按 10 轮一组）

### 4. 生成多版本交付

```bash
"$PY" scripts/delivery_generator.py \
  --full output/00_交付/完整版.md \
  --output output/00_交付/
```

**输出**：精简版 MD + DOCX

---

## 目录结构

```
{workspace}/subproj-{任务名}/
├── 00_交付/                    # 最终交付物（MD + DOCX）
├── 01_全文_JATS/               # 下载的全文 XML
├── 02_解析文本/                # 解析后的纯文本
├── 03_注册库结果/              # ClinicalTrials.gov 注册库数据
├── 04_证据矩阵/                # 证据索引、候选清单、分级结果
├── 05_辩论轮次/                # 每轮攻防的独立文件
└── 06_日志/                    # 执行日志
```

---

## 核心文件

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 完整的工作流文档（六阶段） |
| `README.md` | 本文件（安装、依赖、快速开始） |
| `references/dimension_decomposition.md` | 维度分解参考（阶段 1） |
| `references/grade_assessment.md` | GRADE 证据分级参考（阶段 4） |
| `scripts/evidence_exhaust.py` | 证据穷尽与全文获取（阶段 1–2） |
| `scripts/debate_generator.py` | 迭代攻防生成（阶段 3） |
| `scripts/delivery_generator.py` | 多版本交付生成（阶段 6） |
| `scripts/dimensions_example.json` | 维度分解示例 |

---

## 使用示例

### 示例 1：评估某条技术路线的疗效可达性

```
用户输入：评估 761TEL 管线一（IA 给药 NSC × 亚急性卒中）的临床疗效可达性

执行流程：
1. 阶段 0：任务分类 → A 线（深度调研 + 复杂推理辩论）
2. 阶段 1：证据穷尽
   - 维度分解：IA 给药 NSC 卒中、亚急性期、剂量-效应、安全性、时间窗
   - 全量检索：每个维度 50 条，合并去重后 37 条
3. 阶段 2：全文获取与证据分级
   - 全文可得性判定：9 篇全文级 / 28 篇摘要级
   - 批量下载与解析：9 篇全文级
   - 注册库数据：NCT02448641（ACTIsSIMA）
4. 阶段 3：迭代攻防（40 轮）
   - R1–R4：识别表面问题（递送效率、安全性、初步疗效）
   - R5–R10：深入到机制层面（细胞替代 vs 旁分泌、体内分化、剂量-效应）
   - R11–R20：重新定位（超选给药、时间窗效应、影像学分层）
   - R21–R30：穷尽证据（时间窗梯度、资源分配、核心叙事）
   - R31–R40：收敛（最终判决与行动建议）
5. 阶段 4：证据分级与跨层一致性检验
   - GRADE 分级：低（降级：间接性、不精确性、不一致性）
   - 跨层一致性：L1+L2 强、L3 弱 = 典型转化失败模式
6. 阶段 5：可证伪条件与行动建议
   - 可证伪条件：若 IIT 中 N 例患者 90 天 mRS ≤2 比例 <10%，则路线不成立
   - 行动建议：明确机制主张（旁分泌主导），补充超选 IA 体内药代数据
7. 阶段 6：多版本交付
   - 完整演化版：42,414 字，128 条参考文献
   - 精简结论版：33,837 字，115 条参考文献
```

### 示例 2：科学尽职调查

```
用户输入：帮我做 761TEL 的科学尽职调查，评估两条管线的投资价值

执行流程：
1. 阶段 0：任务分类 → A 线
2. 阶段 1：证据穷尽
   - 维度分解：管线一（IA 给药 NSC × 亚急性）、管线二（脑内移植 NSC × 慢性）、
     管线三（外泌体）、对照（安慰效应、自然恢复）、影像学（DTI/CST）、系统综述
   - 全量检索：每个维度 50 条，合并去重后 180 条
3. 阶段 2：全文获取与证据分级
   - 全文可得性判定：90 篇全文级 / 87 篇摘要级 / 2 项注册库 / 1 篇排除
   - 批量下载与解析：106 篇 XML、108 篇解析文本
   - 注册库数据：NCT02448641（ACTIsSIMA）、NCT03296618（NSI-566）
4. 阶段 3：迭代攻防（40 轮）
   - 管线一：R1–R20（超选给药、剂量-效应、时间窗效应）
   - 管线二：R1–R40（安慰效应边界、数据不相容、影像学分层、资源分配）
   - 跨管线：R14–R40（自洽性、外泌体、资源分配、核心叙事）
5. 阶段 4：证据分级与跨层一致性检验
   - 管线一：GRADE 低，可达概率 15–25%
   - 管线二：GRADE 中低，可达概率 25–35%
   - 管线三：GRADE —，科学自洽性最高
6. 阶段 5：可证伪条件与行动建议
   - 管线一：明确机制主张（旁分泌主导），补充超选 IA 体内药代数据
   - 管线二：IIT 设计必须含假手术对照 + 影像学分层 + 双终点 + 年龄分层
   - 管线三：确定效应 miRNA（效力表征）
7. 阶段 6：多版本交付
   - 完整演化版：42,414 字，128 条参考文献
   - 精简结论版：33,837 字，115 条参考文献
   - 资源分配建议：管线一 30% + 管线二 40% + 管线三 30%
```

---

## 关键经验与陷阱

详见 `SKILL.md` 的"关键经验与陷阱"部分。核心要点：

1. **检索穷尽性原则**：不要"找几篇代表性的"，要"穷尽所有相关的"
2. **全文获取的证据分级**：能下载全文的必须下载全文，不能下载全文的只能用摘要中明确说明的数据
3. **迭代攻防的争点演化**：每轮必须产生新浮现争点，从上轮的反驳中长出
4. **GRADE 证据分级**：每条结论都要标注证据确定性等级
5. **可证伪条件的重要性**：每个判决都要给出"什么情况下这个判决会被推翻"的明确条件
6. **多版本交付的必要性**：完整演化版（内部决策）+ 精简结论版（对外汇报）
7. **检索疏漏的防范**：用产品代号检索后，必须逐篇核对命中结果
8. **数据核对的必要性**：所有数据必须核对，不能凭印象写
9. **中间判决值与最终值的一致性**：中间轮的判决值与最终值必须标注清楚
10. **参考文献的完整性**：下载了的所有全文级文献，都必须在参考文献中体现

---

## 常见问题

### Q1: 这个 Skill 需要联网吗？

**A:** 需要。核心功能依赖三个网络服务：
- **Europe PMC**（全文获取与检索）
- **ClinicalTrials.gov**（注册库数据）
- **PubMed**（E-utilities 检索）

如果网络不可用，只能使用已下载的本地文献进行攻防。

### Q2: 依赖的技能如果不存在怎么办？

**A:** 三个核心依赖技能（ms-search-lit、ms-fulltext-retrieval、md2docx_diy）是**必须的**，如果不存在则无法运行。两个可选依赖技能（agent-review_diy、fable5-workflow_diy）是**推荐的**，如果不存在可以跳过相应的审查与编排步骤。

按上文「安装」章节的 GitHub 地址克隆即可。

### Q3: 能否用于其他领域（非医学）？

**A:** 可以。核心方法论（穷尽证据、对抗式审视、分级评估、可证伪输出）是**领域无关**的，只需要调整维度分解与检索词。但当前的依赖技能（ms-search-lit、ms-fulltext-retrieval）是**医学专用**的，如果用于其他领域需要替换相应的检索与全文获取工具。

### Q4: 攻防轮次可以自定义吗？

**A:** 可以。`debate_generator.py` 的 `--rounds` 参数支持自定义轮次（默认 40 轮）。建议：
- 简单问题：**10–20 轮**
- 中等问题：**30–40 轮**
- 复杂问题：**50+ 轮**

### Q5: 能否只生成精简版，不生成完整版？

**A:** 可以。但**不推荐**——完整版是精简版的基础，精简版是从完整版中提取的。如果只需要精简版，可以先生成完整版，然后用 `delivery_generator.py` 提取精简版。

### Q6: 安装后提示 Python 路径不对怎么办？

**A:** 本技能的脚本中硬编码了 managed Python 路径：
`C:/Users/G1381/.workbuddy/binaries/python/versions/3.13.12/python.exe`

如果你的环境不同，需要修改以下文件中的 `PY` 变量：
- `scripts/evidence_exhaust.py`
- `scripts/delivery_generator.py`

### Q7: 上传到 GitHub 前需要注意什么？

**A:** 使用 `github_upload_diy` 技能上传时，注意排除 `__pycache__` / `*.pyc` / `.git`。可参考 `subproj-疗效预测/06_日志/upload_skills_github.py` 中的 `EXCLUDE_DIRS` 与 `EXCLUDE_EXT` 配置。

---

## 版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0.0 | 2026-08-31 | 初始版本，基于 761TEL 两条 NSC 管线临床疗效可达性评估任务（40 轮攻防、180 条候选、90 篇全文级）固化 |

---

## 相关仓库

| 仓库 | 说明 |
|---|---|
| https://github.com/ZhangGZ-medical/evidence-debate_diy | **本技能** |
| https://github.com/ZhangGZ-medical/ms-search-lit | 依赖：PubMed 检索 |
| https://github.com/ZhangGZ-medical/ms-fulltext-retrieval | 依赖：全文获取（含本项目实地验证补丁） |
| https://github.com/ZhangGZ-medical/md2docx_diy | 依赖：MD → DOCX |
| https://github.com/ZhangGZ-medical/agent-review_diy | 依赖：五维审查 |
| https://github.com/ZhangGZ-medical/fable5-workflow_diy | 依赖：工作流编排 |

---

## 核心价值

**让结论可以被检验，而不是永远正确。**

这个 skill 固化的不是一个"模板"，而是一个**方法论**——如何**穷尽证据、对抗式审视、分级评估、可证伪输出**。它适用于任何需要**科学尽职调查**的场景：评估技术路线的可行性、判断科学主张的可信度、支持投资决策的证据基础。
