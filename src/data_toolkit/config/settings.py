"""Central application configuration."""

from pathlib import Path

REQUIRED_COLUMNS: tuple[str, ...] = ("product", "quantity", "price")

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_LOG_DIR = PROJECT_ROOT / "logs"
DEFAULT_LOG_FILE = DEFAULT_LOG_DIR / "app.log"
