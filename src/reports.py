from datetime import datetime, timedelta
from src.query import filter_events

def access_report(events, resource):
    resource_events = filter_events(events, resource=resource)
    return {
        "resource": resource,
        "total_accesses": len(resource_events),
        "unique_actors": len({e["actor"] for e in resource_events}),
        "read_events": len([e for e in resource_events if e["action"] == "read"]),
        "write_events": len([e for e in resource_events if e["action"] in ("write", "update")]),
        "delete_events": len([e for e in resource_events if e["action"] == "delete"]),
        "denied_events": len([e for e in resource_events if e["outcome"] == "denied"]),
        "period": {
            "start": min((e["timestamp"] for e in resource_events), default=None),
            "end": max((e["timestamp"] for e in resource_events), default=None),
        }
    }

def actor_activity_report(events, actor, days=30):
    start = (datetime.utcnow() - timedelta(days=days)).isoformat()
    actor_events = filter_events(events, actor=actor, start=start)
    return {
        "actor": actor,
        "period_days": days,
        "total_actions": len(actor_events),
        "actions": {a: len([e for e in actor_events if e["action"] == a])
                    for a in {e["action"] for e in actor_events}},
    }

def compliance_summary(events):
    """Отчёт для compliance: sensitive resources, denied access, deletions."""
    return {
        "generated_at": datetime.utcnow().isoformat(),
        "total_events": len(events),
        "denied_access": len([e for e in events if e["outcome"] == "denied"]),
        "deletions": len([e for e in events if e["action"] == "delete"]),
        "exports": len([e for e in events if e["action"] == "export"]),
        "policy_changes": len([e for e in events if e["action"] == "policy_change"]),
        "unique_actors": len({e["actor"] for e in events}),
    }
