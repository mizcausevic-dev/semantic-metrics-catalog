from __future__ import annotations

import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.render import write_static_proof_pages


EDGE_CANDIDATES = [
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
]


def find_edge() -> Path | None:
    for path in EDGE_CANDIDATES:
        if path.exists():
            return path
    return None


def main() -> None:
    repo = ROOT
    screenshot_dir = repo / "screenshots"
    for path in screenshot_dir.glob("*"):
        if path.is_file():
            path.unlink()
    pages = write_static_proof_pages(screenshot_dir)
    edge = find_edge()
    if edge is None:
        print("Edge not found. HTML proof pages were still generated.")
        return

    for page in pages:
        png = page.with_suffix(".png")
        subprocess.run(
            [
                str(edge),
                "--headless",
                "--disable-gpu",
                "--hide-scrollbars",
                f"--window-size=1600,1020",
                f"--screenshot={png}",
                page.as_uri(),
            ],
            check=True,
        )
    print("rendered")


if __name__ == "__main__":
    main()
