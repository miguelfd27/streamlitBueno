from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


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

def bar_chart(data, group_by):
    fig, ax = plt.subplots(figsize=(10, 6)) 
    grouped_data = data.groupby(group_by).size().sort_values(ascending=True)
    grouped_data.plot(kind='barh', ax=ax)
    ax.set_xlabel(group_by)
    ax.set_ylabel('Number of Cars Sold')
    ax.set_title('Cars Sold by Model')
    plt.xticks(rotation=45)
    return fig

def treemap(data, group_by):
    fig = px.treemap(data, path=[group_by], values=data.index, color=data.index)
    return fig

# PieChart
def pie_chart(data, group_by):
    fig, ax = plt.subplots(figsize=(2, 2)) 
    grouped_data = data.groupby(group_by).size()
    ax.pie(grouped_data , labels=grouped_data.index, autopct='%1.1f%%', startangle=90,textprops={'fontsize': 7})
    ax.axis('equal')  
    return fig

st.title('Company Cars')


def load_data():
    data = pd.read_csv('C:\\Users\\mfdourado.INDRA\\Documents\\PBI\\COCHES\\Car Sales.xlsx - car_data.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data["Ingreso Anual"] = data["Annual Income"].apply(lambda x: ingreso_anual(x))
    return data

data = load_data()


#filtros
all_marcas = sorted(data['Company'].unique())
selected_Company = st.selectbox('Select Year:', all_marcas)

filtered_data = data[data['Company'] == selected_Company]



# Mes Actual
current_month = datetime.now().month 
current_year = datetime.now().year - 1

current_month_data = data[(data['Month'] == current_month) & (data['Year'] == current_year) & (data['Company'] == selected_Company)]

totalAutomoviles_current = current_month_data['Car_id'].count()
totalRevenue_current = current_month_data['Price ($)'].sum()
revenueCoche_current = totalRevenue_current / totalAutomoviles_current

# Mes Previous
previous_month = current_month - 1
previous_year = current_year
if previous_month == 0:
    previous_month = 12
    previous_year -= 1

previous_month_data = data[(data['Month'] == previous_month) & (data['Year'] == previous_year) & (data['Company'] == selected_Company)]

totalAutomoviles_previous = previous_month_data['Car_id'].count()
totalRevenue_previous = previous_month_data['Price ($)'].sum()
revenueCoche_previous = totalRevenue_previous / totalAutomoviles_previous


autos_porcentaje = ((totalAutomoviles_current / totalAutomoviles_previous) - 1) * 100
revenue_porcentaje = ((totalRevenue_current / totalRevenue_previous) - 1) * 100
revenue_por_coche_porcentaje = ((revenueCoche_current / revenueCoche_previous) - 1) * 100

# Metrics
st.header(f"KPI Metrics for {selected_Company} (vs Previous Month)")

row = st.columns(3)

# Autos vendidos
with row[0]:
    st.metric(label="Autos Vendidos", value=totalAutomoviles_current, delta=f"{autos_porcentaje:.2f}%")

# Revenue
with row[1]:
    st.metric(label="Revenue", value=f"${totalRevenue_current:,}", delta=f"{revenue_porcentaje:.2f}%")

# Revenue por coche
with row[2]:
    st.metric(label="Revenue por Coche", value=f"${revenueCoche_current:.2f}", delta=f"{revenue_por_coche_porcentaje:.2f}%")



# Pie Chart
st.header(f"Pie Chart by {'Ingreso Anual'}")
fig = pie_chart(filtered_data, 'Ingreso Anual')
st.pyplot(fig)

st.header(f"Pie Chart by {'Engine'}")
fig = pie_chart(filtered_data, 'Engine')
st.pyplot(fig)

st.header(f"Pie Chart by {'Dealer_Region'}")
fig = pie_chart(filtered_data, 'Dealer_Region')
st.pyplot(fig)

st.header(f"Pie Chart by {'Color'}")
fig = pie_chart(filtered_data, 'Color')
st.pyplot(fig)

st.header("Cars Sold by Model")
fig = bar_chart(filtered_data, 'Model')
st.pyplot(fig)



#treemap
st.header("Sales by Design (Treemap)")
fig = treemap(filtered_data, 'Body Style')
st.plotly_chart(fig)
