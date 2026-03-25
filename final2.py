import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Ocean & Fisheries", layout="wide")

st.title("🌊 Ocean Temperature & Fish Populations")
st.write("See how rising ocean temperatures affect fish populations and fishing practices.")

# Sidebar control
st.sidebar.header("Controls")
temp_increase = st.sidebar.slider(
    "Ocean Temperature Increase (°C)",
    min_value=0.0,
    max_value=4.0,
    value=1.5,
    step=0.5
)

# Create a DataFrame for years
years = list(range(2020, 2051))
df = pd.DataFrame({"Year": years})

# Add initial populations
df["Traditional"] = 100000  
df["Adaptive"] = 100000

# Temperature stress factor as a constant value
temp_stress = max(0.3, 1 - (temp_increase * 0.2))

# --- Tradition Method Simulation ---
for i in range(1, len(df)):
    current = df.loc[i-1, "Traditional"]

    growth = current * 0.04 * temp_stress
    fishing_catch = 4500                      # fixed catch

    new_pop = current + growth - fishing_catch
    df.loc[i, "Traditional"] = max(10000, new_pop)

# --- Adaptive Method Simulation ---
for i in range(1, len(df)):
    current = df.loc[i-1, "Adaptive"]

    growth = current * 0.04 * temp_stress
    fishing_catch = 3000 * temp_stress        # catch reduces with warming

    new_pop = current + growth - fishing_catch
    df.loc[i, "Adaptive"] = max(10000, new_pop)

# --- Metrics ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Temperature Increase", f"{temp_increase}°C", "Scenario")

with col2:
    trad_final = df["Traditional"].iloc[-1]
    trad_change = ((trad_final - 100000) / 100000) * 100
    st.metric("Traditional Fishing", f"{trad_final:,.0f} fish", f"{trad_change:+.0f}%")

with col3:
    adapt_final = df["Adaptive"].iloc[-1]
    adapt_change = ((adapt_final - 100000) / 100000) * 100
    st.metric("Adaptive Fishing", f"{adapt_final:,.0f} fish", f"{adapt_change:+.0f}%")

# --- Plotting ---
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Year"],
    y=df["Traditional"],
    name='Traditional Fishing (Fixed Quota)',
    line=dict(color='red', width=3)
))

fig.add_trace(go.Scatter(
    x=df["Year"],
    y=df["Adaptive"],
    name='Adaptive Fishing (Adjusts to Conditions)',
    line=dict(color='green', width=3)
))

fig.update_layout(
    title=f"Fish Population with {temp_increase}°C Ocean Warming",
    xaxis_title="Year",
    yaxis_title="Fish Population",
    height=500,
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Explanation
st.markdown("---")
st.subheader("What This Shows:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🔴 Traditional Fishing**
    - Uses the same fishing amount every year  
    - Does not adjust to temperature changes  
    - Fish population goes down fast  
    """)

with col2:
    st.markdown("""
    **🟢 Adaptive Fishing**
    - Reduces fishing when oceans warm  
    - Helps the fish population survive  
    - More sustainable  
    """)

st.info("💡 Move the slider to see the effect of warming!")
