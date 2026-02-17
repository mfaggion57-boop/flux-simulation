import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import os

# Config page
st.set_page_config(page_title="Comptage Mobilité", layout="wide", page_icon="🚀")

st.title("🚀 Simulation de comptage des flux de mobilité")
st.markdown("---")

# Rafraîchissement automatique toutes les 1 minute
st_autorefresh(interval=60_000, key="refresh")

LOCAL_CSV = "compteurs.csv"

if not os.path.exists(LOCAL_CSV):
    st.warning(f"Le fichier {LOCAL_CSV} n'a pas été trouvé.")
    st.stop()

df = pd.read_csv(LOCAL_CSV)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df_recent = df.tail(50)

last = df_recent.iloc[-1]
previous = df_recent.iloc[-2] if len(df_recent) > 1 else last

# -----------------------------
# Métriques EN HAUT
# -----------------------------
col1, spacer1, col2, spacer2, col3 = st.columns([1, 0.2, 1, 0.2, 1])

with col1:
    st.metric(
        label="🚶 Piétons",
        value=int(last["humains"]),
        delta=int(last["humains"] - previous["humains"])
    )

with col2:
    st.metric(
        label="🚲 Vélos",
        value=int(last["velos"]),
        delta=int(last["velos"] - previous["velos"])
    )

with col3:
    st.metric(
        label="📊 Total",
        value=int(last["humains"] + last["velos"]),
        delta=int((last["humains"] + last["velos"]) - (previous["humains"] + previous["velos"]))
    )

# -----------------------------
# Graphique
# -----------------------------
st.subheader("📈 Évolution des flux en temps réel")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_recent["timestamp"],
    y=df_recent["humains"],
    mode="lines",
    name="humains",
    line=dict(color="#FF6B6B", width=3),
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=df_recent["timestamp"],
    y=df_recent["velos"],
    mode="lines",
    name="velos",
    line=dict(color="#4ECDC4", width=3),
    showlegend=False
))

fig.update_layout(
    hovermode="x unified",
    template="plotly_white",
    height=450,
    margin=dict(l=0, r=0, t=30, b=10),
    xaxis_title="Heure",
    yaxis_title="Nombre",
)

st.plotly_chart(fig, use_container_width=True)

# Légende HTML sous le graphique
st.markdown(
    """
    <div style="display:flex; justify-content:center; align-items:center; gap:40px; margin-top:-20px; margin-bottom:24px;">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:36px; height:4px; background:#FF6B6B; border-radius:2px;"></div>
            <span style="font-size:15px; color:#ccc;">humains</span>
        </div>
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:36px; height:4px; background:#4ECDC4; border-radius:2px;"></div>
            <span style="font-size:15px; color:#ccc;">velos</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
previous["humains"] + previous["velos"]))
    


