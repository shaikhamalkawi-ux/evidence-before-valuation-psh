from __future__ import annotations

import hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = root / "SHA256SUMS.txt"
excluded = {".git", "__pycache__"}
files = sorted(
    path for path in root.rglob("*")
    if path.is_file()
    and not any(part in excluded for part in path.relative_to(root).parts)
    and path != manifest
)
lines = []
for path in files:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {path.relative_to(root).as_posix()}")
manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {len(lines)} SHA-256 entries to {manifest.name}")
