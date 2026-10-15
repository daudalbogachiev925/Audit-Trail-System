import json
import hashlib

def verify_chain(entries):
    prev_hash = "0" * 64
    errors = []
    for i, entry in enumerate(entries):
        stored_hash = entry.get("hash")
        entry_copy = dict(entry)
        entry_copy.pop("hash", None)
        payload = json.dumps(entry_copy, sort_keys=True, ensure_ascii=False).encode()
        expected = hashlib.sha256(prev_hash.encode() + payload).hexdigest()
        if expected != stored_hash:
            errors.append({"index": i, "expected": expected, "got": stored_hash})
        prev_hash = stored_hash
    return {"valid": len(errors) == 0, "errors": errors, "total": len(entries)}
