from cmath import pi
import streamlit as st
import json
import pandas as pd
st.set_page_config(layout="wide")

col1, col2, col3, col4 = st.columns([1.1,1,2.3,0.85])
st.sidebar.title("Tilapia Culture Economics Prophet BI")
#Sidebar Controls
st.sidebar.markdown("# SiteSpecs")
total_water = st.sidebar.slider('Input Site Total m3',value=3000,min_value=500,max_value=6000,step=100)
st.sidebar.markdown("# MBBR Type")
mbbr_type = st.sidebar.selectbox('MBBR Type',('conventional','microbeads'))
#Main Configs
with col1:
    st.header('Configs')
    with st.expander('HardwareConfigs',expanded=True):
        microbeads_ssa = st.select_slider('Beads Media SSA',[1280,1800,2500,3500],value=2500)
        conventional_ssa = st.select_slider('Conventional K type filter SSA',[500,600,700,800,900,1000,1100,1200],value=800)
        tank_depth = st.slider("Tank Culture Depth(m)",min_value=1.0,max_value=1.5, step=0.1, value=1.2)
        tank_diameter = st.slider("Tank Diameter",min_value=6.0,max_value=9.0,step=1.0, value=6.0)
        static_o2_consumptions = st.slider('O2 Consumption(mg/hr) / kg biomass',min_value=200,max_value=800,step=50,value=550)
        tan_removal_rate = st.slider('TAN Removal Rate:',min_value=0.1,max_value=0.5,value=0.25)   
    with st.expander('BioInputs',expanded=False):
        start_weight = st.number_input('Fingerling Weight(g)',value=5)
        harvest_weight = st.slider('Harvest Weight(g)',min_value=500,max_value=1200,step=50)
        fcr = st.slider('FCR:',min_value=1.3,step=0.05,max_value=2.0,value=1.50)


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
        stage_5_abw = st.number_input('Stage 5 ExitABW:',value=harvest_weight)
    #Densities Per Stage   
    with st.expander('Densities Per Stage',expanded=False):
        stage_1_den = st.slider('Stage 1 Densities',min_value=500,max_value=1600,step=100,value=1000)
        stage_2_den = st.slider('Stage 2 Densities',min_value=200,max_value=800,step=50,value=450)
        stage_3_den = st.slider('Stage 3 Densities',min_value=80,max_value=400,step=25,value=125)
        stage_4_den = st.slider('Stage 4 Densities',min_value=50,max_value=250,step=25,value=100)
        stage_5_den = st.slider('Stage 5 Densities',min_value=20,max_value=150,step=10,value=60)
    #Feeding % each stage
    with st.expander('每階段攝食率（百分比）',expanded=False):
        stage_1_feedrat = st.slider('1階攝食率',min_value=5.0,max_value=10.0,step=0.5,value=6.00)
        stage_2_feedrat = st.slider('2階攝食率',min_value=3.0,max_value=7.0,step=0.5,value=4.00)
        stage_3_feedrat = st.slider('3階攝食率',min_value=2.0,max_value=3.0,step=0.5,value=1.50)
        stage_4_feedrat = st.slider('4階攝食率',min_value=1.0,max_value=2.0,step=0.1,value=1.25)
        stage_5_feedrat = st.slider('5階攝食率',min_value=1.0,max_value=2.0,step=0.1,value=1.00)
     #Feeding % each stage
    with st.expander('每階段餌料蛋白質）',expanded=False):
        stage_1_feed_cp = st.slider('1階餌料蛋白質',min_value=28.0,max_value=35.0,step=1.0,value=35.0)
        stage_2_feed_cp = st.slider('2階餌料蛋白質',min_value=25.0,max_value=35.0,step=1.0,value=28.0)
        stage_3_feed_cp = st.slider('3階餌料蛋白質',min_value=20.0,max_value=32.0,step=0.5,value=25.0)
        stage_4_feed_cp = st.slider('4階餌料蛋白質',min_value=20.0,max_value=28.0,step=0.1,value=25.0)
        stage_5_feed_cp = st.slider('5階餌料蛋白質',min_value=20.0,max_value=28.0,step=0.1,value=25.0)
    #Not expanded stage mortalities
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
    x = stage_1_den * (stage_1_abw/1000) 
    return x
def stage_2_biomass():
    x = stage_2_den*stage_2_abw/1000
    return x
def stage_3_biomass():
    x = stage_3_den*stage_3_abw/1000
    return x
def stage_4_biomass():
    x = stage_4_den*stage_4_abw/1000
    return x
def stage_5_biomass():
    x = stage_5_den*stage_5_abw/1000
    return x

def volume_coefficent():
    x = (stage_5_den/stage_1_den) + (stage_5_den/stage_2_den) + (stage_5_den/stage_3_den) + (stage_5_den/stage_4_den) + 1
    return x

def tank_1_amount():
   x = round(((stage_5_den/stage_1_den) / volume_coefficent() * total_water) / tank_volume_fn(),0)+1
   return x
def tank_1_volume():
   x = round(((stage_5_den/stage_1_den) / volume_coefficent() * total_water),3)
   return x
