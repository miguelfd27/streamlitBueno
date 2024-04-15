from datetime import datetime
import streamlit as st
import pandas as pd

st.title('Sales Cars')

def load_data():
    data = pd.read_csv('resources\\car_data.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    return data

data = load_data()

data['year'] = data['Date'].dt.year

#filtros
all_years = sorted(data['year'].unique())
selected_years = st.multiselect('Select Year:', all_years, default=all_years)

all_regions = sorted(data['Dealer_Region'].unique())
selected_regions = st.multiselect('Select Dealer Region:', all_regions, default=all_regions)

filtered_data = data[data['year'].isin(selected_years) & data['Dealer_Region'].isin(selected_regions)]

#datas enseñar
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

if st.checkbox('Show filtered data'):
    st.subheader('Filtered Data')
    st.write(filtered_data)

 
#autos vendidos mes actual
current_month = datetime.now().month 
current_year = datetime.now().year -1

current_month_data = data[(data['Date'].dt.month == current_month) & (data['Date'].dt.year == current_year)]

totalAutomoviles = current_month_data['Car_id'].count()
totalRevenue =current_month_data['Price ($)'].sum()
revenueCOche = totalRevenue/totalAutomoviles

totalRevenueM = totalRevenue / 1_000_000  
FtotalRevenue = f"{totalRevenueM:.2f} M"  


# Obtener los datos del mes anterior
previous_month = current_month - 1
previous_year = current_year
if previous_month == 0:
    previous_month = 12
    previous_year -= 1

previous_month_data = data[(data['Date'].dt.month == previous_month) & (data['Date'].dt.year == previous_year)]

# Calcular los valores del mes anterior
previous_totalAutomoviles = previous_month_data['Car_id'].count()
previous_totalRevenue = previous_month_data['Price ($)'].sum()
previous_revenueCOche = previous_totalRevenue / previous_totalAutomoviles
previous_totalRevenueM = previous_totalRevenue / 1_000_000
previous_FtotalRevenue = f"{previous_totalRevenueM:.2f} M"

# Calcular los porcentajes respecto al mes anterior
autos_porcentaje = ((totalAutomoviles / previous_totalAutomoviles) - 1) * 100
revenue_porcentaje = ((totalRevenue / previous_totalRevenue) - 1) * 100
revenue_por_coche_porcentaje = ((revenueCOche / previous_revenueCOche) - 1) * 100

# Mostrar métricas con porcentaje respecto al mes anterior
st.header("KPI Metrics (vs Mes Anterior)")

# Autos vendidos
st.metric(label="Autos Vendidos", value=totalAutomoviles, delta=f"{autos_porcentaje:.2f}%")

# Revenue
st.metric(label="Revenue", value=f"${totalRevenue:,}", delta=f"{revenue_porcentaje:.2f}%")

# Revenue por coche
st.metric(label="Revenue por Coche", value=f"${FtotalRevenue}", delta=f"{revenue_por_coche_porcentaje:.2f}%")

# company
sales_summary = filtered_data.groupby('Company').agg(
    total_sales=('Price ($)', 'sum'),
    total_cars_sold=('Car_id', 'count')
).reset_index()

sales_summary['revenue_per_car'] = sales_summary['total_sales'] / sales_summary['total_cars_sold']

st.write("Summary by Company:", sales_summary)

#date
aggregated_data = filtered_data.groupby('Date').agg(
    total_cars_sold=('Car_id', 'count'),
    total_revenue=('Price ($)', 'sum')
).reset_index()

aggregated_data['revenue_per_car'] = aggregated_data['total_revenue'] / aggregated_data['total_cars_sold']

option = st.selectbox(
    'Select the metric to display:',
    ('Automóviles vendidos', 'Revenue Total', 'Revenue por coche')
)

if option == 'Automóviles vendidos':
    st.write("Automóviles Vendidos por Fecha")
    chart_data = aggregated_data[['Date', 'total_cars_sold']].set_index('Date')
elif option == 'Revenue Total':
    st.write("Revenue Total por Fecha")
    chart_data = aggregated_data[['Date', 'total_revenue']].set_index('Date')
elif option == 'Revenue por coche':
    st.write("Revenue por Coche por Fecha")
    chart_data = aggregated_data[['Date', 'revenue_per_car']].set_index('Date')

st.line_chart(chart_data)
# marca con mas automoviles vendidos
company = filtered_data.groupby('Company')
ventasCompany = company['Car_id'].count()
CompañiaMax = ventasCompany.idxmax()

# Mostrar métricas
st.header("Métricas de la Compañía con Más Ventas")
st.metric(label="Compañía con más ventas :", value=CompañiaMax)

# Calcular y mostrar autos vendidos y revenue total de la compañía con más ventas
ventas_max = company.get_group(CompañiaMax)
totalAutosMax = ventas_max['Car_id'].count()
totalRevenueMax = ventas_max['Price ($)'].sum()

st.metric(label="Autos Vendidos (Compañía Máx.)", value=totalAutosMax)
st.metric(label="Revenue Total (Compañía Máx.)", value=f"${totalRevenueMax:,.2f}")





