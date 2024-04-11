import plotly.express as px
import pandas as pd

def pie_chart_figura(data, agrupacion, agrupar,colores, tam, leyenda,funcion):
    if funcion == "suma":
        agrupado = pd.Series.to_frame(data.groupby(agrupacion)[agrupar].sum())
    elif funcion == "size":
        agrupado = pd.Series.to_frame(data.groupby(agrupacion).size())
        agrupado.columns = [agrupar]

    nombre_nueva_col = "c " + agrupacion
    agrupado[nombre_nueva_col] = agrupado.index.values

    fig = px.pie(agrupado,values=agrupar, names=nombre_nueva_col,color_discrete_sequence=colores)
    fig.update_layout(
        autosize= False,
        width=tam,
        height=tam,
        showlegend = leyenda
    )
    return fig