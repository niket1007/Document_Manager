import streamlit as st
import pandas as pd
from GDrive.services import get_gdrive_instance

def admin_ui():
    st.title("🛡️ Admin Dashboard")
    session = get_gdrive_instance()
    
    # --- 1. Storage Metrics ---
    st.subheader("📊 GDrive Storage Usage")
    quota = session.get_storage_quota()
    
    # Convert bytes to Gigabytes for readability
    limit = int(quota.get('limit', 0)) / (1024**3)
    usage = int(quota.get('usage', 0)) / (1024**3)
    used_pct = (usage / limit) * 100 if limit > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Limit", f"{limit:.1f} GB")
    col2.metric("Used Space", f"{usage:.2f} GB", delta=f"{used_pct:.1f}%")
    col3.metric("Available", f"{(limit - usage):.1f} GB")

    st.progress(used_pct / 100)

    # --- 2. API Request Tracker ---
    st.divider()
    st.subheader("📈 App Performance")
    
    total_reqs = st.session_state.get("api_requests", 0)
    st.info(f"Total API requests made in this session: **{total_reqs}**")
    
    # Optional: Visualizing request limits
    # Google free limit is 20,000 per minute per project
    st.write("Usage vs Google Quota (20k/min)")
    st.bar_chart(pd.DataFrame({"Requests": [total_reqs]}, index=["Current Session"]))

if st.session_state.get("logged_in", False):
    admin_ui()
else:
    st.error("Unauthorized access.")