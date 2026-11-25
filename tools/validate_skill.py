#!/usr/bin/env python3
"""技能侧开发检查：只在维护/发布技能仓库时运行。"""
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
skill=ROOT/"SKILL.md"
if not skill.is_file(): errors.append("缺少 SKILL.md")
else:
    text=skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"): errors.append("SKILL.md 缺少 YAML Frontmatter")
    else:
        end=text.find("\n---",4)
        if end<0: errors.append("Frontmatter 未闭合")
        else:
            fm=text[4:end]
            for key in ("name","description"):
                if not re.search(rf"(?m)^{key}:\s*\S",fm): errors.append(f"Frontmatter 缺少有效字段 {key}")
    for rel in re.findall(r"(?:references|templates|schemas|tools|tests|docs)/[A-Za-z0-9_./-]+",text):
        rel=rel.rstrip(".,;:)")
        if not (ROOT/rel).exists(): errors.append(f"引用路径不存在：{rel}")
for folder in ("references","templates","schemas","tools","tests","docs"):
    if not (ROOT/folder).is_dir(): errors.append(f"缺少开发目录：{folder}")
if errors:
    print("技能仓库开发检查未通过：\n"+"\n".join("- "+e for e in errors)); sys.exit(1)
print("技能仓库开发检查通过。此工具仅供技能研发使用。")
