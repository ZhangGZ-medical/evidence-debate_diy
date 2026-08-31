#!/usr/bin/env python3
"""
Evidence Debate — 证据穷尽与全文获取脚本

用途：阶段 1（证据穷尽）+ 阶段 2（全文获取与证据分级）
输入：维度分解后的检索词列表
输出：去重后的候选清单、全文级/摘要级分级结果、下载的全文 XML、解析后的纯文本

依赖：
- ms-search-lit（PubMed E-utilities）
- ms-fulltext-retrieval（Europe PMC 全文获取、JATS 解析）

使用方法：
    python evidence_exhaust.py --dimensions dimensions.json --output ./output/
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

# 依赖路径
EUTILS = os.path.expanduser("~/.workbuddy/skills/ms-search-lit/references/pubmed_eutils.sh")
PARSER = os.path.expanduser("~/.workbuddy/skills/ms-search-lit/references/parse_pubmed.py")
EPMC_SEARCH = os.path.expanduser("~/.workbuddy/skills/ms-fulltext-retrieval/references/epmc_search.py")
JATS_TO_TEXT = os.path.expanduser("~/.workbuddy/skills/ms-fulltext-retrieval/references/jats_to_text.py")
PY = "C:/Users/G1381/.workbuddy/binaries/python/versions/3.13.12/python.exe"


def search_pubmed(query, retmax=50):
    """用 PubMed E-utilities 检索"""
    cmd = f'bash "{EUTILS}" search "{query}" {retmax}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    ids = result.stdout.strip()
    if not ids:
        return []
    
    # 解析 ID 列表
    cmd = f'echo "{ids}" | "{PY}" -c "import sys,json;print(\',\'.join(json.load(sys.stdin)[\'esearchresult\'][\'idlist\']))"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    id_list = result.stdout.strip().split(',')
    return [id for id in id_list if id]


def fetch_summaries(pmids):
    """用 PubMed E-utilities 获取摘要"""
    if not pmids:
        return []
    
    ids_str = ','.join(pmids)
    cmd = f'bash "{EUTILS}" fetch_json "{ids_str}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # 解析摘要
    cmd = f'echo "{result.stdout}" | "{PY}" "{PARSER}" esummary'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    records = []
    for line in result.stdout.strip().split('\n'):
        parts = line.split('|')
        if len(parts) >= 4:
            records.append({
                'pmid': parts[0],
                'year': parts[1],
                'journal': parts[2],
                'title': parts[3]
            })
    return records


def check_epmc(pmid):
    """检查 Europe PMC 全文可得性"""
    url = f'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:{pmid}&resultType=core&format=json'
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode())
        res = (d.get('resultList') or {}).get('result') or []
        if res:
            r0 = res[0]
            return {
                'pmcid': r0.get('pmcid'),
                'inEPMC': r0.get('inEPMC'),
                'isOpenAccess': r0.get('isOpenAccess'),
                'hasFullText': bool(r0.get('pmcid') and r0.get('inEPMC') == 'Y' and r0.get('isOpenAccess') == 'Y')
            }
    except:
        pass
    return {'pmcid': None, 'inEPMC': None, 'isOpenAccess': None, 'hasFullText': False}


def main():
    parser = argparse.ArgumentParser(description='Evidence Debate — 证据穷尽与全文获取')
    parser.add_argument('--dimensions', required=True, help='维度分解 JSON 文件')
    parser.add_argument('--output', required=True, help='输出目录')
    parser.add_argument('--retmax', type=int, default=50, help='每个维度的最大命中数')
    args = parser.parse_args()
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / '01_全文_JATS').mkdir(exist_ok=True)
    (output_dir / '02_解析文本').mkdir(exist_ok=True)
    (output_dir / '04_证据矩阵').mkdir(exist_ok=True)
    
    # 读取维度分解
    with open(args.dimensions, encoding='utf-8') as f:
        dimensions = json.load(f)
    
    print(f'=== 阶段 1：证据穷尽 ===')
    print(f'维度数: {len(dimensions)}')
    
    # 每个维度独立检索
    all_records = {}
    for dim_name, query in dimensions.items():
        print(f'\n维度: {dim_name}')
        print(f'  检索词: {query}')
        
        pmids = search_pubmed(query, args.retmax)
        print(f'  命中: {len(pmids)} 条')
        
        if not pmids:
            continue
        
        records = fetch_summaries(pmids)
        print(f'  获取摘要: {len(records)} 条')
        
        # 合并去重
        for r in records:
            pmid = r['pmid']
            if pmid not in all_records:
                all_records[pmid] = {**r, 'dimensions': [dim_name]}
            else:
                all_records[pmid]['dimensions'].append(dim_name)
        
        # 保存维度清单
        with open(output_dir / '04_证据矩阵' / f'{dim_name}_list.txt', 'w', encoding='utf-8') as f:
            for r in records:
                f.write(f"{r['pmid']}|{r['year']}|{r['journal']}|{r['title']}\n")
        
        time.sleep(0.5)  # 避免请求过快
    
    print(f'\n=== 合并去重 ===')
    print(f'去重后总数: {len(all_records)}')
    
    # 保存合并清单
    with open(output_dir / '04_证据矩阵' / 'all_records.json', 'w', encoding='utf-8') as f:
        json.dump(list(all_records.values()), f, ensure_ascii=False, indent=1)
    
    # 按维度统计
    print('\n按维度统计:')
    for dim_name in dimensions.keys():
        n = sum(1 for r in all_records.values() if dim_name in r['dimensions'])
        print(f'  {dim_name}: {n}')
    
    print(f'\n=== 阶段 2：全文获取与证据分级 ===')
    
    # 检查全文可得性
    print('检查全文可得性...')
    records = list(all_records.values())
    for i, r in enumerate(records):
        info = check_epmc(r['pmid'])
        r.update(info)
        if (i+1) % 20 == 0:
            print(f'  进度: {i+1}/{len(records)}')
        time.sleep(0.35)
    
    # 分级
    fulltext = [r for r in records if r['hasFullText']]
    abstract_only = [r for r in records if not r['hasFullText']]
    
    print(f'\n分级结果:')
    print(f'  全文级: {len(fulltext)}')
    print(f'  摘要级: {len(abstract_only)}')
    
    # 保存分级结果
    with open(output_dir / '04_证据矩阵' / 'all_records_graded.json', 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=1)
    
    # 批量下载全文
    print(f'\n批量下载全文...')
    pmcids = [r['pmcid'] for r in fulltext if r.get('pmcid')]
    print(f'  待下载: {len(pmcids)} 条')
    
    if pmcids:
        pmcids_str = ' '.join(pmcids)
        cmd = f'"{PY}" "{EPMC_SEARCH}" fetch {pmcids_str} -o "{output_dir}/01_全文_JATS/"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
    
    # 批量解析
    print(f'\n批量解析...')
    xml_files = list((output_dir / '01_全文_JATS').glob('*.xml'))
    print(f'  待解析: {len(xml_files)} 条')
    
    for xml_file in xml_files:
        pmcid = xml_file.stem
        txt_file = output_dir / '02_解析文本' / f'{pmcid}.txt'
        if not txt_file.exists():
            cmd = f'"{PY}" "{JATS_TO_TEXT}" "{xml_file}" > "{txt_file}"'
            subprocess.run(cmd, shell=True)
    
    print(f'\n=== 完成 ===')
    print(f'输出目录: {output_dir}')
    print(f'  01_全文_JATS/: {len(list((output_dir / "01_全文_JATS").glob("*.xml")))} 篇 XML')
    print(f'  02_解析文本/: {len(list((output_dir / "02_解析文本").glob("*.txt")))} 篇 TXT')
    print(f'  04_证据矩阵/: all_records.json, all_records_graded.json')


if __name__ == '__main__':
    main()
