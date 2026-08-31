#!/usr/bin/env python3
"""
Evidence Debate — 多版本交付生成脚本

用途：阶段 6（多版本交付）
输入：完整版报告（MD）、精简版配置
输出：精简版报告（MD + DOCX）

依赖：
- md2docx_diy（Markdown → DOCX 转换）

使用方法：
    python delivery_generator.py --full full_report.md --output ./00_交付/
"""

import argparse
import re
import subprocess
from pathlib import Path

# 依赖路径
MD2DOCX = "C:/Users/G1381/.workbuddy/skills/md2docx_diy"
PY = "C:/Users/G1381/.workbuddy/binaries/python/versions/3.13.12/python.exe"


def extract_final_conclusions(full_md):
    """从完整版中提取最终结论"""
    # 提取执行摘要
    exec_summary = re.search(r'## 执行摘要(.+?)(?=\n## )', full_md, re.DOTALL)
    if exec_summary:
        exec_summary = exec_summary.group(1)
    else:
        exec_summary = ""
    
    # 提取方法学声明
    methodology = re.search(r'## 0\. 方法学声明(.+?)(?=\n## )', full_md, re.DOTALL)
    if methodology:
        methodology = methodology.group(1)
    else:
        methodology = ""
    
    # 提取各管线的最终判决（一号争点 + 二号争点的收敛判决）
    pipeline1_verdict = re.search(r'### 1\.0 【一号争点】(.+?)#### 收敛判决(.+?)(?=\n### 1\.1)', full_md, re.DOTALL)
    pipeline1_verdict2 = re.search(r'### 1\.1 【二号争点】(.+?)#### 收敛判决(.+?)(?=\n### 1\.2)', full_md, re.DOTALL)
    
    pipeline2_verdict = re.search(r'### 2\.0 【一号争点】(.+?)#### 收敛判决(.+?)(?=\n### 2\.1)', full_md, re.DOTALL)
    
    # 提取交叉辩论
    cross_debate = re.search(r'## 3\. 交叉辩论(.+?)(?=\n## )', full_md, re.DOTALL)
    if cross_debate:
        cross_debate = cross_debate.group(1)
    else:
        cross_debate = ""
    
    # 提取双线判决总表
    verdict_table = re.search(r'## 4\. 双线判决总表(.+?)(?=\n## )', full_md, re.DOTALL)
    if verdict_table:
        verdict_table = verdict_table.group(1)
    else:
        verdict_table = ""
    
    # 提取既有报告乐观偏差修正清单
    corrections = re.search(r'## 5\. 既有报告乐观偏差修正清单(.+?)(?=\n## )', full_md, re.DOTALL)
    if corrections:
        corrections = corrections.group(1)
    else:
        corrections = ""
    
    # 提取三层证据矩阵
    evidence_matrix = re.search(r'## 6\. 三层证据矩阵(.+?)(?=\n## )', full_md, re.DOTALL)
    if evidence_matrix:
        evidence_matrix = evidence_matrix.group(1)
    else:
        evidence_matrix = ""
    
    # 提取参考文献
    references = re.search(r'## 参考文献(.+?)(?=\n## )', full_md, re.DOTALL)
    if references:
        references = references.group(1)
    else:
        references = ""
    
    return {
        'exec_summary': exec_summary,
        'methodology': methodology,
        'pipeline1_verdict': pipeline1_verdict.group(2) if pipeline1_verdict else "",
        'pipeline1_verdict2': pipeline1_verdict2.group(2) if pipeline1_verdict2 else "",
        'pipeline2_verdict': pipeline2_verdict.group(2) if pipeline2_verdict else "",
        'cross_debate': cross_debate,
        'verdict_table': verdict_table,
        'corrections': corrections,
        'evidence_matrix': evidence_matrix,
        'references': references
    }


