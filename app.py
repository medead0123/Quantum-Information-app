import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from grover_demo import simulate_grover

st.set_page_config(page_title="Q-ALERT Dashboard", layout="wide")

st.title("🌐 Q-ALERT — Quantum Risk Visualization")

st.write("""
This dashboard shows:
1. Comparative crypto performance (RSA, ECC, Kyber)
2. Grover’s algorithm impact
3. Industry Preparedness Index (IPI)
4. Security decay & migration timeline
""")

# Example dataset (later can load benchmarks.csv if you run benchmark_crypto.py)
df = pd.DataFrame({
    "algorithm": ["RSA-2048","ECC-P256","Kyber-512"],
    "keygen": [1.2,0.2,0.4],
    "encrypt": [0.25,0.04,0.06],
    "decrypt": [0.26,0.05,0.07]
})

st.header("1️⃣ Comparative Crypto Performance")
st.dataframe(df)

fig = px.bar(df.melt(id_vars="algorithm"), x="algorithm", y="value",
             color="variable", barmode="group")
st.plotly_chart(fig, use_container_width=True)

st.header("2️⃣ Grover’s Algorithm Impact")
n_qubits = st.slider("Number of qubits", 2, 12, 6)
iters = st.slider("Iterations", 1, 30, 10)
x, probs = simulate_grover(n_qubits, max_iterations=iters)
grover_df = pd.DataFrame({"iteration": x, "success probability": probs})
fig2 = px.line(grover_df, x="iteration", y="success probability", markers=True)
st.plotly_chart(fig2, use_container_width=True)

st.header("3️⃣ Industry Preparedness Index (IPI)")
sectors = ["Banking","Telecom","Defence","Healthcare","Energy","SMEs"]
scores = [0.78,0.45,0.50,0.40,0.55,0.32]
ipi_df = pd.DataFrame({"sector":sectors,"readiness":scores})
fig3 = px.bar(ipi_df, x="sector", y="readiness", color="sector")
st.plotly_chart(fig3, use_container_width=True)

st.header("4️⃣ Security Decay & Migration Timeline")
def security_decay(initial_bits, years, loss):
    t = np.arange(0, years+1)
    return t, np.maximum(initial_bits - loss*t, 0)

years = st.slider("Projection years", 1, 30, 10)
t, rsa_bits = security_decay(112, years, 10)
_, aes_bits = security_decay(128, years, 6)
fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=t, y=rsa_bits, mode="lines+markers", name="RSA-2048"))
fig4.add_trace(go.Scatter(x=t, y=aes_bits, mode="lines+markers", name="AES-128"))
st.plotly_chart(fig4, use_container_width=True)
