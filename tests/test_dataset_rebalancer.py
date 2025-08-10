import sys
from pathlib import Path

# Ensure the project root is on sys.path for direct execution of `pytest`
sys.path.append(str(Path(__file__).resolve().parent.parent))

from dataset_rebalancer import rebalance_dataset


def populate_dir(directory: Path, count: int) -> None:
    for i in range(count):
        (directory / f"file_{i}.txt").write_text("data")


def test_rebalance_copies_quarter_with_stable_selection(tmp_path):
    source = tmp_path / "source"
    dest1 = tmp_path / "dest1"
    dest2 = tmp_path / "dest2"
    source.mkdir()

    populate_dir(source, 20)

    copied1 = rebalance_dataset(source, dest1)
    copied2 = rebalance_dataset(source, dest2)

    assert len(copied1) == 5
    assert len(list(dest1.iterdir())) == 5
    assert copied1 == copied2
    assert sorted(p.name for p in dest1.iterdir()) == sorted(copied1)
