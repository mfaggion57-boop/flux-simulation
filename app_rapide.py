import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import os

# Config page
st.set_page_config(page_title="Comptage Mobilité", layout="wide", page_icon="🚀")

# Style CSS personnalisé
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .stMetric { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Simulation de comptage des flux de mobilité")
st.markdown("---")

# Rafraîchissement automatique toutes les 1 minute
st_autorefresh(interval=60_000, key="refresh")

# Fichier CSV local
LOCAL_CSV = "compteurs.csv"

# Vérifier que le fichier existe
if not os.path.exists(LOCAL_CSV):
    st.warning(f"Le fichier {LOCAL_CSV} n'a pas été trouvé.")
    st.stop()

# Lire le CSV local
df = pd.read_csv(LOCAL_CSV)

# Conversion timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Prendre les 50 dernières lignes
df_recent = df.tail(50)

# Dernières valeurs
last = df_recent.iloc[-1]
previous = df_recent.iloc[-2] if len(df_recent) > 1 else last

# Affichage des métriques
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("👤 Humains", int(last["humains"]), delta=int(last["humains"] - previous["humains"]))
with col2:
    st.metric("🚲 Vélos", int(last["velos"]), delta=int(last["velos"] - previous["velos"]))
with col3:
    st.metric("📊 Total", int(last["humains"] + last["velos"]),
              delta=int((last["humains"] + last["velos"]) - (previous["humains"] + previous["velos"])))

st.markdown("---")
st.subheader("📈 Évolution des flux en temps réel")

# Graphique
fig = px.line(df_recent, x="timestamp", y=["humains", "velos"],
              labels={"value": "Nombre", "timestamp": "Heure", "variable": "Type"},
              color_discrete_map={"humains": "#FF6B6B", "velos": "#4ECDC4"},
              template="plotly_white")

fig.update_layout(hovermode='x unified',
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=""),
                  height=500, margin=dict(l=0, r=0, t=30, b=0))
fig.update_traces(line=dict(width=3))
st.plotly_chart(fig, use_container_width=True)