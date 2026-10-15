from datetime import datetime

def filter_events(events, actor=None, action=None, resource=None,
                   outcome=None, start=None, end=None):
    result = events
    if actor:
        result = [e for e in result if e.get("actor") == actor]
    if action:
        result = [e for e in result if e.get("action") == action]
    if resource:
        result = [e for e in result if resource in e.get("resource", "")]
    if outcome:
        result = [e for e in result if e.get("outcome") == outcome]
    if start:
        result = [e for e in result if e.get("timestamp", "") >= start]
    if end:
        result = [e for e in result if e.get("timestamp", "") <= end]
    return result

def group_by_action(events):
    groups = {}
    for e in events:
        a = e.get("action", "unknown")
        groups[a] = groups.get(a, 0) + 1
    return groups

def by_actor(events):
    groups = {}
    for e in events:
        a = e.get("actor", "unknown")
        groups[a] = groups.get(a, 0) + 1
    return groups
