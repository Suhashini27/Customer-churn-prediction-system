import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Churn Analytics", layout="wide")

# ---------------- COLORS ----------------
BG = "#0D1117"
CARD = "#161B22"
BORDER = "#21262D"
TEXT = "#E6EDF3"
MUTED = "#8B949E"
BLUE = "#1F6FEB"
RED = "#F85149"
AMBER = "#E3B341"
GREEN = "#3FB950"
ORANGE = "#F0883E"

API = "http://localhost:8001"

# ---------------- CSS ----------------
st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
background:{BG};
color:{TEXT};
}}
[data-testid="stHeader"] {{
background:{BG};
}}
.block-container {{
padding-top:1rem;
max-width:100%;
}}
.card {{
background:{CARD};
border:1px solid {BORDER};
border-radius:4px;
padding:14px;
}}
.small {{
font-size:11px;
color:{MUTED};
}}
.metric {{
font-size:26px;
font-weight:600;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown(f"""
<div class="card" style="height:44px;display:flex;justify-content:space-between;align-items:center;">
<div style="font-weight:600;">Churn Analytics</div>
<div class="small">Connected to localhost:8001</div>
</div>
""", unsafe_allow_html=True)

# ---------------- API HEALTH ----------------
try:
    health = requests.get(f"{API}/health").json()
    st.success("Backend Connected Successfully")
except:
    st.error("Backend not running. Start api.py first.")
    st.stop()

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.header("Customer Inputs")

customer_id = st.sidebar.text_input("Customer ID", "USR-1001")
billing_amount = st.sidebar.number_input("Billing Amount", 100.0)
last_payment_days_ago = st.sidebar.number_input("Last Payment Days Ago", 5)
tenure_months = st.sidebar.number_input("Tenure Months", 12)
monthly_usage_hours = st.sidebar.number_input("Usage Hours", 40.0)
active_days = st.sidebar.number_input("Active Days", 20)
login_count = st.sidebar.number_input("Login Count", 10)
avg_session_min = st.sidebar.number_input("Avg Session Minutes", 35.0)
device_count = st.sidebar.number_input("Device Count", 2)
add_on_count = st.sidebar.number_input("Add On Count", 1)
support_tickets = st.sidebar.number_input("Support Tickets", 0)
sla_breaches = st.sidebar.number_input("SLA Breaches", 0)
promotions_redeemed = st.sidebar.number_input("Promotions Redeemed", 1)
email_opens = st.sidebar.number_input("Email Opens", 5)
email_clicks = st.sidebar.number_input("Email Clicks", 2)
last_campaign_days_ago = st.sidebar.number_input("Campaign Days Ago", 10)
nps_score = st.sidebar.slider("NPS Score", 0, 10, 8)

plan_tier = st.sidebar.selectbox("Plan Tier", ["Basic", "Standard", "Premium", "Enterprise"])
region = st.sidebar.selectbox("Region", ["North", "South", "East", "West"])

is_autopay = st.sidebar.selectbox("Autopay", [1,0])
is_discounted = st.sidebar.selectbox("Discounted", [1,0])
has_family_bundle = st.sidebar.selectbox("Family Bundle", [1,0])

# ---------------- PAYLOAD ----------------
payload = {
    "customer_id": customer_id,
    "cycle_start": "2026-01-01T00:00:00",
    "cycle_end": "2026-01-31T00:00:00",
    "billing_amount": billing_amount,
    "last_payment_days_ago": last_payment_days_ago,
    "plan_tier": plan_tier,
    "tenure_months": tenure_months,
    "monthly_usage_hours": monthly_usage_hours,
    "active_days": active_days,
    "login_count": login_count,
    "avg_session_min": avg_session_min,
    "device_count": device_count,
    "add_on_count": add_on_count,
    "support_tickets": support_tickets,
    "sla_breaches": sla_breaches,
    "promotions_redeemed": promotions_redeemed,
    "email_opens": email_opens,
    "email_clicks": email_clicks,
    "last_campaign_days_ago": last_campaign_days_ago,
    "nps_score": nps_score,
    "region": region,
    "is_autopay": is_autopay,
    "is_discounted": is_discounted,
    "has_family_bundle": has_family_bundle
}

# ---------------- BUTTON ----------------
if st.sidebar.button("Predict Churn"):

    score = requests.post(f"{API}/score", json=payload).json()
    explain = requests.post(f"{API}/explain", json=payload).json()

    churn = score["churn_prob"]
    segment = score["segment"]

    # ---------- KPI ----------
    a,b,c = st.columns(3)

    with a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="small">CUSTOMER ID</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric">{customer_id}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="small">CHURN PROBABILITY</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric">{churn:.2%}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c:
        color = GREEN if segment=="Low" else AMBER if segment=="Medium" else RED
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="small">RISK SEGMENT</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric" style="color:{color};">{segment}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # ---------- GAUGE ----------
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=churn*100,
        number={'suffix':"%"},
        gauge={
            'axis': {'range':[0,100]},
            'bar': {'color': BLUE},
            'steps':[
                {'range':[0,25],'color':GREEN},
                {'range':[25,50],'color':AMBER},
                {'range':[50,75],'color':ORANGE},
                {'range':[75,100],'color':RED},
            ]
        }
    ))

    fig.update_layout(
        paper_bgcolor=CARD,
        font_color=TEXT,
        height=300
    )

    left,right = st.columns([1,1])

    with left:
        st.plotly_chart(fig, use_container_width=True)

    # ---------- SHAP ----------
    with right:
        df = pd.DataFrame(explain["top_features"])
        fig2 = px.bar(
            df,
            x="impact",
            y="feature",
            orientation="h",
            color="impact",
            color_continuous_scale="Bluered"
        )
        fig2.update_layout(
            paper_bgcolor=CARD,
            plot_bgcolor=CARD,
            font_color=TEXT,
            height=300,
            title="Top Churn Drivers"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ---------- TREND ----------
    st.write("")
    st.markdown("### Historical Churn Trend")

    trend = pd.DataFrame({
        "Month":["Jan","Feb","Mar","Apr","May","Jun"],
        "Rate":[12.4,11.2,10.8,9.7,8.4,8.9]
    })

    fig3 = px.line(trend, x="Month", y="Rate", markers=True)
    fig3.update_layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font_color=TEXT,
        height=300
    )

    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Enter customer details in sidebar and click Predict Churn")