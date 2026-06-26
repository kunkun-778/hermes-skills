---
name: skill-linter
description: "扫描 ~/.openclaw/workspace/skills、~/.npm-global/lib/node_modules/openclaw/skills 和 ~/.hermes/skills 下所有 SKILL.md，验证 frontmatter 字段是否齐全、格式是否规范，并生成 HTML 报告。"
version: 1.0.0
author: 小雨
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skill, lint, validation, maintenance]
    homepage: ""
    related_skills: []
---
# Skill Linter

扫描 **三个技能目录**，验证 frontmatter 字段是否齐全、格式是否规范，并生成 HTML 报告：

1. **OpenClaw 工作区技能**：`~/.openclaw/workspace/skills/`
2. **全局技能（npm）**：`~/.npm-global/lib/node_modules/openclaw/skills/`
3. **Hermes 技能**：`~/.hermes/skills/`

## 功能

- **三目录扫描**：递归遍历上述三个目录。
- **提取 frontmatter**：解析 YAML frontmatter（`---` 包裹部分）。
- **必填字段校验**：检查 `name`, `description`, `author`, `version`, `license`, `platforms` 是否存在。
- **YAML 格式校验**：检查缩进是否为 2 空格、字符串是否使用双引号。
- **生成 HTML 报告**：按目录分组展示结果，支持复制修复命令。

## 使用方法

```bash
# 直接运行
python -m ~/.hermes/skills/skill-linter/linter.py
```

运行后会在 `~/.hermes/cron/output/skill-lint-report-YYYYMMDD-HHmm.html` 生成报告。

## 📁 支持的配置

可选的 `lint-config.yaml` 文件可以放在：

```
~/.hermes/skills/skill-linter/lint-config.yaml
```

或作为模板复制：

```bash
cp ~/.hermes/skills/skill-linter/templates/lint-config.yaml ~/.hermes/skills/skill-linter/lint-config.yaml
```

运行 `linter.py` 时会读取此配置以覆盖默认行为（若存在）。

## 报告示例

### ✅ 通过的 Skill（按目录分组）

#### ~/.openclaw/workspace/skills/

| Skill 名称 | 状态 | 耗时 |
|------------|------|------|
| xiaoyu | ✅ | 0.02s |

#### ~/.npm-global/lib/node_modules/openclaw/skills/

| Skill 名称 | 状态 | 耗时 |
|------------|------|------|
| qq-bot | ✅ | 0.01s |

#### ~/.hermes/skills/

| Skill 名称 | 状态 | 耗时 |
|------------|------|------|
| hermes-agent | ✅ | 0.03s |

### ❌ 失败的 Skill（按目录分组）

| Skill 名称 | 目录 | 错误 |
|------------|------|------|
| missing-name | ~/.openclaw/workspace/skills/missing | 缺少必填字段: name |

## 技术细节

- 使用 `pathlib.Path` 扫描文件（支持 `~` 展开）
- 使用 `PyYAML` 解析 frontmatter
- 使用 `jinja2` 生成 HTML 报告
- 支持跨平台（Windows 使用 `%APPDATA%` / `%LOCALAPPDATA%`）

## 待办

- [ ] 自动修复缺失的 frontmatter 字段
- [ ] 集成到 `/reload-skills` 命令中，实时 lint
- [ ] 支持自定义规则（通过 `lint-config.yaml`）
