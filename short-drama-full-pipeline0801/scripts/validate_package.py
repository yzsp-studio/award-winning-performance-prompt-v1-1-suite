#!/usr/bin/env python3
"""Validate required files and internal references for short-drama-full-pipeline."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "references/chain-audit.md",
    "references/production-data-center.md",
    "references/story-structure.md",
    "references/script-format.md",
    "references/asset-pipeline.md",
    "references/storyboard-pipeline.md",
    "references/video-prompt-pipeline.md",
    "references/post-production-pipeline.md",
    "references/qc-checklist.md",
    "references/api_reference.md",
]
FORBIDDEN_MARKERS = ["TODO", "placeholder", "占位", "Replace with", "example_asset", "example.py"]
REQUIRED_KEYWORDS = [
    "production_chain_id: short-drama-full-pipeline",
    "workflow_source: user_skill_locked",
    "fallback_allowed: false",
    "template_source",
    "LOCAL_CHAIN_AUDIT",
    "不得走线上通用制作链路",
    "不得 light dispatch",
    "全链路继承矩阵",
    "参考图继承矩阵",
    "reference count lock",
    "verbatim dispatch lock",
    "台词保真验收硬规则",
    "加硬修改保护",
]


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    errors = []

    for rel in REQUIRED:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing required file: {rel}")
            continue
        if path.stat().st_size == 0:
            errors.append(f"Empty required file: {rel}")

    skill_path = ROOT / "SKILL.md"
    if skill_path.exists():
        skill_text = read_text("SKILL.md")
        if not skill_text.startswith("---\nname: short-drama-full-pipeline\n"):
            errors.append("SKILL.md frontmatter name is not exact")
        if "description:" not in skill_text.split("---", 2)[1]:
            errors.append("SKILL.md frontmatter missing description")

        linked_refs = sorted(set(re.findall(r"`(references/[^`]+\.md)`", skill_text)))
        for rel in linked_refs:
            if not (ROOT / rel).exists():
                errors.append(f"Broken SKILL.md reference link: {rel}")
        for rel in REQUIRED:
            if rel.startswith("references/") and rel not in linked_refs:
                errors.append(f"Required reference not listed in SKILL.md: {rel}")

    combined_text = ""
    for rel in REQUIRED:
        path = ROOT / rel
        if not path.exists():
            continue
        text = read_text(rel)
        combined_text += "\n" + text
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                errors.append(f"Forbidden marker '{marker}' found in {rel}")

    for keyword in REQUIRED_KEYWORDS:
        if keyword not in combined_text:
            errors.append(f"Missing required chain-lock keyword: {keyword}")

    if errors:
        print("short-drama-full-pipeline package FAILED")
        for item in errors:
            print(f"- {item}")
        return 1

    print("short-drama-full-pipeline package OK")
    print(f"checked_files={len(REQUIRED)}")
    print("chain_lock=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
