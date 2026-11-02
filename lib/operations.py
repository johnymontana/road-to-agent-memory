"""Atomic local receipts; an HTTP retry can recover the completed operation."""

import hashlib
import json
import os
from pathlib import Path


def read_receipt(data_dir: Path, request_id: str):
    path = data_dir / "operations" / (hashlib.sha256(request_id.encode()).hexdigest() + ".json")
    return json.loads(path.read_text()) if path.exists() else None


def write_receipt(data_dir: Path, request_id: str, response: dict):
    directory = data_dir / "operations"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (hashlib.sha256(request_id.encode()).hexdigest() + ".json")
    temporary = path.with_suffix(f".{os.getpid()}.tmp")
    temporary.write_text(json.dumps(response, default=str))
    temporary.replace(path)
