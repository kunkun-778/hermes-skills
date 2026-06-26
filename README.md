# Skill Linter

快速扫描并验证技能文件（SKILL.md）的 frontmatter 是否完整且格式正确。

## 📦 安装

无需安装额外依赖，脚本已包含所有必需库（`pyyaml`, `jinja2`）。

## 🚀 使用

### 基本用法

```bash
# 在终端中直接运行
python -m ~/.hermes/skills/skill-linter/linter.py
```

### 作为 Skill 加载

在 Hermes 对话中：

```
/skill skill-linter
```

然后运行：

```
运行 skill-linter 检查所有技能文件
```

## 📊 输出

运行后会生成 HTML 报告，保存在：

```
~/.hermes/cron/output/skill-lint-report-YYYYMMDD-HHmm.html
```

报告包含：

- ✅ 总计技能数
- ✅ 通过数量
- ❌ 失败/错误数量
- 按目录分组的详细列表
- 错误详情

## 🔧 配置

可选的配置文件 `lint-config.yaml` 放置在：

```
~/.hermes/skills/skill-linter/lint-config.yaml
```

详见 `lint-config.yaml` 文件中的注释。

## 📁 扫描的目录

1. `~/.openclaw/workspace/skills/` - OpenClaw 工作区技能
2. `~/.npm-global/lib/node_modules/openclaw/skills/` - npm 全局技能
3. `~/.hermes/skills/` - Hermes 原生技能

## 🛠️ 支持的验证

- 必填字段检查：`name`, `description`, `author`, `version`, `license`, `platforms`
- YAML 语法验证
- 缩进检查（推荐 2 空格）
- 类型验证

## 📝 待办

- [ ] 自动修复功能
- [ ] 与 Hermes `/reload-skills` 集成
- [ ] 支持自定义规则
- [ ] JSON 输出格式
- [ ] 命令行参数支持

## 🤝 贡献

欢迎提交 PR 或 issue！
