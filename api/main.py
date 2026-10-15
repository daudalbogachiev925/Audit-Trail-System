from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from src.audit_log import AuditLog
from src.events import AuditEvent, ActionType, Outcome
from src.query import filter_events, group_by_action
from src.integrity import verify_chain
from src.reports import compliance_summary, access_report

app = FastAPI(title="Audit Trail API")
audit = AuditLog()

class EventIn(BaseModel):
    action: ActionType
    actor: str
    resource: str
    outcome: Outcome
    ip: str = ""
    user_agent: str = ""
    details: dict = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/events")
def log_event(e: EventIn):
    entry = audit.append(AuditEvent(**e.dict()))
    return entry

@app.get("/events")
def list_events(actor: Optional[str] = None, action: Optional[str] = None,
                resource: Optional[str] = None, outcome: Optional[str] = None):
    events = audit.all()
    return filter_events(events, actor, action, resource, outcome)

@app.get("/events/groups")
def groups():
    return group_by_action(audit.all())

@app.get("/integrity")
def integrity():
    return verify_chain(audit.all
