import streamlit as st
import pandas as pd
from src.audit_log import AuditLog
from src.events import AuditEvent, ActionType, Outcome
from src.query import filter_events, group_by_action, by_actor
from src.integrity import verify_chain
from src.reports import compliance_summary

st.set_page_config(page_title="Audit Trail", layout="wide")
st.title("📜 Audit Trail System")

audit = AuditLog("audit.log")

# Seed
if not audit.all():
    samples = [
        (ActionType.LOGIN, "alice", "system", Outcome.SUCCESS),
        (ActionType.READ, "alice", "customers", Outcome.SUCCESS),
        (ActionType.EXPORT, "bob", "customers", Outcome.SUCCESS),
        (ActionType.DELETE, "admin", "orders/12345", Outcome.SUCCESS),
        (ActionType.ACCESS_DENIED, "charlie", "salaries", Outcome.DENIED),
        (ActionType.POLICY_CHANGE, "admin", "policy/p2", Outcome.SUCCESS),
        (ActionType.READ, "bob", "customers", Outcome.SUCCESS),
    ]
    for action, actor, resource, outcome in samples:
        audit.append(AuditEvent(action, actor, resource, outcome))

events = audit.all()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total events", len(events))
c2.metric("Unique actors", len({e["actor"] for e in events}))
c3.metric("Denied", len([e for e in events if e["outcome"] == "denied"]))
c4.metric("Deletions", len([e for e in events if e["action"] == "delete"]))

tab1, tab2, tab3, tab4 = st.tabs(["📋 Events", "🔍 Filters", "🔐 Integrity", "📊 Reports"])

with tab1:
    st.dataframe(pd.DataFrame(events))

with tab2:
    actor = st.text_input("Actor")
    action = st.selectbox("Action", ["All"] + [a.value for a in ActionType])
    filtered = filter_events(events,
                             actor=actor or None,
                             action=action if action != "All" else None)
    st.dataframe(pd.DataFrame(filtered))
    st.bar_chart(pd.Series(group_by_action(filtered)))

with tab3:
    result = verify_chain(events)
    if result["valid"]:
        st.success(f"✅ Hash chain валидна ({result['total']} entries)")
    else:
        st.error(f"❌ Найдено нарушений: {len(result['errors'])}")
        st.json(result["errors"])

with tab4:
    st.subheader("Compliance Summary")
    st.json(compliance_summary(events))
    st.subheader("Top actors")
    st.bar_chart(pd.Series(by_actor(events)))
