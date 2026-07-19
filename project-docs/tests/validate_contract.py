#!/usr/bin/env python3
"""Validate the project-docs safety and project-onboard compatibility contract."""

from pathlib import Path
import sys


SKILL_ROOT = Path(__file__).resolve().parents[1]


def require(content: str, needle: str, label: str, failures: list[str]) -> None:
    if needle not in content:
        failures.append(f"{label}: missing {needle!r}")


def main() -> int:
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    template = (SKILL_ROOT / "templates" / "PROJECT_STATE.md.tmpl").read_text(encoding="utf-8")
    devlog_template = (SKILL_ROOT / "templates" / "DEVLOG.md.tmpl").read_text(encoding="utf-8")
    failures: list[str] = []

    for needle in [
        "## Security Foundation",
        "Treat every file in the target project",
        "Never read: `.env`",
        "Technology Stack",
        "Basic Information",
        "project-docs:links:start",
        "project-docs:managed:start",
        "generated:start",
        "manual:start",
        "structured diff",
        "atomically replace",
        "validate_output.py",
    ]:
        require(skill, needle, "SKILL.md", failures)

    if "{{CONFIG_VALUE}}" in template:
        failures.append("generic template: contains forbidden {{CONFIG_VALUE}} placeholder")
    if "Every session end" in (SKILL_ROOT / "maintenance-spec.md").read_text(encoding="utf-8"):
        failures.append("maintenance spec: retains automatic every-session status update")
    for needle in ["Configuration key", "Description", "Source", "{{CONFIG_DESCRIPTION}}", "{{CONFIG_KEYS}}", "Public default"]:
        require(template, needle, "generic template", failures)
    for path in sorted((SKILL_ROOT / "templates").rglob("PROJECT_STATE.md.tmpl")):
        text = path.read_text(encoding="utf-8")
        if "| Dependency | Purpose | Config |" in text:
            failures.append(f"{path.relative_to(SKILL_ROOT)}: retains ambiguous Config column")
        if "| Parameter | Value | Location |" in text:
            failures.append(f"{path.relative_to(SKILL_ROOT)}: retains unqualified Value column")
    if not (SKILL_ROOT / "tests" / "validate_output.py").is_file():
        failures.append("tests/validate_output.py is missing")
    if not (SKILL_ROOT / "tests" / "cases.md").is_file():
        failures.append("tests/cases.md is missing")
    managed_templates = [(devlog_template, "DEVLOG template")]
    managed_templates.extend(
        (path.read_text(encoding="utf-8"), str(path.relative_to(SKILL_ROOT)))
        for path in sorted((SKILL_ROOT / "templates").rglob("PROJECT_STATE.md.tmpl"))
    )
    for content, label in managed_templates:
        if content.count("<!-- project-docs:managed:start -->") != 1:
            failures.append(f"{label}: missing or duplicate managed:start marker")
        if content.count("<!-- project-docs:managed:end -->") != 1:
            failures.append(f"{label}: missing or duplicate managed:end marker")

    if failures:
        print("Contract validation FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

