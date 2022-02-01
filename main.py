import streamlit as st
st.sidebar.title("Tilapia Culture Economics Prophet BI")

st.sidebar.markdown("# Navigations")
nav_page = st.sidebar.selectbox("Navigate Page",["Dashboard","KPIs","CostFactors"],0)


st.sidebar.markdown("# MBBR Type")
mbbr_type = st.sidebar.selectbox("Select build type",["Conventional","Microbeads"],0)
peak_biomass = st.sidebar.slider('Peak Biomass(kg/m3)')


if nav_page == "Dashboard":
    st.write('Selected MBBR Type', mbbr_type)
    st.write('Peak Biomass', peak_biomass,'kg/m3')

if nav_page == "KPIs":
    st.write('not done yet')

if nav_page == "CostFactors":
    tank_costs = st.slider("RAS Tank Costs(TWD/m3)", min_value=0, max_value=1000, value=600)
