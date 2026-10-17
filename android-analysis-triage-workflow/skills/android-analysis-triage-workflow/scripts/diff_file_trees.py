#!/usr/bin/env python3
"""Hash and diff two extracted, matching Android filesystem trees."""

import argparse
import hashlib
import json
import os
import stat
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(root):
    entries = {}

    def visit(directory):
        with os.scandir(directory) as items:
            for item in items:
                path = Path(item.path)
                info = item.stat(follow_symlinks=False)
                relative = path.relative_to(root).as_posix()
                if stat.S_ISDIR(info.st_mode):
                    visit(path)
                    continue
                kind = "regular" if stat.S_ISREG(info.st_mode) else "symlink" if stat.S_ISLNK(info.st_mode) else "special"
                entries[relative] = {
                    "type": kind,
                    "sha256": sha256(path) if kind == "regular" else None,
                    "size": info.st_size,
                    "mode": stat.S_IMODE(info.st_mode),
                    "mtime_ns": info.st_mtime_ns,
                    "link_target": os.readlink(path) if kind == "symlink" else None,
                }

    visit(root)
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--partition", required=True)
    parser.add_argument("--interval", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    before_root, after_root = args.before.resolve(), args.after.resolve()
    if not before_root.is_dir() or not after_root.is_dir() or before_root == after_root:
        parser.error("before and after must be distinct existing directories")
    if args.output.resolve().is_relative_to(before_root) or args.output.resolve().is_relative_to(after_root):
        parser.error("output must be outside both snapshot trees")
    before, after = inventory(before_root), inventory(after_root)
    changes = []
    for path in sorted(before.keys() | after.keys()):
        old, new = before.get(path), after.get(path)
        if old == new:
            continue
        status = "created" if old is None else "deleted" if new is None else "modified"
        content_changed = old is not None and new is not None and (old["type"], old["sha256"], old["link_target"]) != (new["type"], new["sha256"], new["link_target"])
        metadata_changed = old is not None and new is not None and (old["size"], old["mode"], old["mtime_ns"]) != (new["size"], new["mode"], new["mtime_ns"])
        basis = "presence" if status != "modified" else "content+metadata" if content_changed and metadata_changed else "content" if content_changed else "metadata"
        changes.append({"partition": args.partition, "interval": args.interval, "path": path,
                        "status": status, "change_basis": basis, "before": old, "after": new})
    result = {"schema_version": 1, "partition": args.partition, "interval": args.interval,
              "before_root": str(before_root), "after_root": str(after_root),
              "before_entries": len(before), "after_entries": len(after),
              "changes": changes}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
