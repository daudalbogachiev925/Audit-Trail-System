import json
import hashlib
from pathlib import Path
from src.events import AuditEvent

class AuditLog:
    """Append-only log с hash chain для integrity."""
    def __init__(self, path="audit.log"):
        self.path = Path(path)
        self.prev_hash = "0" * 64
        if self.path.exists():
            self._load_last_hash()

    def _load_last_hash(self):
        last_line = None
        with open(self.path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    last_line = line
        if last_line:
            entry = json.loads(last_line)
            self.prev_hash = entry.get("hash", self.prev_hash)

    def _compute_hash(self, entry: dict) -> str:
        payload = json.dumps(entry, sort_keys=True, ensure_ascii=False).encode()
        h = hashlib.sha256(self.prev_hash.encode() + payload).hexdigest()
        return h

    def append(self, event: AuditEvent):
        entry = event.to_dict()
        entry["prev_hash"] = self.prev_hash
        entry["hash"] = self._compute_hash(entry)
        self.prev_hash = entry["hash"]
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry

    def all(self):
        if not self.path.exists():
            return []
        with open(self.path, encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
