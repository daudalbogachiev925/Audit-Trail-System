from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import uuid

class ActionType(str, Enum):
    READ = "read"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
    LOGIN = "login"
    POLICY_CHANGE = "policy_change"
    ACCESS_DENIED = "access_denied"

class Outcome(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    DENIED = "denied"

@dataclass
class AuditEvent:
    action: ActionType
    actor: str
    resource: str
    outcome: Outcome
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    ip: str = ""
    user_agent: str = ""
    details: dict = field(default_factory=dict)

    def to_dict(self):
        d = asdict(self)
        d["action"] = self.action.value
        d["outcome"] = self.outcome.value
        return d
