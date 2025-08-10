from __future__ import annotations

from pathlib import Path
import shutil
from typing import Iterable, List


def rebalance_dataset(source: Path | str, destination: Path | str, fraction: float = 0.25) -> List[str]:
    """Copy a fraction of files from source to destination.

    Files are selected deterministically by sorting the source directory and
    copying every Nth file where N is 1/fraction.

    Returns a list of file names that were copied.
    """
    source_path = Path(source)
    dest_path = Path(destination)
    dest_path.mkdir(parents=True, exist_ok=True)

    files = sorted([p for p in source_path.iterdir() if p.is_file()])
    if not files:
        return []

    step = max(int(round(1 / fraction)), 1)
    selected = files[step - 1 :: step]

    for file_path in selected:
        shutil.copy2(file_path, dest_path / file_path.name)

    return [f.name for f in selected]
