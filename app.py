import streamlit as st
import pandas as pd
from monday_api import fetch_board_items

# ---------- CONFIG ----------
DEALS_BOARD_ID = 5026562971
WORK_BOARD_ID = 5026563122

st.set_page_config(page_title="Founder BI Agent", layout="wide")
st.title("📊 Founder Business Intelligence AI Agent")

question = st.text_input("Ask a business question:")

if question:
    st.write("Fetching data from monday.com...")

    deals_df = fetch_board_items(DEALS_BOARD_ID)
    work_df = fetch_board_items(WORK_BOARD_ID)

    # ---------- SIMPLE BUSINESS INTELLIGENCE ----------
    insight = ""

    if not deals_df.empty:
        # try numeric conversion
        if "Amount" in deals_df.columns:
            deals_df["Amount"] = pd.to_numeric(deals_df["Amount"], errors="coerce")

            total_pipeline = deals_df["Amount"].sum()
            avg_deal = deals_df["Amount"].mean()

            open_deals = deals_df[
                deals_df.get("Status", "").str.contains("Open", case=False, na=False)
            ].shape[0]

            insight += f"""
### 📈 Sales Pipeline Summary
- **Total Pipeline Value:** ₹{total_pipeline:,.0f}
- **Average Deal Size:** ₹{avg_deal:,.0f}
- **Number of Open Deals:** {open_deals}
"""

    if not work_df.empty:
        completed = work_df[
            work_df.get("Status", "").str.contains("Completed", case=False, na=False)
        ].shape[0]

        total_work = len(work_df)

        insight += f"""
### 🛠 Execution Summary
- **Total Work Orders:** {total_work}
- **Completed Work Orders:** {completed}
- **Completion Rate:** {(completed/total_work*100 if total_work else 0):.1f}%
"""

    # ---------- DISPLAY ----------
    st.subheader("🤖 AI-Style Insight")
    st.markdown(insight if insight else "No meaningful insight found.")

    st.subheader("Deals Data")
    st.dataframe(deals_df)

    st.subheader("Work Orders Data")
    st.dataframe(work_df)
