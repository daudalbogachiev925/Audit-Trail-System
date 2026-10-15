from src.audit_log import AuditLog
from src.events import AuditEvent, ActionType, Outcome
from src.integrity import verify_chain
import tempfile, os

def test_append_and_verify():
    tmp = tempfile.mktemp(suffix=".log")
    log = AuditLog(tmp)
    log.append(AuditEvent(ActionType.LOGIN, "u1", "system", Outcome.SUCCESS))
    log.append(AuditEvent(ActionType.READ, "u1", "data", Outcome.SUCCESS))
    entries = log.all()
    assert len(entries) == 2
    assert verify_chain(entries)["valid"] is True
    os.remove(tmp)

def test_tamper_detection():
    tmp = tempfile.mktemp(suffix=".log")
    log = AuditLog(tmp)
    log.append(AuditEvent(ActionType.LOGIN, "u1", "system", Outcome.SUCCESS))
    log.append(AuditEvent(ActionType.READ, "u1", "data", Outcome.SUCCESS))
    entries = log.all()
    entries[0]["actor"] = "hacker"
    assert verify_chain(entries)["valid"] is False
    os.remove(tmp)
