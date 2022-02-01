from cmath import pi
from re import L, X
from sqlalchemy import true
import streamlit as st
import json
import pandas as pd
from sympy import expand 
st.set_page_config(layout="wide")

col1, col2, col3, col4 = st.columns([1.1,1,2.3,0.85])

st.sidebar.title("Tilapia Culture Economics Prophet BI")
#Sidebar Controls
st.sidebar.markdown("# SiteSpecs")
total_water = st.sidebar.number_input('Input Site Total m3',value=3000,min_value=500,max_value=6000)
st.sidebar.markdown("# MBBR Type")
mbbr_type = st.sidebar.selectbox('MBBR Type',('conventional','microbeads'))
#Main Configs
with col1:
    st.header('Configs')
    with st.expander('HardwarConfigs',expanded=True):
        microbeads_ssa = st.select_slider('Beads Media SSA',[1280,1800,2500,3500])
        conventional_ssa = st.select_slider('Conventional K type filter SSA',[500,600,700,800,900,1000,1100,1200],value=800)
        tank_depth = st.slider("Tank Culture Depth(m)",min_value=1.0,max_value=1.5, step=0.1, value=1.2)
        tank_diameter = st.slider("Tank Diameter",min_value=6.0,max_value=9.0,step=1.0, value=6.0)
        static_o2_consumptions = st.slider('O2 Consumption(mg/hr) / kg biomass',min_value=200,max_value=800,step=50,value=550)
    with st.expander('BioInputs',expanded=False):
        start_weight = st.number_input('Fingerling Weight(g)',value=5)
        harvest_weight = st.slider('Harvest Weight(g)',min_value=500,max_value=1200,step=50)
    #Not expanded stage DOCs
    with st.expander('DOCs/Stage Inputs', expanded=False):
        stage_1_days = st.number_input('Stage 1 days:',value=60)
        stage_2_days = st.number_input('Stage 2 days:',value=60)
        stage_3_days = st.number_input('Stage 3 days:',value=60)
        stage_4_days = st.number_input('Stage 4 days:',value=60)
        stage_5_days = st.number_input('Stage 5 days:',value=60)
    #Not expanded Exit Weights
    with st.expander('ExitABW Inputs', expanded=False):
        stage_1_abw = st.number_input('Stage 1 ExitABW:',value=50)
        stage_2_abw = st.number_input('Stage 2 ExitABW:',value=150)
        stage_3_abw = st.number_input('Stage 3 ExitABW:',value=350)
        stage_4_abw = st.number_input('Stage 4 ExitABW:',value=600)
        stage_5_abw = st.number_input('Stage 5 ExitABW:',value=1000)
    #Densities Per Stage   
    with st.expander('Densities Per Stage',expanded=False):
        stage_1_den = st.slider('Stage 1 Densities',min_value=500,max_value=1600,step=100,value=1000)
        stage_2_den = st.slider('Stage 2 Densities',min_value=200,max_value=800,step=50,value=500)
        stage_3_den = st.slider('Stage 3 Densities',min_value=80,max_value=400,step=25,value=150)
        stage_4_den = st.slider('Stage 4 Densities',min_value=50,max_value=250,step=25,value=100)
        stage_5_den = st.slider('Stage 5 Densities',min_value=20,max_value=150,step=10,value=60)
    #Not expanded stage mortalitiess
    with st.expander('Mortalities Each Stage', expanded=False):
        stage_1_mort = st.number_input('Stage 1 Mortalities: (%)',value=3)
        stage_2_mort = st.number_input('Stage 2 Mortalities: (%)',value=2)
        stage_3_mort = st.number_input('Stage 3 Mortalities: (%)',value=1.5)
        stage_4_mort = st.number_input('Stage 4 Mortalities: (%)',value=1)
        stage_5_mort = st.number_input('Stage 5 Mortalities: (%)',value=1)

def tank_volume_fn():
    x = round(tank_depth *float(tank_diameter*0.5)*float(tank_diameter*0.5)*3.1415,3)
    return x
def tank_number_fn():
    x = round(total_water/tank_volume_fn(),0)+1
    return x
def stage_1_adg():
    x =(stage_1_abw-start_weight)/stage_1_days
    return x
def stage_2_adg():
    x =(stage_2_abw-stage_1_abw)/stage_2_days
    return x
def stage_3_adg():
    x =(stage_3_abw-stage_2_abw)/stage_3_days
    return x
def stage_4_adg():
    x =(stage_4_abw-stage_3_abw)/stage_4_days
    return x
def stage_5_adg():
    x =(harvest_weight-stage_4_abw)/stage_5_days
    return x
def stage_1_biomass():
    x = ((stage_1_den*stage_1_abw)/1000)
    return x
def stage_2_biomass():
    x = stage_2_den*stage_2_abw*(100-stage_2_mort)/1000
    return x
def stage_3_biomass():
    x = stage_3_den*stage_3_abw*(100-stage_3_mort)/1000
    return x
def stage_1_biomass():
    x = stage_4_den*stage_4_abw*(100-stage_4_mort)/1000
    return x
def stage_1_biomass():
    x = stage_5_den*stage_5_abw*(100-stage_5_mort)/1000
    return x

with col2:
    st.header('KPIs')
    peak_biomass = st.sidebar.slider('Peak Biomass(kg/m3)')
    tank_area = st.write('Tank Area Footprint:',round(float(tank_diameter*0.5)*float(tank_diameter*0.5)*3.1415,3))
    tank_volume = st.write('Tank Volume(m3)',tank_volume_fn())
    tank_number = st.write('Number of Tanks:',tank_number_fn())
    with st.expander('ADG',expanded=False):
        st.write('Stage 1 ADG: {0: .3f}(g/day)'.format(stage_1_adg()))
        st.write('Stage 2 ADG: {0: .3f}(g/day)'.format(stage_2_adg()))
        st.write('Stage 3 ADG: {0: .3f}(g/day)'.format(stage_3_adg()))
        st.write('Stage 4 ADG: {0: .3f}(g/day)'.format(stage_4_adg()))
        st.write('Stage 5 ADG: {0: .3f}(g/day)'.format(stage_5_adg()))
    with st.expander('Biomass Per Stage',expanded=False):
        st.write('Stage 1 Peak Biomass: {0: .2f}(kg/m3)'.format(stage_1_biomass()))





with col3:
    st.header('Charts Tables')
    st.write('test space')

with col4:
    st.header('Investment Remarks')


with st.expander('Costs Input Variables',expanded=True):    
    tank_costs = st.slider("RAS Tank Costs(TWD/m3)", min_value=0, max_value=1000, value=600)

st.empty()
st.write('Further Remarks')