from gevent import config
import streamlit as st
import json

st.sidebar.title("Tilapia Culture Economics Prophet BI")
#Sidebar Controls
st.sidebar.markdown("# Navigations")
nav_page = st.sidebar.selectbox("Navigate Page",["Dashboard","KPIs","CostFactors"],0)
st.sidebar.markdown("# MBBR Type")
mbbr_type = st.sidebar.selectbox("Select build type",["Conventional","Microbeads"],0)
peak_biomass = st.sidebar.slider('Peak Biomass(kg/m3)')
#Main Configs






if nav_page == "Dashboard":
    st.write('Selected MBBR Type', mbbr_type)
    st.write('Peak Biomass', peak_biomass,'kg/m3')

if nav_page == "KPIs":
    st.write('not done yet')

if nav_page == "CostFactors":
    tank_costs = st.slider("RAS Tank Costs(TWD/m3)", min_value=0, max_value=1000, value=600)
    microbeads_ssa = st.select_slider('Beads Media SSA',[1280,1800,2500,3500])

    nav_config = {
            "microbeads_ssa": microbeads_ssa, 
            "tank_costs": tank_costs,
    }

    config = json.dumps(nav_config)
    st.write('json test',config)
    with open('json_data.json', 'w') as outfile:
        json.dump(config, outfile)
    
