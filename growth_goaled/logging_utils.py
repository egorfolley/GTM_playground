from __future__ import annotations

import json
import logging
import sys
from dataclasses import asdict
from typing import Any


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("growth_goaled_snapshot")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%H:%M:%S")
        )
        logger.addHandler(handler)

    return logger


LOGGER = setup_logger()


def log_step(step: str, data: Any | None = None, max_chars: int = 1600) -> None:
    """Log a readable pipeline step to the Streamlit terminal."""
    if data is None:
        LOGGER.info(step)
        return

    try:
        if hasattr(data, "__dataclass_fields__"):
            serializable = asdict(data)
        else:
            serializable = data
        rendered = json.dumps(serializable, indent=2, default=str)
    except TypeError:
        rendered = str(data)

    if len(rendered) > max_chars:
        rendered = f"{rendered[:max_chars]}... [truncated]"

    LOGGER.info("%s\n%s", step, rendered)

