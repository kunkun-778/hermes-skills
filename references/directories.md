# Skill Linter 目录结构说明

## 扫描的三个技能目录

| 目录类型 | 路径 | 说明 |
|---------|------|------|
| OpenClaw 工作区技能 | `~/.openclaw/workspace/skills/` | 用户自定义技能（如 `xiaoyu`） |
| 全局技能（npm） | `~/.npm-global/lib/node_modules/openclaw/skills/` | npm 安装的内置技能 |
| Hermes 技能 | `~/.hermes/skills/` | Hermes 原生技能（如 `hermes-agent`） |

## 目录结构示例

```
~/.openclaw/workspace/skills/
├── xiaoyu/
│   └── SKILL.md          # 开放Claw 工作区技能
└── visual-qa-enhancer/
    └── SKILL.md

~/.npm-global/lib/node_modules/openclaw/skills/
├── discord/
│   └── SKILL.md
├── github/
│   └── SKILL.md
└── ...

~/.hermes/skills/
├── hermes-agent/
│   └── SKILL.md
├── skill-linter/
│   ├── SKILL.md
│   ├── linter.py
│   └── templates/
│       └── lint-config.yaml
└── ...
```

## SKILL.md 期望的目录布局

```
skill-name/
├── SKILL.md              # 主文档（必须）
├── references/           # 可选：会话特定细节（错误记录、API文档等）
├── templates/            # 可选：模板文件（可复制的配置、脚手架等）
└── scripts/              # 可选：可重运行的脚本（验证、探测等）
```

## 验证要点

1. `SKILL.md` 必须有 YAML frontmatter
2. 必填字段：`name`, `description`, `author`, `version`, `license`, `platforms`
3. YAML 格式规范：
   - 缩进：2 空格
   - 字符串引号：推荐双引号