def tank_2_amount():
   x = round(((stage_5_den/stage_2_den) / volume_coefficent()* total_water) / tank_volume_fn(),0)+1
   return x
def tank_2_volume():
   x = round(((stage_5_den/stage_2_den) / volume_coefficent() * total_water),3)
   return x 
def tank_3_amount():
   x = round(((stage_5_den/stage_3_den) / volume_coefficent()* total_water) / tank_volume_fn(),0)+1
   return x
def tank_3_volume():
   x = round(((stage_5_den/stage_3_den) / volume_coefficent() * total_water),3)
   return x
def tank_4_amount():
   x = round(((stage_5_den/stage_4_den) / volume_coefficent()* total_water) / tank_volume_fn(),0)+1
   return x
def tank_4_volume():
   x = round(((stage_5_den/stage_4_den) / volume_coefficent() * total_water),3)
   return x
def tank_5_amount():
   x = round(((stage_5_den/stage_5_den) / volume_coefficent()* total_water) / tank_volume_fn(),0)+1
   return x
def tank_5_volume():
   x = round(((1 / volume_coefficent()) * total_water),3)
   return x
def real_capacity():
    x = (tank_1_amount()+tank_2_amount()+tank_3_amount()+tank_4_amount()+tank_5_amount())*tank_volume_fn()
    return x

def stage_1_tan():
    x = tank_1_volume() * stage_1_biomass() * stage_1_feed_cp/100 * 0.16 * 0.3 * 1.2 * stage_1_feedrat/100
    return x
def stage_2_tan():
    x = tank_2_volume() * stage_2_biomass() * stage_2_feed_cp/100 * 0.16 * 0.3 * 1.2 * stage_2_feedrat/100
    return x
def stage_3_tan():
    x = tank_3_volume() * stage_3_biomass() * stage_3_feed_cp/100 * 0.16 * 0.3 * 1.2 * stage_3_feedrat/100
    return x
def stage_4_tan():
    x = tank_4_volume() * stage_4_biomass() * stage_4_feed_cp/100 * 0.16 * 0.3 * 1.2 * stage_4_feedrat/100
    return x
def stage_5_tan():
    x = tank_5_volume() * stage_5_biomass() * stage_5_feed_cp/100 * 0.16 * 0.3 * 1.2 * stage_5_feedrat/100
    return x
def total_tan():
    x = stage_1_tan() + stage_2_tan() + stage_3_tan() + stage_4_tan() + stage_5_tan()
    return x
def hypo_ssa():
    x = round(total_tan()*1000/tan_removal_rate,0)
    return x
def biofilter_volume():
    x = hypo_ssa()/microbeads_ssa
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
        st.write('Stage 1 Peak Biomass: {0: .3f}(kg/m3)'.format(stage_1_biomass()))
        st.write('Stage 2 Peak Biomass: {0: .3f}(kg/m3)'.format(stage_2_biomass()))
        st.write('Stage 3 Peak Biomass: {0: .3f}(kg/m3)'.format(stage_3_biomass()))
        st.write('Stage 4 Peak Biomass: {0: .3f}(kg/m3)'.format(stage_4_biomass()))
        st.write('Stage 5 Peak Biomass: {0: .3f}(kg/m3)'.format(stage_5_biomass()))
    totaltan = st.write('Total TAN: kg/day',total_tan())
    hypothetical_ssa = st.write('理論需求表面積(m2)',hypo_ssa())
    microbeadsamount = st.write('保麗龍球體積:(m3)',biofilter_volume())  





with col3:
    st.header('Charts Tables')
    st.write('test space')

with col4:
    st.header('Costs Input Variables')
    with st.expander('HardwareInvestments',expanded=True):
        tank_costs = st.slider("RAS Tank Costs(TWD/m3)", min_value=0, max_value=1000, value=600,step=25)
     

st.empty()
with st.container():
    st.header('投資指標評估') 
st.expander('投資指標評估',expanded=True)
tank_invest = st.write('槽體工程投資金額:',round(tank_costs*real_capacity(),0))


con_col = st.columns([2,1,2])

with con_col[0]:
    st.header('每階段水池設計配比')
    st.write('Stage 1 tanks',tank_1_amount())
    st.write ('1階水體量(m3):',tank_1_volume())
    st.write('Stage 2 tanks',tank_2_amount())
    st.write ('2階水體量(m3):',tank_2_volume())
    st.write('Stage 3 tanks',tank_3_amount())
    st.write ('3階水體量(m3):',tank_3_volume())
    st.write('Stage 4 tanks',tank_4_amount())
    st.write ('4階水體量(m3):',tank_4_volume())
    st.write('Stage 5 tanks',tank_5_amount())
    st.write ('5階水體量(m3):',tank_5_volume())
    st.write('Total Tanks',tank_1_amount()+tank_2_amount()+tank_3_amount()+tank_4_amount()+tank_5_amount())
    st.write('項目總裝置噸位（m3)',real_capacity())
with con_col[2]:
    st.header('虛位以待')