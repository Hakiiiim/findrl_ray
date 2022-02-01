from cmath import pi
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
    with open('config.json') as json_file:
        config_data = json.load(json_file)
    st.write('config file data',config_data)
    st.write('microbeads ssa',config_data['microbeads_ssa'])
    st.write('Selected MBBR Type', mbbr_type)
    st.write('Peak Biomass', peak_biomass,'kg/m3')

if nav_page == "KPIs":
    st.write('not done yet')

if nav_page == "CostFactors":
    tank_costs = st.slider("RAS Tank Costs(TWD/m3)", min_value=0, max_value=1000, value=600)
    microbeads_ssa = st.select_slider('Beads Media SSA',[1280,1800,2500,3500])
    tank_depth = st.slider("Tank Culture Depth(m)",min_value=1.0,max_value=1.5, step=0.1, value=1.2)
    tank_diameter = st.slider("Tank Diameter",min_value=6.0,max_value=9.0,step=1.0, value=6.0)
    tank_area = ((float(tank_diameter)*0.5)^2)*3.1415
    tank_volume = tank_area*tank_depth
    static_o2_consumptions = st.slider()


    nav_config = {
            "microbeads_ssa": microbeads_ssa, 
            "tank_costs": tank_costs,
            "tank_depth":tank_depth,
            "tank_diameter":tank_diameter,
            "tank_area":tank_area,
            "tank_volume":tank_volume,
            "static_o2_consumptions":static_o2_consumptions,

    }

    with open('config.json', 'w') as outfile:
        json.dump(nav_config, outfile)
    
