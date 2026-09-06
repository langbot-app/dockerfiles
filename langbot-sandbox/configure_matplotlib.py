"""Customize the bundled rc template without deleting required defaults."""

from pathlib import Path
import re
import sys

import matplotlib


template = Path(matplotlib.get_data_path()) / "matplotlibrc"
content = template.read_text(encoding="utf-8")
for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    key, value = line.split(":", 1)
    # Matplotlib derives rcParamsDefault from this entire template, including
    # commented settings. Replacing it with a small user rc file breaks import.
    content, count = re.subn(
        rf"^#*\s*{re.escape(key)}:.*$",
        f"{key}:{value}",
        content,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise RuntimeError(f"Expected exactly one template setting for {key}, got {count}")
template.write_text(content, encoding="utf-8")
