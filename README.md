# Master Learning Skill

![Master Learning 总览](docs/showcase/01-overview.png)

`master-learning` 是一个给 Codex 使用的前置学习 skill。它的目标是让 Codex 在进入实现之前，先像学徒一样学习陌生领域，再像工程师一样做决策。

当任务涉及新框架、新 API、论文复现、GitHub 项目改造、标准规范、本地代码约束或最佳实践时，Codex 很容易凭旧知识直接开写。这个 skill 会先调研官方文档、论文、标准、GitHub repositories、examples、issues、tests 和本地代码，然后产出一份可执行的 `Learning Brief`，再进入计划和实现。

核心理念：大师永远怀着一颗学徒的心。

![Master Learning 流程](docs/showcase/02-workflow.png)

## 它是干嘛的

这个 skill 给 Codex 增加一个“先学习，再实现”的工作流：

- 先明确任务目标、运行环境、未知点、成功标准和风险等级。
- 优先检查本地项目文件、依赖、配置、测试和已有代码风格。
- 调研官方文档、release notes、迁移说明、标准和规范。
- 阅读论文时提取方法、假设、评估方式、代码/数据可用性和工程限制。
- 研究 GitHub 项目时检查 stars 之外的东西：许可证、活跃度、examples、tests、issues、依赖健康度。
- 明确标出证据不足、API 过期、仓库停更、来源冲突和暂定结论。
- 输出一份 `Learning Brief`，作为后续实现计划的依据。

## 什么时候用

适合使用 `$master-learning` 的情况：

- 你要开始一个陌生领域项目。
- 你要选择框架、库、算法、论文方法或架构方案。
- 你要求 Codex 遵循最新文档、最佳实践、标准或 GitHub examples。
- 你要把一个 GitHub 项目改造成自己的项目。
- 任务错误成本较高，不能靠猜。
- 本地项目已有约定，需要先读代码再动手。

不适合的情况：

- 修 typo。
- 明确的小 bug。
- 格式化。
- 用户明确要求不要调研。

## Learning Brief 包含什么

`Learning Brief` 不是泛泛的调研报告，而是给实现阶段使用的工程交付物：

- `Task`：用户目标、目标环境、成功标准、研究深度、信心等级。
- `Sources`：来源表，包含 URL/路径、类型、时间/时效性、可信度和用途。
- `Domain Model`：关键概念、对象、数据、关系和术语。
- `Local Code Lessons`：本地项目结构、约定、配置、测试和约束。
- `GitHub/Code Lessons`：仓库、实现模式、许可证/复用说明、examples、issues。
- `Paper/Standard Lessons`：论文方法、假设、评估设置、标准要求和限制。
- `Implementation Patterns`：推荐架构、API 契约、数据流、测试方式。
- `Risks and Anti-Patterns`：风险、边界情况、反模式、弱假设。
- `Recommendation`：推荐方案、验收标准和下一步。
- `Open Questions`：仍需要用户确认或继续调研的问题。

![Master Learning 训练验证](docs/showcase/03-training.png)

## SkillOpt-style 训练

这个仓库包含一个 Microsoft SkillOpt 启发的本地训练/验证流程。它不是微调模型，而是把 `SKILL.md` 当作可训练的外部状态，通过场景 rollout、失败反思、有界编辑和 held-out validation 来优化 skill 文档。

包含文件：

- `master-learning/references/skillopt-training.md`
- `master-learning/scripts/skillopt_train.py`
- `master-learning/training/benchmark-scenarios.json`
- `master-learning/training/skillopt-run-2026-06-21.md`
- `master-learning/training/skillopt-run-2026-06-21-round2.md`
- `master-learning/training/skillopt-run-2026-06-21-128.md`

场景覆盖：

- 最新框架 / API 使用
- 论文复现
- GitHub 项目改造
- 本地项目优先
- 低风险任务跳过
- 网络降级调研

128 轮稳定性验证结果：`score 1.0`，release gate `PASS`。

![Master Learning 安装分享](docs/showcase/04-install.png)

## 安装

克隆仓库，然后复制 skill 文件夹到 Codex skills 目录：

```powershell
git clone https://github.com/GzmSTAR/master-learning-skill.git
Copy-Item -Recurse -Force .\master-learning-skill\master-learning "$env:USERPROFILE\.codex\skills\master-learning"
```

如果 Codex 没有自动刷新 skill 列表，重启 Codex。

## 使用示例

```text
Use $master-learning to study robot vision SLAM libraries, produce a Learning Brief, then plan the implementation.
```

```text
Use $master-learning before building this paper reproduction project. Check official docs, papers, GitHub repos, and known failure modes.
```

## 目录结构

```text
master-learning/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
  training/
```

脚本全部只使用 Python 标准库：

- `create_learning_brief.py`
- `github_scan.py`
- `paper_scan.py`
- `source_audit.py`
- `merge_learning_brief.py`
- `skillopt_train.py`

## 验证

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "$env:USERPROFILE\.codex\skills\master-learning"
python "$env:USERPROFILE\.codex\skills\master-learning\scripts\skillopt_train.py" --help
```

## License

MIT
