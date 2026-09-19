#!/usr/bin/env python3
"""Conservatively detect project tooling and emit an engineering profile."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:  # pragma: no cover - Python < 3.11
    tomllib = None


def _package_data(root: Path) -> dict[str, Any]:
    path = root / "package.json"
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}


def _pyproject_data(root: Path) -> dict[str, Any]:
    path = root / "pyproject.toml"
    if not path.is_file() or tomllib is None:
        return {}
    try:
        with path.open("rb") as stream:
            value = tomllib.load(stream)
        return value if isinstance(value, dict) else {}
    except (OSError, tomllib.TOMLDecodeError):
        return {}


def _first_script(scripts: dict[str, Any], names: tuple[str, ...]) -> tuple[str | None, str | None]:
    for name in names:
        value = scripts.get(name)
        if isinstance(value, str):
            return name, f"npm run {name}"
    return None, None


def _tool(name: str | None = None, command: str | None = None) -> dict[str, str | None]:
    return {"name": name, "command": command}


def scan(root: Path) -> dict[str, Any]:
    root = root.resolve()
    package = _package_data(root)
    pyproject = _pyproject_data(root)
    scripts = package.get("scripts", {}) if isinstance(package.get("scripts"), dict) else {}
    deps: set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        value = package.get(key, {})
        if isinstance(value, dict):
            deps.update(value)

    languages: list[str] = []
    frameworks: list[str] = []
    if package or (root / "tsconfig.json").is_file():
        languages.append("typescript" if (root / "tsconfig.json").is_file() or "typescript" in deps else "javascript")
    if (root / "pyproject.toml").is_file():
        languages.append("python")
    if (root / "Cargo.toml").is_file():
        languages.append("rust")
    if "vue" in deps or any(root.glob("vite.config.*")) and any(root.rglob("*.vue")):
        frameworks.append("vue")
    if "react" in deps:
        frameworks.append("react")
    if "next" in deps:
        frameworks.append("nextjs")
    if "vite" in deps or any(root.glob("vite.config.*")):
        frameworks.append("vite")

    formatter = _tool()
    linter = _tool()
    typecheck = _tool()
    test_runner = _tool()

    script_name, command = _first_script(scripts, ("format:check", "format", "fmt"))
    if command:
        formatter = _tool(script_name, command)
    script_name, command = _first_script(scripts, ("lint", "check:lint"))
    if command:
        linter = _tool(script_name, command)
    script_name, command = _first_script(scripts, ("typecheck", "type-check", "check:types"))
    if command:
        typecheck = _tool(script_name, command)
    script_name, command = _first_script(scripts, ("test", "test:unit"))
    if command:
        test_runner = _tool(script_name, command)

    py_tools = pyproject.get("tool", {}) if isinstance(pyproject.get("tool"), dict) else {}
    if formatter["name"] is None:
        for name in ("ruff", "black"):
            if name in py_tools:
                formatter = _tool(name, "ruff format --check ." if name == "ruff" else "black --check .")
                break
    if linter["name"] is None:
        for name, cmd in (("ruff", "ruff check ."), ("flake8", "flake8 ."), ("pylint", "pylint .")):
            if name in py_tools:
                linter = _tool(name, cmd)
                break
    if typecheck["name"] is None:
        for name in ("mypy", "pyright"):
            if name in py_tools:
                typecheck = _tool(name, f"{name} .")
                break
    if test_runner["name"] is None and ("pytest" in py_tools or "pytest.ini_options" in py_tools):
        test_runner = _tool("pytest", "python -m pytest")

    if (root / "Cargo.toml").is_file():
        formatter = formatter if formatter["name"] else _tool("rustfmt", "cargo fmt --check")
        linter = linter if linter["name"] else _tool("clippy", "cargo clippy --all-targets --all-features -- -D warnings")
        typecheck = typecheck if typecheck["name"] else _tool("cargo-check", "cargo check --all-targets --all-features")
        test_runner = test_runner if test_runner["name"] else _tool("cargo-test", "cargo test")

    source_roots = [name for name in ("src", "app", "lib") if (root / name).is_dir()]
    test_roots = [name for name in ("tests", "test", "__tests__") if (root / name).is_dir()]
    return {
        "standard": {"version": "0.1.0", "strictness": "balanced"},
        "project": {
            "languages": sorted(set(languages)),
            "frameworks": sorted(set(frameworks)),
            "architecture": {"style": "unknown", "source_roots": source_roots, "test_roots": test_roots},
        },
        "quality": {"formatter": formatter, "linter": linter, "typecheck": typecheck, "test_runner": test_runner},
        "agent": {"target": "codex", "instructions": []},
    }


def _scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def to_yaml(value: Any, indent: int = 0) -> str:
    prefix = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{prefix}{key}:")
                lines.append(to_yaml(item, indent + 2))
            elif isinstance(item, (dict, list)):
                lines.append(f"{prefix}{key}: {'{}' if isinstance(item, dict) else '[]'}")
            else:
                lines.append(f"{prefix}{key}: {_scalar(item)}")
        return "\n".join(lines)
    if isinstance(value, list):
        return "\n".join(f"{prefix}- {_scalar(item)}" for item in value)
    return f"{prefix}{_scalar(value)}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument("--output", type=Path, help="Write YAML to this file instead of stdout.")
    parser.add_argument("--force", action="store_true", help="Replace an existing output file.")
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        parser.error(f"project root is not a directory: {args.root}")
    rendered = to_yaml(scan(args.root)) + "\n"
    if args.output:
        output = args.output.resolve()
        if output.exists() and not args.force:
            print(f"Refusing to overwrite existing profile: {output}", file=sys.stderr)
            return 2
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