def generate_simplified_version(full_md, output_path):
    """生成精简版"""
    conclusions = extract_final_conclusions(full_md)
    
    # 从完整版中提取关键发现（R7/R11/R13/R21/R39 等）
    key_findings = []
    
    # R7：体外 84% ≠ 体内 0.015%
    r7 = re.search(r'\*\*R7 是本 6 轮最重要的发现\*\*：(.+?)(?=\n\n|\n###)', full_md, re.DOTALL)
    if r7:
        key_findings.append(('R7：体外 84% ≠ 体内 0.015%', r7.group(1)))
    
    # R11：超选给药的关键修正
    r11 = re.search(r'\*\*R11 的关键修正\*\*：(.+?)(?=\n\n|\n###)', full_md, re.DOTALL)
    if r11:
        key_findings.append(('R11：超选给药的关键修正', r11.group(1)))
    
    # R13：超选 IA 的诚实结论
    r13 = re.search(r'\*\*R13 的诚实结论\*\*：(.+?)(?=\n\n|\n###)', full_md, re.DOTALL)
    if r13:
        key_findings.append(('R13：超选 IA 的诚实结论', r13.group(1)))
    
    # R21：时间窗效应
    r21 = re.search(r'\*\*R21 是穷尽文献后浮现的最重要争点\*\*：(.+?)(?=\n\n|\n###)', full_md, re.DOTALL)
    if r21:
        key_findings.append(('R21：时间窗效应', r21.group(1)))
    
    # R39：最终资源分配
    r39 = re.search(r'\*\*R39 的最终资源分配\*\*：(.+?)(?=\n\n|\n###)', full_md, re.DOTALL)
    if r39:
        key_findings.append(('R39：最终资源分配', r39.group(1)))
    
    # 生成精简版
    simplified_md = f"""# 761TEL 两条 NSC 管线临床疗效可达性 · 对抗式循证辩论报告（精简版）

> 编制日期：2026-08-30 | 版本：精简版（最终结论版）
> 方法学：fable5-workflow_diy v2.0 A线｜40 轮迭代式攻防｜GRADE 证据分级｜三层证据跨层一致性检验
> 疗效判据：**注册终点可达成**（统计学显著 + ≥MCID）
> 证据获取：Europe PMC 全文 XML / ClinicalTrials.gov 注册库 / OpenAlex 引用链（全部为可通读全文或注册库原始数据）
> 说明：本版仅保留 40 轮攻防后的**最终结论与核心证据**，中间轮的过程性判决已省略。完整演化版见同目录《761TEL_双管线疗效可达性_对抗式循证辩论报告.md》。

---

## 执行摘要
{conclusions['exec_summary']}

---

## 0. 方法学声明
{conclusions['methodology']}

---

## 1. 管线一：超选 IA hNSC × 亚急性缺血性卒中

### 1.0 【一号争点】细胞替代与旁分泌的两难：安全剂量远低于有效剂量

#### 收敛判决
{conclusions['pipeline1_verdict']}

### 1.1 【二号争点】注册终点可达性：荟萃层面证据的稳健性

#### 收敛判决
{conclusions['pipeline1_verdict2']}

### 1.2 第 5–40 轮攻防：关键发现与最终调整

"""
    
    # 添加关键发现
    for title, content in key_findings:
        simplified_md += f"""#### {title}

{content}

"""
    
    simplified_md += f"""---

## 2. 管线二：脑内立体定向 hNSC × 慢性缺血性卒中

### 2.0 【一号争点】安慰效应边界

#### 收敛判决
{conclusions['pipeline2_verdict']}

### 2.1 其余争点

| 序 | 维度 | 正方 | 反方 | 判决 |
|---|---|---|---|---|
| 2 | 概念验证质量 | NR1 +12.1[未定位到可通读全文]、hNPC01 +16[未定位到可通读全文] | PISCES-2 主要终点 1/23；NR1/hNPC01 原始出处尚未定位到可通读全文 | 中性偏负 |
| 3 | 人群匹配 | 慢性期需细胞替代 | **基线完全瘫痪者应答为零**[8]，最需治疗者恰无效 | **负** |
| 4 | 对照强度 | NSI-566 剂量爬坡至 7.2×10⁷ 无 DLT | 除 ACTIsSIMA 外全部开放标签 | 中性 |
| 5 | 细胞命运 | 直接植入 >90% 到位 | 移植后长期存活率与功能性突触整合**无人类直接证据** | 负 |
| 6 | 微环境 | 慢性期结构稳定，利于精准植入 | 胶质瘢痕 CSPG/Nogo 抑制轴突生长 | 中性 |

### 2.2 第 8–40 轮攻防：关键发现与最终调整

"""
    
    # 添加管线二的关键发现
    simplified_md += f"""#### R8：两项研究数据不相容的根源

两项研究数据不相容，反方归因于 (a) 极端值驱动与 (b) 基线/盲法差异，正方归因于 (c) 细胞类型差异（SB623 是 MSC 类而非 NSC）与 (d) 终点定义不同。再质疑判定：**(c) 不成立**——若 NSC 确优于 MSC，则应在 NSC 自己的对照试验（PISCES 系列）中看到阳性，但 PISCES-2 主要终点同样未达成。因此不相容的根源是 (a)+(d)：**+16 分大概率由少数极端值驱动（N=9），且"平均变化"这一指标本身对偏态分布具有误导性。**

#### R9：GRADE 升级因素全部不成立

GRADE 三个升级因素逐一检验后全部不成立——大效应量（+16 分因 N=9 置信区间极宽，不成立）、剂量-反应（人体层面无检验，ACTIsSIMA 两剂量差异未显著）、残余混杂有利（开放标签引入的混杂方向不利）。**管线二证据确定性维持中低，无法上调。**

#### R21：时间窗效应——慢性期优于亚急性期

MSC 荟萃（PMC11386217，全文级）显示，**慢性期（>3 个月）给药的 mRS MD -0.60、NIHSS MD -3.20，均 P < 0.001**，且改善幅度大于亚急性期（2 周至 3 个月）。这与管线二"慢性期"的定位一致，是其可达概率上调至 25–35% 的核心依据。

#### R31–R32：影像学分层的关键盲区与指标选择

- **年龄分层**：PISCES-2 显示 6 个月应答者显著更年轻（53±6 岁 vs 64±11 岁，p=0.025）[8]，且既往 DTI 研究很少纳入年龄因素[26]。761TEL 的 IIT 应设置年龄分层（如 <65 岁 vs ≥65 岁），并采用 **edema-corrected CST integrity** 校正技术[27]。
- **指标选择**：**中脑脚 FA 值比纤维数更能预测手功能**[28]，应作为主要分层指标；纤维数可作为快速筛查（排除完全瘫痪者）。

#### R34–R35：慢性期自然恢复的量化上限与效应量异常

慢性期自然恢复的上限是**功能代偿（FMA +7.95）**[16]，且 3200–9600 次重复训练 8 周仍**无结构可塑性**[29]。NSI-566 的 +16 分是运动训练的 2 倍、假刺激的 8 倍——这个异常大的效应量**强化而非削弱了对"极端值驱动"的怀疑**（R8 判决）。

#### R39：最终资源分配

从"管线一 80%"调整为"**管线一 30% + 管线二 40% + 管线三 30%**"——管线二作为近期价值锚点（安全性已确立、时间窗效应有利）。

---

## 3. 交叉辩论：机制主张 × 给药途径 × 时间窗的自洽性
{conclusions['cross_debate']}

---

## 4. 双线判决总表（最终版）
{conclusions['verdict_table']}

---

## 5. 既有报告乐观偏差修正清单
{conclusions['corrections']}

---

## 6. 三层证据矩阵
{conclusions['evidence_matrix']}

---

## 参考文献（正文引用 31 条）
{conclusions['references']}

---

## 补充参考文献（全文级，90 篇）

> 以下文献均为 Europe PMC 全文级（可通读全文），按主题分组排列。其中已在正文引用的文献保留原有编号与标注，其余按主题归类列出。

### A. 管线一：IA 给药 NSC 卒中（9 篇）

[A3] Comparative study of the efficacy of intra-arterial and intravenous stem cell transplantation in experimental stroke. PeerJ. 2023. PMC10640846. `[全文]`——IA 与 IV 给药途径的头对头比较

[A4] Stem Cell- and Cell-Based Therapies for Ischemic Stroke. Bioengineering (Basel). 2022. PMC9687728. `[全文]`——细胞治疗缺血性卒中综述

[A5] Transplantation of Human Umbilical Cord Mesenchymal Stem Cells for Ischemic Stroke. Biomolecules. 2022. PMC8945978. `[全文]`——脐带 MSC 卒中移植

[A6] Therapeutic Effects of hiPSC-Derived Glial and Neuronal Progenitor Cells in Stroke. Int J Mol Sci. 2021. PMC8125106. `[全文]`——hiPSC 来源胶质与神经前体细胞

[A7] Intra-Arterial Stem Cell Transplantation in Experimental Stroke. Front Neurosci. 2021. PMC7960930. `[全文]`——IA 干细胞移植实验卒中

[A8] Neurogenin-1 Overexpression Increases the Therapeutic Effects of Neural Stem Cells in Stroke. Int J Stem Cells. 2020. PMC7119213. `[全文]`——Neurogenin-1 过表达增强 NSC 疗效

[A9] Epidermal neural crest stem cell transplantation as a promising therapy for stroke. CNS Neurosci Ther. 2020. PMC7298983. `[全文]`——表皮神经嵴干细胞移植

[A10] Stem cell-like dog placenta cells afford neuroprotection against ischemic stroke. PLoS One. 2013. PMC3783428. `[全文]`——犬胎盘细胞神经保护

[A11] Molecular Encoding of Ischemic Stroke and its Resolution after Stem Cell Therapy. MedComm. 2025. PMC12559856. `[全文]`——缺血性卒中的分子编码与干细胞治疗后的消退

### B. 管线二：脑内移植慢性卒中（5 篇）

[B3] Implantation of the clinical-grade human neural stem cell line for chronic stroke. Stem Cells. 2020. PMC7496241. `[全文]`——临床级人 NSC 系慢性卒中植入

[B4] c-MycERTAM transgene silencing in a genetically modified human neural stem cell line. BMC Neurosci. 2009. PMC2725042. `[全文]`——c-MycERTAM 转基因沉默

### C. DTI/影像学分层（22 篇）

[C4] Objective motor function assessment using diffusion tensor tractography in stroke. Medicine (Baltimore). 2025. PMC12746945. `[全文]`——DTT 客观运动功能评估

[C5] Toward Precision Post-Stroke Rehabilitation Medicine: Integrating Neuroimaging. J Clin Med. 2025. PMC12653625. `[全文]`——精准卒中后康复医学

[C6] Human corticospinal tract lateralization at the height of the hand knob. Sci Rep. 2025. PMC12460680. `[全文]`——人 CST 侧化

[C7] Integrated neuroimaging and robotic rehabilitation in chronic stroke. Exp Ther Med. 2025. PMC12329399. `[全文]`——神经影像与机器人康复整合

[C8] Prediction of Motor Recovery after Subacute Cerebral Infarction. Neurorehabil Neural Repair. 2025. PMC12405655. `[全文]`——亚急性脑梗死运动恢复预测

[C9] Infratentorial white matter integrity as a potential biomarker for stroke recovery. Brain Commun. 2025. PMC12079383. `[全文]`——幕下白质完整性作为卒中恢复生物标志物

[C10] Assessment of corticospinal tract damage and cytokines response in stroke. Front Immunol. 2024. PMC11638050. `[全文]`——CST 损伤与细胞因子反应

[C11] Usefulness of automated tractography for outcome prediction in stroke. J Phys Ther Sci. 2024. PMC11441893. `[全文]`——自动纤维追踪预后预测

[C12] Outcome Prediction by Combining Corticospinal Tract Lesion Load. Prog Rehabil Med. 2024. PMC10782178. `[全文]`——CST 病灶负荷联合预后预测

[C13] Preservation of Cerebellar Afferent Pathway May Be Related to Motor Recovery. Life (Basel). 2022. PMC9318318. `[全文]`——小脑传入通路保留与运动恢复

[C14] Performance Comparison of Different Neuroimaging Methods for Predicting Motor Outcome. Neural Plast. 2022. PMC9192322. `[全文]`——不同神经影像方法预测运动结局比较

[C15] Dynamic Relationship Between Interhemispheric Functional Connectivity and Motor Recovery. Front Aging Neurosci. 2022. PMC9120434. `[全文]`——半球间功能连接动态关系

[C16] The Severity of Sensorimotor Tracts Degeneration May Predict Motor Outcome. Front Neurol. 2022. PMC9008887. `[全文]`——感觉运动束变性严重程度预测运动结局

[C17] Relationship between the Corticospinal and Corticocerebellar Tracts. J Pers Med. 2021. PMC8620974. `[全文]`——CST 与皮质小脑束关系

[C18] Prediction of Motor Recovery after Stroke by Assessment of Corticospinal Tract. Indian J Radiol Imaging. 2021. PMC8299489. `[全文]`——CST 评估预测运动恢复

[C19] Does Motor Tract Integrity at 1 Month Predict Gait and Balance at 6 Months? Brain Sci. 2021. PMC8301763. `[全文]`——1 个月运动束完整性预测 6 个月步态与平衡

[C20] Brain Connectivity Affecting Gait Function After Unilateral Stroke. Brain Sci. 2021. PMC8301903. `[全文]`——脑连接影响单侧卒中步态

[C21] White matter integrity of contralesional and transcallosal tracts in chronic stroke. Neuroimage Clin. 2021. PMC8209270. `[全文]`——对侧与经胼胝体束白质完整性

[C22] An overview of fractional anisotropy as a reliable quantitative measure for stroke. J Phys Ther Sci. 2021. PMC7829559. `[全文]`——FA 作为卒中可靠定量指标综述

[C23] Diffusion Tensor Imaging Biomarkers to Predict Motor Outcomes. Front Neurol. 2019. PMC6530391. `[全文]`——DTI 生物标志物预测运动结局

### D. 归巢/迁移（4 篇）

[D1] Transplanted hair follicle stem cells migrate to the penumbra of ischemic stroke. Stem Cell Res Ther. 2020. PMC7510278. `[全文]`——毛囊干细胞迁移至缺血边缘带

[D2] Neurogenin-1 Overexpression Increases the Therapeutic Effects of Neural Stem Cells in Stroke. Int J Stem Cells. 2020. PMC7119213. `[全文]`——同 [A8]

[D3] Identification of pro-angiogenic markers in blood vessels from stroke patients. BMC Genomics. 2009. PMC2664824. `[全文]`——卒中患者血管促血管生成标志物

[D4] Advancements in the treatment of cerebral ischemia-reperfusion injury. Medicine (Baltimore). 2025. PMC11730110. `[全文]`——脑缺血再灌注损伤治疗进展

### E. 突触整合/环路重建（3 篇）

[E3] Human stem cell-derived neurons establish functional inhibitory synapses. Sci Rep. 2026. PMC13076780. `[全文]`——人干细胞来源神经元建立功能性抑制性突触

[E4] Transplanted deep-layer cortical neuroblasts integrate into host neural circuits. Stem Cell Res Ther. 2024. PMC11558921. `[全文]`——深层皮质神经母细胞整合入宿主环路

### F. 外泌体（27 篇）

[F3] Mesenchymal stromal/stem cell-derived extracellular vesicles in brain disorders. Front Cell Neurosci. 2026. PMC13193808. `[全文]`——MSC 来源 EV 在脑疾病中的应用

[F4] Extracellular vesicles derived from astrocytes pretreated with neuroprotective compounds. J Transl Med. 2026. PMC12983613. `[全文]`——星形胶质细胞来源 EV

[F5] Healthy young human plasma-derived exosomes enhance neural stem cell function. J Nanobiotechnology. 2026. PMC12879336. `[全文]`——健康年轻人血浆外泌体增强 NSC 功能

[F6] Exosomes in stroke management: A promising paradigm shift in stroke treatment. Neural Regen Res. 2026. PMC12094539. `[全文]`——外泌体卒中管理的范式转变

[F7] Human Stem Cell-Derived Extracellular Vesicles: A Pioneering Paradigm in Ischemic Stroke. Int J Mol Sci. 2025. PMC12607505. `[全文]`——同 [31]

[F8] Mesenchymal stem cells and exosomes in ischemic brain injury. Front Genet. 2025. PMC12425733. `[全文]`——同 [30]

[F9] Extracellular vesicles enriched with miR-486 from Tetramethylpyrazine-treated MSCs. Stem Cell Res Ther. 2025. PMC12382071. `[全文]`——川芎嗪处理 MSC 来源富集 miR-486 的 EV

[F10] Human Neural Progenitor Cell-Derived Exosomes Deliver miR-100-5p Targeting HDAC6. Mol Neurobiol. 2025. PMC12367819. `[全文]`——人 NPC 外泌体递送 miR-100-5p

[F11] Effects of stem cell therapy on preclinical stroke. Open Vet J. 2025. PMC11974274. `[全文]`——干细胞治疗临床前卒中

[F12] Human neural stem cell-derived exosomes activate PINK1/Parkin pathway. J Transl Med. 2025. PMC11971779. `[全文]`——人 NSC 外泌体激活 PINK1/Parkin 通路

[F13] Therapeutic Potential of Injectable Supramolecular Hydrogels with Exosomes. Int J Nanomedicine. 2025. PMC11853779. `[全文]`——可注射超分子水凝胶与外泌体

[F14] miRNA in blood-brain barrier repair: role of extracellular vesicles. Front Cell Neurosci. 2025. PMC11842324. `[全文]`——miRNA 在 BBB 修复中的作用

[F15] Role of STAT3-FOXO3 Signaling in the Modulation of Neuroplasticity by Exosomes. Adv Sci. 2024. PMC11423231. `[全文]`——STAT3-FOXO3 信号调控外泌体神经可塑性

[F16] Exosomes as a therapeutic tool to promote neurorestoration after stroke. CNS Neurosci Ther. 2024. PMC11110007. `[全文]`——外泌体促进卒中后神经修复

[F17] Emerging strategies for nerve repair and regeneration in ischemic stroke. Neural Regen Res. 2024. PMC11090435. `[全文]`——缺血性卒中神经修复新策略

[F18] Bibliometric Analysis of Stem Cells in Ischemic Stroke (2001–2023). Int J Med Sci. 2024. PMC10750336. `[全文]`——干细胞缺血性卒中文献计量分析

[F19] NSC-derived exosomes enhance therapeutic effects of NSC transplantation in stroke. eLife. 2023. PMC10139690. `[全文]`——NSC 外泌体增强 NSC 移植疗效

[F20] The Neuroprotective Effects of Exosomes Derived from TSG101-Modified MSCs. Int J Mol Sci. 2022. PMC9455780. `[全文]`——TSG101 修饰 MSC 外泌体神经保护

[F21] Targeted delivery of neural progenitor cell-derived extracellular vesicles for stroke. Theranostics. 2021. PMC8120222. `[全文]`——NPC 外泌体靶向递送

[F22] Potential effects of mesenchymal stem cell derived extracellular vesicles in stroke. Neural Regen Res. 2021. PMC8374551. `[全文]`——MSC 外泌体卒中潜在效应

[F23] Biosensing surfaces and therapeutic biomaterials for the central nervous system. Emergent Mater. 2021. PMC7944718. `[全文]`——CNS 生物传感表面与治疗性生物材料

[F24] The use of hydrogel-delivered extracellular vesicles in recovery after stroke. Neural Regen Res. 2021. PMC8067932. `[全文]`——水凝胶递送 EV 用于卒中后恢复

[F25] Neural Stem Cell Extracellular Vesicles Disrupt Midline Shift in Stroke. Transl Stroke Res. 2020. PMC7340639. `[全文]`——NSC 外泌体阻断卒中线移位

[F26] Exosomes from human urine-derived stem cells enhanced neurogenesis after stroke. J Cell Mol Med. 2020. PMC6933407. `[全文]`——人尿源干细胞外泌体增强神经发生

[F27] Intranasally Administered Human MSC-Derived Extracellular Vesicles in Stroke. Int J Mol Sci. 2019. PMC6981466. `[全文]`——经鼻给予人 MSC 外泌体

[F28] Multicellular Crosstalk Between Exosomes and the Neurovascular Unit in Stroke. Front Neurosci. 2018. PMC6232510. `[全文]`——外泌体与神经血管单元的多细胞串扰

### G. 系统综述/荟萃（23 篇）

[G3] Efficacy and safety of mesenchymal stem cells for cerebral infarction: a systematic review. Biomed Rep. 2026. PMC12884146. `[全文]`——MSC 脑梗死疗效与安全性；3-6 月随访 NIHSS WMD -2.40

[G4] Cardiomyocyte regeneration therapy and its effect on LVEF and clinical outcomes. Stem Cell Res Ther. 2025. PMC12403498. `[全文]`——心肌细胞再生治疗

[G5] Current Advancement and Patient Outcomes in Reperfusion Brain Injury. Brain Behav. 2025. PMC12321978. `[全文]`——再灌注脑损伤进展

[G6] The efficacy and safety of stem cell therapy for ischemic stroke: a systematic review. BMC Neurol. 2025. PMC12125799. `[全文]`——蛛网膜下腔+静脉联合优于单一途径

[G7] Safety and Efficacy of Stem Cell Therapy in Ischemic Stroke: A Systematic Review. J Clin Med. 2025. PMC11943215. `[全文]`——卒中干细胞荟萃；NIHSS/mRS/BI/FMA 多终点

[G8] Safety and Efficacy of Transendocardial Stem Cells Therapy in Ischemic Heart Disease. Curr Cardiol Rev. 2025. PMC12172215. `[全文]`——经心内膜干细胞治疗

[G9] Stem cell therapy for non-ischemic dilated cardiomyopathy: a systematic review. Syst Rev. 2024. PMC11546504. `[全文]`——非缺血性扩张型心肌病

[G10] Stem cell-derived exosomes for ischemic stroke: a conventional and network meta-analysis. Front Pharmacol. 2024. PMC11537945. `[全文]`——干细胞外泌体缺血性卒中荟萃

[G11] Mesenchymal stem cells therapy for chronic ischemic stroke-a systematic review. Asian Biomed. 2024. PMC11524678. `[全文]`——MSC 慢性缺血性卒中系统综述

[G12] Efficacy and safety of mesenchymal stem cells in patients with ischemic stroke. BMC Neurol. 2024. PMC10823675. `[全文]`——MSC 患者缺血性卒中

[G13] Efficacy and safety of intravenous mesenchymal stem cells for ischemic stroke. Front Stroke. 2023. PMC12802624. `[全文]`——静脉 MSC 缺血性卒中

[G14] Allogeneic Cell Therapy Applications in Neonates: A Systematic Review. Stem Cells Transl Med. 2023. PMC10552935. `[全文]`——新生儿异体细胞治疗

[G15] Comparison of the Administration Route of Stem Cell Therapy in Ischemic Stroke. J Clin Med. 2023. PMC10094955. `[全文]`——给药途径比较

[G16] The Efficacy and Safety of Ischemic Stroke Therapies: An Umbrella Review. Front Pharmacol. 2022. PMC9355553. `[全文]`——缺血性卒中治疗伞状综述

[G17] Safety and Clinical Efficacy of Mesenchymal Stem Cell Treatment in Ischemic Stroke. Front Neurol. 2022. PMC9196044. `[全文]`——MSC 治疗缺血性卒中安全性与疗效

[G18] Clinical outcome and safety of stem cell therapy for ischemic stroke. Surg Neurol Int. 2022. PMC9168316. `[全文]`——干细胞治疗缺血性卒中临床结局与安全性

[G19] Stem Cell Therapy in Ischemic Stroke: A Systematic Review and Meta-analysis. Ann Indian Acad Neurol. 2021. PMC8232485. `[全文]`——干细胞治疗缺血性卒中系统综述；**48 例患者，卒中后 8–15 天，IA 输注在 12 个月后未改善结局**

[G20] Stem Cell Therapies for Ischemic Stroke: A Systematic Review. Cureus. 2021. PMC7936858. `[全文]`——干细胞治疗缺血性卒中系统综述

[G21] Stem cell-based therapies for ischemic stroke: a systematic review and meta-analysis. Stem Cell Res Ther. 2020. PMC7318436. `[全文]`——干细胞治疗缺血性卒中系统综述

[G22] Safety and Efficacy of Adult Stem Cell Therapy for Acute Myocardial Infarction. Stem Cells Transl Med. 2018. PMC6265630. `[全文]`——成人干细胞治疗急性心肌梗死

[G23] Association Between Clonal Hematopoiesis and Cardiometabolic Disease. JACC CardioOncol. 2026. PMC13282834. `[全文]`——克隆性造血与心血管代谢疾病

---

## 流水线记录

> 工作流：fable5-workflow_diy v2.0 | 线路：A线（深度调研 + 复杂推理辩论） | 日期：2026-08-30
> 前置阶段：澄清 2 轮 / 技能就绪 7 个 / 提示词 v3 确认
> 已执行：ms-search-lit 检索 → Europe PMC JATS 全文获取与解析 → ClinicalTrials.gov 注册库取数 → OpenAlex 引用链 → **40 轮迭代式攻防** → GRADE 分级 → 三层证据跨层一致性检验
> 证据获取：**180 条候选**（90 篇全文级已下载 106 篇 XML、解析 108 篇 + 87 篇摘要级 + 2 项注册库 + 1 篇排除）
> 参考文献：**正文引用 31 条 + 补充参考文献 90 条（全文级），合计 121 条**
> 全文与解析文本存放：`subproj-疗效预测/01_全文_JATS/`、`02_解析文本/`；证据索引：`04_证据矩阵/证据索引_v1.md`；第 5–10 轮：`05_辩论轮次/R5-R10_攻防.md`；第 11–20 轮：`05_辩论轮次/R11-R20_攻防.md`；第 21–30 轮：`05_辩论轮次/R21-R30_攻防.md`；第 31–40 轮：`05_辩论轮次/R31-R40_攻防.md`

### 版本说明

本精简版仅保留 40 轮攻防后的**最终结论与核心证据**，中间轮的过程性判决已省略。完整演化版（含全部 40 轮攻防过程）见同目录《761TEL_双管线疗效可达性_对抗式循证辩论报告.md》。
"""
    
    # 保存精简版
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(simplified_md)
    
    print(f'精简版已生成: {output_path}')
    return output_path


