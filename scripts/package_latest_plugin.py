#!/usr/bin/env python3
"""Build or verify the sole versioned Android triage plugin archive."""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path


PLUGIN = "android-analysis-triage-workflow"
VERSION_RE = re.compile(r"\d+\.\d+\.\d+\Z")


def files_for(plugin_dir, root):
    files = sorted(p for p in plugin_dir.rglob("*") if p.is_file())
    if not files or any(p.is_symlink() for p in plugin_dir.rglob("*")):
        raise ValueError("plugin source is empty or contains symlinks")
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in files}


def check_archive(archive, expected):
    with zipfile.ZipFile(archive) as package:
        names = package.namelist()
        if len(names) != len(set(names)) or set(names) != set(expected):
            raise ValueError("archive entries do not match plugin source")
        if package.testzip() is not None:
            raise ValueError("archive integrity check failed")
        for name, contents in expected.items():
            if package.read(name) != contents:
                raise ValueError(f"archive entry differs from source: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="directory containing the plugin folder and versioned ZIP")
    parser.add_argument("--check", action="store_true", help="verify without changing files")
    args = parser.parse_args()
    root = args.root.resolve()
    plugin_dir = root / PLUGIN
    version = json.loads((plugin_dir / "plugin.json").read_text(encoding="utf-8"))["version"]
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise ValueError("plugin.json must contain a numeric major.minor.patch version")
    skill = (plugin_dir / "skills" / PLUGIN / "SKILL.md").read_text(encoding="utf-8")
    if not re.search(rf"(?m)^  version: {re.escape(version)}\s*$", skill):
        raise ValueError("SKILL.md version does not match plugin.json")
    expected = files_for(plugin_dir, root)
    archive = root / f"{PLUGIN}-{version}.zip"
    archives = sorted(root.glob(f"{PLUGIN}-*.zip"))
    if args.check:
        if archives != [archive]:
            raise ValueError(f"expected only {archive.name}; found {[p.name for p in archives]}")
        check_archive(archive, expected)
        print(f"Verified {archive.name}: {len(expected)} source files; no older ZIPs")
        return
    temporary = root / f".{archive.name}.tmp"
    try:
        with zipfile.ZipFile(temporary, "w") as package:
            for name, contents in expected.items():
                info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                package.writestr(info, contents, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        temporary.replace(archive)
    finally:
        temporary.unlink(missing_ok=True)
    for old in archives:
        if old != archive:
            old.unlink()
    check_archive(archive, expected)
    print(f"Built {archive.name}: {len(expected)} source files; removed {sum(old != archive for old in archives)} older ZIPs")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"Packaging failed: {error}", file=sys.stderr)
        raise SystemExit(1)
