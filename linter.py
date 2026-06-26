#!/usr/bin/env python3
"""
Skill Linter - 扫描三个技能目录并验证 frontmatter
"""
import os
import sys
import yaml
import json
import time
from datetime import datetime
from pathlib import Path
from jinja2 import Template

# 定义扫描目录
SKILL_DIRS = [
    {
        "name": "openclaw-workspace",
        "path": Path("~/.openclaw/workspace/skills").expanduser(),
        "desc": "~/.openclaw/workspace/skills/"
    },
    {
        "name": "openclaw-npm",
        "path": Path("~/.npm-global/lib/node_modules/openclaw/skills").expanduser(),
        "desc": "~/.npm-global/lib/node_modules/openclaw/skills/"
    },
    {
        "name": "hermes",
        "path": Path("~/.hermes/skills").expanduser(),
        "desc": "~/.hermes/skills/"
    }
]

# 必填字段及其类型
REQUIRED_FIELDS = {
    "name": str,
    "description": str,
    "author": str,
    "version": (str, int, float),
    "license": str,
    "platforms": list
}


def extract_frontmatter(content: str) -> tuple:
    """提取 YAML frontmatter"""
    if not content.startswith("---"):
        return None, "No frontmatter found"
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, "Invalid frontmatter format"
    
    try:
        yaml_content = parts[1].strip()
        frontmatter = yaml.safe_load(yaml_content)
        return frontmatter, None
    except yaml.YAMLError as e:
        return None, f"YAML parse error: {e}"


def validate_frontmatter(frontmatter: dict, filepath: Path) -> list:
    """验证 frontmatter 字段"""
    errors = []
    
    if not isinstance(frontmatter, dict):
        return ["Frontmatter is not a valid YAML object"]
    
    # 检查必填字段
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")
        elif not isinstance(frontmatter[field], expected_type):
            errors.append(f"Field '{field}' has wrong type, expected {expected_type}")
    
    # 检查 YAML 格式（缩进、引号）
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查缩进（frontmatter 部分）
        frontmatter_section = content.split("---")[1] if "---" in content else ""
        lines = frontmatter_section.strip().split('\n')
        for i, line in enumerate(lines, 1):
            if line and line[0] == ' ':
                indent = len(line) - len(line.lstrip())
                if indent % 2 != 0:
                    errors.append(f"Line {i}: Odd indentation ({indent} spaces)")
    except Exception:
        pass
    
    return errors


def scan_skill_directory(dir_info: dict) -> list:
    """扫描单个目录下的所有 SKILL.md"""
    results = []
    skill_dir = dir_info["path"]
    desc = dir_info["desc"]
    
    if not skill_dir.exists():
        return [{
            "dir": desc,
            "skills": [],
            "error": "Directory not found"
        }]
    
    for skill_path in skill_dir.rglob("SKILL.md"):
        skill_name = skill_path.parent.name
        start_time = time.time()
        
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, error = extract_frontmatter(content)
            
            if error:
                errors = [error]
            else:
                errors = validate_frontmatter(frontmatter, skill_path)
            
            elapsed = round(time.time() - start_time, 3)
            
            results.append({
                "name": skill_name,
                "path": str(skill_path),
                "status": "pass" if not errors else "fail",
                "errors": errors,
                "elapsed": elapsed
            })
            
        except Exception as e:
            results.append({
                "name": skill_name,
                "path": str(skill_path),
                "status": "error",
                "errors": [f"Read error: {e}"],
                "elapsed": round(time.time() - start_time, 3)
            })
    
    return [{
        "dir": desc,
        "skills": results,
        "error": None
    }]


def generate_report(results: list) -> str:
    """生成 HTML 报告"""
    template = Template("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skill Linter Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #333; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }
        h2 { color: #555; margin-top: 30px; }
        .section { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #e0e0e0; }
        th { background: #f8f9fa; font-weight: 600; }
        .pass { color: #28a745; }
        .fail { color: #dc3545; }
        .error { color: #ffc107; }
        .error-msg { color: #dc3545; font-family: monospace; font-size: 14px; margin-top: 5px; }
        .stats { display: flex; gap: 20px; margin-bottom: 20px; }
        .stat { background: white; padding: 15px 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stat-value { font-size: 24px; font-weight: bold; }
        .stat-label { color: #666; font-size: 14px; }
        .pass .stat-value { color: #28a745; }
        .fail .stat-value { color: #dc3545; }
        .total .stat-value { color: #007bff; }
    </style>
</head>
<body>
    <h1>🔍 Skill Linter Report</h1>
    
    <div class="stats">
        <div class="stat total">
            <div class="stat-value">{{ total }}</div>
            <div class="stat-label">Total Skills</div>
        </div>
        <div class="stat pass">
            <div class="stat-value">{{ passing }}</div>
            <div class="stat-label">✅ Passing</div>
        </div>
        <div class="stat fail">
            <div class="stat-value">{{ failing }}</div>
            <div class="stat-label">❌ Failing/Errors</div>
        </div>
    </div>

{% for result in results %}
    <div class="section">
        <h2>{{ result.dir }}</h2>
        {% if result.error %}
            <p class="error-msg">⚠️ {{ result.error }}</p>
        {% elif not result.skills %}
            <p>No SKILL.md files found in this directory.</p>
        {% else %}
            <table>
                <thead>
                    <tr>
                        <th>Skill 名称</th>
                        <th>状态</th>
                        <th>耗时 (s)</th>
                    </tr>
                </thead>
                <tbody>
                    {% for skill in result.skills %}
                        <tr>
                            <td>{{ skill.name }}</td>
                            <td>
                                {% if skill.status == "pass" %}✅{% elif skill.status == "fail" %}❌{% else %}⚠️{% endif %}
                                {% if skill.status == "pass" %}<span class="pass">Pass</span>{% elif skill.status == "fail" %}<span class="fail">Fail</span>{% else %}<span class="error">Error</span>{% endif %}
                            </td>
                            <td>{{ skill.elapsed }}</td>
                        </tr>
                        {% if skill.errors %}
                        <tr>
                            <td colspan="3" class="error-msg">
                                {{ skill.errors | join('<br>') }}
                            </td>
                        </tr>
                        {% endif %}
                    {% endfor %}
                </tbody>
            </table>
        {% endif %}
    </div>
{% endfor %}

</body>
</html>""")
    
    total = sum(len(r["skills"]) for r in results)
    passing = sum(1 for r in results for s in r["skills"] if s["status"] == "pass")
    failing = total - passing
    
    return template.render(
        results=results,
        total=total,
        passing=passing,
        failing=failing
    )


def main():
    print("🔍 开始扫描技能目录...")
    
    all_results = []
    for dir_info in SKILL_DIRS:
        print(f"📁 扫描: {dir_info['desc']}")
        results = scan_skill_directory(dir_info)
        all_results.extend(results)
    
    # 生成报告
    report = generate_report(all_results)
    
    # 保存报告
    output_dir = Path("~/.hermes/cron/output").expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_path = output_dir / f"skill-lint-report-{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 报告已生成: {report_path}")
    print("📊 查看报告请在浏览器中打开该 HTML 文件")


if __name__ == "__main__":
    main()
