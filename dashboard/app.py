import streamlit as st
import pandas as pd
from pathlib import Path

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="UIDAI – Aadhaar Decision Support",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
GRANULAR_FILE = BASE_DIR / "data" / "processed" / "granular_uidai.csv"
RISK_FILE = BASE_DIR / "results" / "final_policy_output.csv"

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<h2 style='color:#FF6E2E'>Aadhaar Intelligence & Decision Support Platform (AIDSP)</h2>
<hr>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================
if not GRANULAR_FILE.exists() or not RISK_FILE.exists():
    st.error("❌ Required data files not found. Run the pipeline first.")
    st.stop()

granular_df = pd.read_csv(GRANULAR_FILE)
risk_df = pd.read_csv(RISK_FILE)

granular_df["date"] = pd.to_datetime(granular_df["date"], errors="coerce")
granular_df["date"] = granular_df["date"].dt.to_period("M").dt.to_timestamp()

for col in ["enrolment", "biometric", "demographic"]:
    granular_df[col] = pd.to_numeric(granular_df[col], errors="coerce").fillna(0)

# ==================================================
# CONTROL PANEL
# ==================================================
st.markdown("## 🗂 Administrative Control Panel")

c1, c2, c3, c4 = st.columns([1.1, 1.1, 1.5, 1.2])

with c1:
    view = st.radio(
        "Analysis Level",
        ["State Intelligence", "District Drill-down", "PIN Analysis"]
    )

with c2:
    state = st.selectbox(
        "State / UT",
        sorted(granular_df["state"].unique())
    )

with c3:
    min_date = granular_df["date"].min().date()
    max_date = granular_df["date"].max().date()
    date_range = st.date_input(
        "Time Period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

with c4:
    demo_mode = st.toggle("🎤 Demo Mode", value=False)

# Date handling
if isinstance(date_range, tuple):
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date = end_date = pd.to_datetime(date_range)

gdf = granular_df[
    (granular_df["state"] == state) &
    (granular_df["date"] >= start_date) &
    (granular_df["date"] <= end_date)
]

# ==================================================
# RECOMMENDATION & CONFIDENCE LOGIC
# ==================================================
def generate_recommendation(row):
    risk = row["predicted_risk_score"]
    if risk < 0.4:
        return "Low Operational Risk", "Low Intervention", "Normal operational patterns observed"
    elif risk < 0.7:
        return "Moderate Operational Risk", "Medium Intervention", "Sustained increase in updates"
    else:
        return "High Operational Risk", "High Intervention", "Sharp activity surge detected"

def model_confidence(rows):
    if rows > 5000:
        return "High Confidence"
    elif rows > 1000:
        return "Medium Confidence"
    else:
        return "Low Confidence"

# ==================================================
# 1️⃣ STATE INTELLIGENCE
# ==================================================
if view == "State Intelligence":
    st.subheader(f"State Risk Intelligence — {state}")

    sr = risk_df[risk_df["state"] == state]

    if not sr.empty:
        level, action, reason = generate_recommendation(sr.iloc[0])
        confidence = model_confidence(len(gdf))

        # -------------------------------
        # DECISION BANNER
        # -------------------------------
        st.markdown(f"""
        <div style="
            background:#74407F;
            border-left:6px solid #FF6E2E;
            border-radius:10px;
            padding:18px;
            margin-bottom:20px;">
            <h4>🧭 Recommended Administrative Action</h4>
            <p>
            <b>State:</b> {state}<br>
            <b>Risk Level:</b> {level}<br>
            <b>Recommended Intervention:</b> {action}<br>
            <b>Confidence:</b> {confidence}<br>
            <b>Rationale:</b> {reason}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if demo_mode:
            st.info(
                "This recommendation is generated using predicted operational risk "
                "combined with observed Aadhaar activity indicators."
            )

        # -------------------------------
        # RISK METRICS
        # -------------------------------
        r = sr["predicted_risk_score"].iloc[0]
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Predicted Risk Score", f"{r:.3f}")
        m2.metric("Low Intervention Impact", f"{sr['low_intervention'].iloc[0]:.3f}")
        m3.metric("Medium Intervention Impact", f"{sr['medium_intervention'].iloc[0]:.3f}")
        m4.metric("High Intervention Impact", f"{sr['high_intervention'].iloc[0]:.3f}")

    # -------------------------------
    # 🔍 WHY THIS RECOMMENDATION?
    # -------------------------------
    st.markdown("### 🔍 Why this recommendation?")
    st.caption(
        "The following indicators contributed most significantly to the assessed "
        "operational risk for the selected state and time period."
    )

    if gdf.empty:
        st.info("Insufficient activity data available to explain risk drivers.")
    else:
        drivers = (
            gdf[["enrolment", "biometric", "demographic"]]
            .sum()
            .rename({
                "enrolment": "New Enrolments",
                "biometric": "Biometric Corrections",
                "demographic": "Demographic Modifications"
            })
        )

        total = drivers.sum()

        if total == 0:
            st.info("Operational activity levels are minimal during the selected period.")
        else:
            contribution = (drivers / total * 100).round(1)
            st.bar_chart(contribution)

            explanation_df = contribution.reset_index()
            explanation_df.columns = ["Operational Indicator", "Contribution (%)"]

            st.dataframe(
                explanation_df,
                use_container_width=True,
                hide_index=True
            )

            if demo_mode:
                st.caption(
                    "Indicators with higher contribution percentages had greater influence "
                    "on the generated administrative recommendation."
                )

    # -------------------------------
    # ACTIVITY SUMMARY
    # -------------------------------
    st.markdown("### 📦 Aadhaar Activity Summary")
    st.caption(f"Records analysed: {len(gdf)}")

    if not gdf.empty:
        s = gdf[["enrolment", "biometric", "demographic"]].sum()
        a1, a2, a3 = st.columns(3)
        a1.metric("New Enrolments", int(s["enrolment"]))
        a2.metric("Biometric Corrections", int(s["biometric"]))
        a3.metric("Demographic Modifications", int(s["demographic"]))

# ==================================================
# 2️⃣ DISTRICT DRILL-DOWN
# ==================================================
elif view == "District Drill-down":
    st.subheader("District-level Operational Overview")

    if gdf.empty:
        st.warning("No data available.")
    else:
        district = st.selectbox(
            "District",
            sorted(gdf["district"].dropna().unique())
        )
        ddf = gdf[gdf["district"] == district]

        st.dataframe(
            ddf.groupby("district")[["enrolment", "biometric", "demographic"]]
            .sum()
            .reset_index(),
            use_container_width=True
        )

# ==================================================
# 3️⃣ PIN ANALYSIS
# ==================================================
else:
    st.subheader("PIN-level Operational Concentration")

    if gdf.empty:
        st.warning("No data available.")
    else:
        district = st.selectbox(
            "District",
            sorted(gdf["district"].dropna().unique())
        )
        pdf = gdf[gdf["district"] == district]

        pin = (
            pdf.groupby("pincode")[["enrolment", "biometric", "demographic"]]
            .sum()
            .reset_index()
        )
        pin["total_activity"] = pin[["enrolment", "biometric", "demographic"]].sum(axis=1)

        st.dataframe(
            pin.sort_values("total_activity", ascending=False),
            use_container_width=True
        )

# ==================================================
# FOOTER
# ==================================================
st.markdown("""
<hr>
<p style='font-size:12px;color:#6c757d'>
This platform is a decision‑support system. Outputs are indicative and intended for administrative planning.
</p>
""", unsafe_allow_html=True)