def convert_to_docx(md_path, docx_path):
    """转换 MD 为 DOCX"""
    cmd = f'"{PY}" -c "import sys; sys.path.insert(0, r\'{MD2DOCX}\'); from md2docx_diy import md_to_docx; md_to_docx(r\'{md_path}\', r\'{docx_path}\', orientation=\'portrait\')"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    return docx_path


def main():
    parser = argparse.ArgumentParser(description='Evidence Debate — 多版本交付生成')
    parser.add_argument('--full', required=True, help='完整版报告 MD 文件')
    parser.add_argument('--output', required=True, help='输出目录')
    args = parser.parse_args()
    
    # 读取完整版
    with open(args.full, encoding='utf-8') as f:
        full_md = f.read()
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成精简版
    full_name = Path(args.full).stem
    simplified_md_path = output_dir / f'{full_name.replace("_完整版", "")}_精简版.md'
    generate_simplified_version(full_md, simplified_md_path)
    
    # 转换为 DOCX
    simplified_docx_path = simplified_md_path.with_suffix('.docx')
    convert_to_docx(simplified_md_path, simplified_docx_path)
    
    print(f'\n=== 完成 ===')
    print(f'精简版 MD: {simplified_md_path}')
    print(f'精简版 DOCX: {simplified_docx_path}')


if __name__ == '__main__':
    main()
