# 校验与实测体系

本仓库明确区分技能研发检查与小说改编项目检查。二者入口、对象、时机和报告均不同。

## A. 技能侧开发检查（仅技能维护者）

用于开发、修改、发布技能时检查仓库自身：Agent Skills 入口文件、Frontmatter、仓库引用路径、开发目录、工具脚本和测试。执行：

```bash
python tools/validate_skill.py
python -m unittest discover -s tests
```

它不属于小说改编项目流程，不得在日常原著分析、分集创作或剧本审查时调用。

## B. 改编项目侧工作检查（实际改编时）

只检查当前小说改编项目的项目配置和创作产物：配置字段、YAML 可解析性、必要内容标记、稳定 ID 格式和明显重复定义。执行：

```bash
pip install -r requirements.txt
python tools/validate_project.py path/to/adaptation-project
```

它不检查 SKILL.md、Frontmatter、references、templates 或技能仓库结构。

## C. 改编质量审查

由改编流程中的审查阶段执行，检查原著因果、人物动机、改编追溯、剧集推进、连续性、场景戏剧性和可拍性。脚本只能辅助定位，不能替代语义判断。

## 结构化数据与 Markdown 的权威关系

- YAML/JSON 保存适合机器校验和跨文件引用的字段；Markdown 保存解释性分析、创作论证、人物弧光、事件过程、场景和剧本正文。
- 同一字段只设一个权威来源，禁止要求用户重复维护两份同义数据。
- 项目配置 YAML 是项目参数的权威来源；叙述内容以对应 Markdown 文档为权威来源。
- Schema 是字段契约，不意味着每个项目都必须额外维护一份重复 JSON。机器索引优先从 Markdown 的稳定 ID 和明确元数据提取。
