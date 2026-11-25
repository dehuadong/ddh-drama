#!/usr/bin/env python3
"""项目侧检查：只检查小说改编项目产物，不检查技能仓库。"""
import argparse, re, sys
from pathlib import Path

ID_PATTERNS = {
 "C": re.compile(r"^C\d{3,}$"), "E": re.compile(r"^E\d{3,}$"),
 "F": re.compile(r"^F\d{3,}$"), "D": re.compile(r"^D\d{3,}$"),
 "R": re.compile(r"^R\d{3,}$"), "S": re.compile(r"^S\d{2}-\d{3}$"),
}
ID_RE = re.compile(r"\b(?:C\d{3,}|E\d{3,}|F\d{3,}|D\d{3,}|R\d{3,}|S\d{2}-\d{3})\b")
ID_DEF_RE = re.compile(r"(?m)^\s*(?:#{1,6}\s*)?((?:C|E|F|D|R)\d{3,}|S\d{2}-\d{3})(?:\s*[·|：:]|\s*$)")
REQUIRED = {
 "source-analysis":["覆盖范围","关键事件","核心人物","伏笔"],
 "adaptation-proposal":["改编定位","改编决策","新增剧情"],
 "story-outline":["主线因果链","人物弧光","高潮与结局"],
 "series-outline":["阶段划分","分集大纲","连续性检查"],
 "episode-outline":["本集目标","主要事件","结尾钩子","原著依据"],
 "scene-outline":["场景ID","场景目标","冲突/阻力","状态变化"],
 "review-report":["审查范围","问题清单","优先修改顺序"]
}

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument("project_dir",nargs="?",default=".")
 root=Path(parser.parse_args().project_dir)
 if not root.is_dir(): print(f"项目目录不存在：{root}"); return 2
 errors=[]
 config=root/"project-config.yaml"
 if config.exists():
  try:
   import yaml
   data=yaml.safe_load(config.read_text(encoding="utf-8"))
   if not isinstance(data,dict): errors.append("project-config.yaml 顶层必须是对象")
   else:
    for key in ("project","source","adaptation","series","workflow","approval"):
     if key not in data: errors.append(f"project-config.yaml 缺少字段：{key}")
    stages=data.get("workflow",{}).get("stages",{})
    for stage in ("source_analysis","adaptation_design","story_reconstruction","series_planning","screenplay_drafting","script_review"):
     if stage not in stages: errors.append(f"project-config.yaml 缺少阶段状态：{stage}")
    schema_path=Path(__file__).resolve().parents[1]/"schemas"/"project.schema.json"
    if schema_path.exists():
     try:
      import json, jsonschema
      jsonschema.validate(data,json.loads(schema_path.read_text(encoding="utf-8")))
     except ImportError: errors.append("未安装 jsonschema，跳过 Schema 校验；请安装 requirements.txt")
     except Exception as exc: errors.append(f"项目配置 Schema 校验失败：{exc}")
  except ImportError: errors.append("缺少 PyYAML，请先安装 requirements.txt")
  except Exception as exc: errors.append(f"YAML 解析失败：{exc}")
 definitions={}
 for path in root.rglob("*.md"):
  if any(part.startswith(".") for part in path.relative_to(root).parts): continue
  text=path.read_text(encoding="utf-8")
  for stem,headings in REQUIRED.items():
   if stem in path.stem:
    for heading in headings:
     if heading not in text: errors.append(f"{path}: 缺少必要章节/字段「{heading}」")
  for token in ID_DEF_RE.findall(text):
   if token in definitions: errors.append(f"{path}: ID {token} 重复定义（首次定义于 {definitions[token]}）")
   else: definitions[token]=path
 if errors:
  print("项目产物基础检查未通过：")
  for error in errors: print("- "+error)
  return 1
 print("项目产物基础检查通过；语义质量仍需独立审查。")
 return 0

if __name__=="__main__": raise SystemExit(main())
