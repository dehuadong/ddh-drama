# Contributing

本文件面向技能仓库的开发者和维护者，不属于小说改编项目工作流。普通使用者执行小说改编时无需阅读或运行本文件中的检查。

## 技能仓库开发检查

在修改或发布技能仓库时运行：

```bash
pip install -r requirements.txt
python tools/validate_skill.py
python -m unittest discover -s tests -v
```

这些检查针对技能仓库自身，包括 Agent Skills 入口文件、Frontmatter、仓库内引用路径、开发目录、开发脚本和单元测试。它们不检查小说改编项目的剧情或剧本质量。

## CI

.github/workflows/skill-ci.yml 在推送到 main 或向 main 提交 Pull Request 时运行技能仓库开发检查。

## 真实改编实测

tests/acceptance-criteria.md 定义技能研发阶段的验收标准。使用独立的原创或授权小说样本，测试技能从原著分析到剧本审查的执行效果。实测记录应保留技能版本、样本范围、任务规格、生成产物、自动检查结果、独立审查意见、缺陷和复测结论。

实测样本不得污染用户真实项目；不得将未经授权的商业小说正文提交到仓库。
