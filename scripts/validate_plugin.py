#!/usr/bin/env python3
"""Deterministic validator for the enterprise-actions plugin."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
RAW_BASE = "https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/enterprise-search"

RETAINED = {
    "skills/search-strategy/SKILL.md": ["skills/search-strategy/SKILL.md"],
    "skills/source-management/SKILL.md": ["skills/source-management/SKILL.md"],
    "skills/knowledge-synthesis/SKILL.md": ["skills/knowledge-synthesis/SKILL.md"],
    "commands/search.md": ["commands/search.md", "skills/search/SKILL.md"],
    "commands/digest.md": ["commands/digest.md", "skills/digest/SKILL.md"],
    "CONNECTORS.md": ["CONNECTORS.md"],
    ".mcp.json": [".mcp.json"],
    "LICENSE": ["LICENSE"],
}

ACTING_SKILLS = [
    "triage",
    "draft-reply",
    "meeting-to-work",
    "board-sync",
    "rollup",
    "crm-log",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> tuple[bool, dict[str, Any] | None, str]:
    try:
        return True, json.loads(path.read_text(encoding="utf-8")), "ok"
    except Exception as exc:
        return False, None, str(exc)


def print_check(ok: bool, label: str, detail: str = "") -> bool:
    status = "PASS" if ok else "FAIL"
    suffix = f" - {detail}" if detail else ""
    print(f"[{status}] {label}{suffix}")
    return ok


def download_upstream(candidates: list[str]) -> tuple[str, bytes]:
    last_error = ""
    for rel in candidates:
        url = f"{RAW_BASE}/{rel}"
        try:
            with urlopen(url, timeout=30) as response:
                return rel, response.read()
        except HTTPError as exc:
            last_error = f"{url} -> HTTP {exc.code}"
        except URLError as exc:
            last_error = f"{url} -> {exc.reason}"
    raise RuntimeError(last_error or "no candidate upstream path succeeded")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter start")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("missing frontmatter end")

    fields: dict[str, str] = {}
    for raw_line in text[4:end].splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def validate_manifests() -> bool:
    ok = True

    plugin_ok, plugin, plugin_msg = read_json(ROOT / ".claude-plugin" / "plugin.json")
    ok &= print_check(plugin_ok, "plugin.json parses", plugin_msg)
    if plugin:
        required = [
            plugin.get("name") == "enterprise-actions",
            re.fullmatch(r"\d+\.\d+\.\d+", str(plugin.get("version", ""))) is not None,
            bool(plugin.get("description")),
            plugin.get("author", {}).get("name") == "Marco Lobo",
            bool(plugin.get("builtOn")) or "built on" in plugin.get("description", "").lower(),
        ]
        ok &= print_check(all(required), "plugin.json required fields", f"name={plugin.get('name')} version={plugin.get('version')}")

    market_ok, market, market_msg = read_json(ROOT / ".claude-plugin" / "marketplace.json")
    ok &= print_check(market_ok, "marketplace.json parses", market_msg)
    if market:
        plugins = market.get("plugins")
        required = [
            bool(market.get("name")),
            bool(market.get("owner", {}).get("name")),
            isinstance(plugins, list) and len(plugins) == 1,
            isinstance(plugins, list) and plugins[0].get("name") == "enterprise-actions",
            isinstance(plugins, list) and plugins[0].get("source") == "./",
        ]
        ok &= print_check(all(required), "marketplace.json required fields", f"plugins={len(plugins or [])}")

    return ok


def validate_retained_files() -> bool:
    ok = True
    print("Retained upstream file hashes:")
    for local_rel, upstream_candidates in RETAINED.items():
        local_path = ROOT / local_rel
        if not local_path.exists():
            ok &= print_check(False, f"{local_rel} exists")
            continue

        try:
            upstream_rel, upstream_bytes = download_upstream(upstream_candidates)
        except Exception as exc:
            ok &= print_check(False, f"{local_rel} upstream download", str(exc))
            continue

        local_bytes = local_path.read_bytes()
        local_sha = sha256(local_bytes)
        upstream_sha = sha256(upstream_bytes)
        matched = local_sha == upstream_sha
        detail = f"local={local_sha} upstream={upstream_sha} upstream_path={upstream_rel}"
        if upstream_rel != upstream_candidates[0]:
            detail += f" adjusted_from={upstream_candidates[0]}"
        ok &= print_check(matched, f"{local_rel} byte-identical", detail)
    return ok


def validate_frontmatter() -> bool:
    ok = True
    for name in ACTING_SKILLS:
        skill_path = ROOT / "skills" / name / "SKILL.md"
        command_path = ROOT / "commands" / f"{name}.md"
        for path in [skill_path, command_path]:
            try:
                fields = parse_frontmatter(path)
                fields_ok = bool(fields.get("name")) and bool(fields.get("description"))
                if path.name == "SKILL.md":
                    fields_ok = fields_ok and bool(fields.get("argument-hint"))
                else:
                    fields_ok = fields_ok and bool(fields.get("argument-hint"))
                ok &= print_check(fields_ok, f"{path.relative_to(ROOT)} frontmatter", f"name={fields.get('name')}")
            except Exception as exc:
                ok &= print_check(False, f"{path.relative_to(ROOT)} frontmatter", str(exc))
    return ok


def validate_action_safety_files() -> bool:
    required = [
        ROOT / "skills" / "action-safety" / "SKILL.md",
        ROOT / "lib" / "action_safety.py",
        ROOT / "lib" / "action_ledger.py",
        ROOT / "hooks" / "action-gate.sh",
    ]
    ok = True
    for path in required:
        exists = path.exists()
        detail = ""
        if path.name == "action-gate.sh" and exists:
            executable = os.access(path, os.X_OK)
            exists = exists and executable
            detail = "executable" if executable else "not executable"
        ok &= print_check(exists, f"{path.relative_to(ROOT)} exists", detail)
    return ok


def run_command(label: str, command: list[str], cwd: Path = ROOT, timeout: int = 120, fail_on_nonzero: bool = True) -> bool:
    try:
        completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    except FileNotFoundError as exc:
        ok = not fail_on_nonzero
        print_check(ok, label, f"not runnable: {exc}")
        return ok
    except subprocess.TimeoutExpired:
        print_check(False if fail_on_nonzero else True, label, "timeout")
        return not fail_on_nonzero

    output = (completed.stdout + completed.stderr).strip()
    if output:
        print(output)
    ok = completed.returncode == 0
    if fail_on_nonzero:
        print_check(ok, label, f"rc={completed.returncode}")
        return ok

    status = "runnable" if ok else "not runnable/nonzero"
    print_check(True, label, f"{status} rc={completed.returncode}")
    return True


def validate_pytest() -> bool:
    return run_command(
        "pytest action safety and ledger",
        [
            sys.executable,
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "tests/test_action_safety.py",
            "tests/test_action_ledger.py",
        ],
    )


def validate_hook() -> bool:
    return run_command("hook bash test", ["bash", "tests/test_action_gate.sh"])


def plugin_load_check() -> bool:
    return run_command(
        "claude plugin load check",
        ["claude", "--plugin-dir", str(ROOT), "--help"],
        timeout=30,
        fail_on_nonzero=False,
    )


def main() -> int:
    print(f"Enterprise Actions validator root: {ROOT}")

    results = [
        validate_manifests(),
        validate_retained_files(),
        validate_frontmatter(),
        validate_action_safety_files(),
        validate_pytest(),
        validate_hook(),
        plugin_load_check(),
    ]

    required_ok = all(results[:6])
    print(f"VALIDATOR RESULT: {'PASS' if required_ok else 'FAIL'}")
    return 0 if required_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
