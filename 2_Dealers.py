import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

def number_to_month(numero_mes):
    d=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto',
       'Septiembre','Octubre','Noviembre','Diciembre']
    return d[numero_mes - 1]
#calcula en nivel de ingreso dado el ingreso anual
def ingreso_anual(data):
    if (data > 1000000):
        return "Muy Alto"
    elif (data > 750000):
        return "Alto"
    elif (data > 500000):
        return "Medio-Alto"
    elif (data > 250000):
        return "Medio"
    elif (data > 100000):
        return "Medio-Bajo"
    return "Bajo"

#crea una gráfica circular de porciones
def pie_chart(data,agrupacion,agrupar,tam,colores):
    agrupacion_parcial = data.groupby(agrupacion)[agrupar].sum()
    agrupacion_total = data[agrupar].sum()
    etiquetas = agrupacion_parcial.index.to_list()

    tam_porciones = []
    for i in etiquetas:
        tam_porciones.append(agrupacion_parcial[i]/agrupacion_total)

    #creacion del gráfico circular
    fig1, ax1 = plt.subplots(figsize=(tam[0],tam[1]))
    ax1.pie(tam_porciones, labels = etiquetas,radius = 0.2, autopct="%1.1f%%", startangle= 90, colors = colores)
    ax1.axis('equal')
    return fig1

@st.cache_data
#cargamos datos del csv
def load_data():
    data = pd.read_csv("c:\\users\\mrboo.indra\\miproyecto\\resources\\car_data.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['M/Y'] = data['Month'].map(number_to_month) + " " + data['Year'].map(str)
    data["Ingreso Anual"] = data["Annual Income"].apply(lambda x: ingreso_anual(x))
    data = data.sort_values(by=['Year','Month'])
    return data

#funcion para desplegar los kpis
def display_kpi_metrics(kpis: List[float], kpi_names: List[str], delta):
    st.header("KPI Metrics")
    for i, (col, (kpi_name, kpi_value)) in enumerate(zip(st.columns(3), zip(kpi_names, kpis))):
        col.metric(label=kpi_name, value=kpi_value, delta=delta[i])

def car_sold(data, year, month):
    data_y = data[data['Year'] == (data['Year'].max() - year)]
    data_m = data_y[data['Month'] == (data['Month'].max() - month)]
    data_d = data_m[data['Dealer_Name'] == dealer]
    return data_d

def porcentage_relationship(value1, value2, decimals):
    total = ((value1 / value2) - 1) * 100
    if(decimals != -1):
        total = round(total,decimals)
    return total

#establece la página a ventana completa
st.set_page_config(layout="wide")
st.title('Dealers')
data = load_data()
columnas = data.columns.values
container = st.container(border=True)
dealer = st.selectbox('Select Dealer:', data['Dealer_Name'].unique())
num_dealers = len(data['Dealer_Name'].unique())

##creación de las metricas/KPIs
car_actual_month = car_sold(data,0,0)
car_previous_month = car_sold(data,0,1)

#automóviles vendidos mes actual y mes previo - KPI1
autos_vendidos_actual = car_actual_month['Car_id'].count()
autos_vendidos_previous = car_previous_month['Car_id'].count()
autos_vendidos_total = int(autos_vendidos_actual - autos_vendidos_previous)

#revenue obtenido el mes actual y el mes anterior - KP2
autos_revenue_actual = car_actual_month['Price ($)'].sum()
autos_revenue_previous = car_previous_month['Price ($)'].sum()
autos_revenue_total = int(autos_revenue_actual - autos_revenue_previous)

#revenue promedio obtenido por coche el mes actual y el mes anterior - KPI3
revenue_por_coche_actual = autos_revenue_actual / autos_vendidos_actual
revenue_por_coche_previous = autos_revenue_previous / autos_vendidos_previous
revenue_por_coche_total = float(round(revenue_por_coche_actual - revenue_por_coche_previous,2))

#porcentajes de las 3 metricas
porcentaje = porcentage_relationship(autos_vendidos_actual,autos_vendidos_previous,2)
porcentaje2 = porcentage_relationship(autos_revenue_actual,autos_revenue_previous,2)
porcentaje3 = porcentage_relationship(revenue_por_coche_actual, revenue_por_coche_previous,2)

#Se muestran los KPIs
kpi_names = ["Autos vendidos","Revenue","Revenue por coche"]
kpis = [porcentaje, porcentaje2, porcentaje3]
deltas = [autos_vendidos_total, autos_revenue_total, revenue_por_coche_total]
display_kpi_metrics(kpis, kpi_names, deltas)

data_dealer = data[data['Dealer_Name'] == dealer]

data_clients = data_dealer.groupby(['M/Y']).Phone.nunique()
st.bar_chart(data_clients, color="#000000")

data_vehiculos = data_dealer.groupby(['M/Y']).Car_id.count()
data_vehiculos_total = data.groupby(['M/Y']).Car_id.count() / num_dealers

#para poder mostrar las 2 líneas en la gráfica
data_vehiculos_total.name= "Promedio de ventas"
data_vehiculos.name = "Ventas de " + dealer 
lista_data = pd.concat([data_vehiculos,data_vehiculos_total], axis=1)
st.line_chart(lista_data, color=["#E1C233","#000000"])
#barra = st.slider(label="",value=data_clients.index)

autos = pd.Series.to_frame(data_dealer.groupby('Company')['Price ($)'].sum())
top_5_autos = autos.nlargest(5,'Price ($)')

row = st.columns(3)
colores = ["#000000","#E1C233","#1FC2C2","#A666B0","#573B92","#666666"]
colores2 = ["#000000","#E1C233"]
graf1 = pie_chart(data_dealer,'Ingreso Anual','Price ($)',[5,5], colores)
graf2 = pie_chart(data_dealer,'Gender','Price ($)',[6,5],colores2)
lista = [graf1,graf2,top_5_autos]

i = 0
for col in row:
    tile = col.container(height=350, border=False)
    if( i== 2):
        tile.bar_chart(lista[i], color="#000000")
    else:
        tile.pyplot(lista[i])
    i+=1
