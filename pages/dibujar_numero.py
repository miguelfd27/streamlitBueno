import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import paquetes.modulo as md
import tensorflow as tf
from streamlit_gsheets import GSheetsConnection
from collections import Counter
import csv
import hydralit_components as hc
import extra_streamlit_components as stx

def concatenar_matriz(matriz, aux, veces, vert):
    aux_matrix = matriz
    z = 0
    for i in range(veces):
        if vert:
            aux_matrix = np.vstack((aux,aux_matrix))
            aux_matrix = np.vstack((aux_matrix,aux))
        else:
            aux_matrix = np.hstack((aux,aux_matrix))
            aux_matrix = np.hstack((aux_matrix,aux))  
        z+=1

    return aux_matrix
def rellenar_cuadrado(valores_rgb,default_rgb):
    aux_matrix = valores_rgb
    shape = valores_rgb.shape
    dim_diff = abs(shape[0] - shape[1])

    vertical = True

    if shape[0] > shape[1]:
        vertical = False
        len = shape[0]
    else:
        len = shape[1]
    
    aux_line = []
    aux_line2 = []
    aux = [default_rgb]

    for i in range(len):
        if not vertical:
            aux_line.append(aux)
        else:
            aux_line2.append(default_rgb)

    if vertical:
        aux_line.append(aux_line2)     
    
    div = int(dim_diff / 2)

    if dim_diff%2 == 0:    
        aux_matrix = concatenar_matriz(aux_matrix, aux_line, div, vertical)
    else:
        aux_matrix = concatenar_matriz(aux_matrix, aux_line, div, vertical)
        if vertical:
            aux_matrix = np.vstack((aux_line,aux_matrix))
        else:
            aux_matrix = np.hstack((aux_line,aux_matrix))
    
    return aux_matrix

def ampliacion_coordenadas(coordenadas, amp):
    return "hello"

#min_left, min_top, max_left, max_top
def obtener_coordenadas(json_data):
    aux = [0,0,0,0]
    aux_left = 0
    aux_top = 0
    ini = True

    for i in json_data['objects'][0]['path']:
        aux_left = i[1]
        aux_top = i[2]
        if ini:
            aux[0] = int(aux_left)
            aux[1] = int(aux_top)
            ini = False
        if aux_left < aux[0]:
            aux[0] = int(aux_left)
        if aux_top < aux[1]:
            aux[1] = int(aux_top)
        if aux_left > aux[2]:
            aux[2] = int(aux_left)
        if aux_top > aux[3]:
            aux[3] = int(aux_top)

    return aux

def obtener_numero(array_num):
    delta = 0
    aux_d = 0
    aux = array_num[delta]

    for i in array_num:
        if i > aux:
            aux = i
            delta = aux_d
        aux_d+=1

    return delta

def obtener_forma(array_form):
    delta = obtener_numero(array_form)
    if delta == 0:
        return "Círculo"
    elif delta == 1:
        return "Cruz"
    elif delta == 2:
        return "Triángulo"
    elif delta == 3:
        return "Cuadrado"
        

def obtener_matriz_grises(data):
    aux = [0,0,0,0]
    aux_left = 0
    aux_top = 0
    ini = True
        #for i in canvas_result.json_data['objects'][0]['path']:
    for f in data:
        for i in f['path']:
            aux_left = i[1]
            aux_top = i[2]
            if ini:
                aux[0] = int(aux_left)
                aux[1] = int(aux_top)
                ini = False
            if aux_left < aux[0]:
                aux[0] = int(aux_left)
            if aux_top < aux[1]:
                aux[1] = int(aux_top)
            if aux_left > aux[2]:
                aux[2] = int(aux_left)
            if aux_top > aux[3]:
                aux[3] = int(aux_top)

    matriz_imagen = canvas_result.image_data[aux[1]-15:aux[3]+15,aux[0]-15:aux[2]+15,:3]
    default_value = [0,0,0]
    image_array = rellenar_cuadrado(np.array(matriz_imagen),default_value)
    image_array = np.array(image_array, dtype=np.uint8)
    #image_array = np.array(matriz_imagen, dtype=np.uint8)
    image = Image.fromarray(image_array, 'RGB')
    image_resized = image.resize((28,28))
    matriz_rgb = image_resized.convert('RGB')
    imagen_grises = image_resized.convert('L')
    image_rgb = np.array(matriz_rgb)
    matriz_grises = np.array(imagen_grises)
    return matriz_grises, imagen_grises

def inicializar_estado():
    if 'target_number' not in st.session_state:
        st.session_state.target_number = None
    if 'matriz' not in st.session_state:
            st.session_state.matriz = None
    if 'botoncito' not in st.session_state:
            st.session_state.botoncito = False
    if 'control' not in st.session_state:
            st.session_state.control = 0
    if 'canvas' not in st.session_state:
            st.session_state.canvas = False
    if 'canvas_result' not in st.session_state:
            st.session_state.canvas_result = None
    if 'predecir' not in st.session_state:
            st.session_state.predecir = None
    if 'target' not in st.session_state:
            st.session_state.target = None
    if 'select_form' not in st.session_state:
            st.session_state.select_form = None

def code_target(target):
    targets = ["Círculo","Cruz","Triángulo","Cuadrado"]
    aux = 0
    pos = 0
    
    for i in targets:
        if i == target:
            pos = aux
        aux+=1

    return pos

def calificar_resultado(columna):

    if predecir == 1:
        st.session_state.target = 1
    if predecir == 2:
        st.session_state.target = 2

    option_data = [
            {'icon': "bi bi-hand-thumbs-up", 'label':"Correcto"},
            {'icon': "bi bi-hand-thumbs-down", 'label':"Incorrecto"},
        ]

    over_theme = {'txc_inactive': 'white',
                    'menu_background':'purple',
                    'txc_active':'yellow',
                    'option_active':'blue'}
        
    font_fmt = {'font-class':'h2','font-size':'150%'}
    with columna:
        op2 = hc.option_bar(option_definition=option_data,
                        title='Califica el resultado',
                        key='PrimaryOption',
                        #override_theme=over_theme,
                        font_styling=font_fmt,horizontal_orientation=True)

def barra_seleccion(lista):
    col1, inter_cols_pace, col2 = st.columns((2, 3, 2))

    with inter_cols_pace:
        chosen_id = stx.tab_bar(data=[
                    stx.TabBarItemData(id=1, title=lista[0], description=""),
                    stx.TabBarItemData(id=2, title=lista[1], description=""),
                    ], default=None, key="predecir") 
    return chosen_id

def append_line(line, resource):
    with open(resource,"a",newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(line)
            csvfile.close()

st.set_page_config(layout="wide")
#INICIO DE LA PAGINA
authenticator = md.obtener_auth()
inicializar_estado()

if st.session_state["authentication_status"]:  
    st.markdown("<h1 style='text-align: center; color: grey;'>Prueba para la predicción de imágenes</h1>", unsafe_allow_html=True)
    #st.title("Prueba para la predicción de imágenes")

    val = stx.stepper_bar(steps=["Dibujar", "Prediccion", "Enviar"])

    if (st.session_state.control != 2):
        if (st.session_state.select_form is not None):
            target = code_target(st.session_state.select_form)
            resource = "resources\\bd_formas.csv"
            array_state = np.append(st.session_state.matriz, target)
            append_line(array_state, resource)

            st.session_state.control = 2
        if (st.session_state.target_number is not None):
            target = st.session_state.target_number
            resource = "resources\\bd_numeros.csv"
            array_state = np.append(st.session_state.matriz, target)
            append_line(array_state, resource)

            st.session_state.control = 2

    #añadimos el valor de entrada para la red neuronal y el target (784+1)
    md.logout(authenticator)
    md.menu()

    if (val == 0):
        stroke_width = 10
        stroke_color = "#FFFFFF"
        bg_color = "#000000"
        realtime_update = True

        
        left, inter_cols_pace, right = st.columns((2, 6, 2))
        left2, inter_cols_pace2, right2 = st.columns((2, 6, 2))

        with inter_cols_pace:
            st.write("Dibuje un número entre el 0 al 9 o una forma (Círculo, Cruz, Triángulo o Cuadrado) para que el modelo lo prediga: ")
        with inter_cols_pace2:
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
                stroke_width=stroke_width,
                stroke_color=stroke_color,
                background_color=bg_color,
                update_streamlit=realtime_update,
                height=150,
                drawing_mode="freedraw",
                display_toolbar=True,
                key="full_app",
            )
        canvas = False
        try:
            canvas = canvas_result.json_data['objects']!=[]
        except Exception as Error:
            print(Error)

        if canvas:
            st.session_state.control = 1
            st.session_state.canvas = True
            st.session_state.canvas_result = canvas_result

    if (val == 1 or val == 2) and (st.session_state.control == 0):
        if val == 1:
            st.markdown("<h3 style='text-align: center; color: grey;'>Dibuje un número o forma antes de realizar la prediccion</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='text-align: center; color: grey;'>Dibuje un número o forma antes de enviar la respuesta</h3>", unsafe_allow_html=True)
    if (val == 1) and (st.session_state.control == 1):
        #with st.container(height=100,border=False):
        predecir = barra_seleccion(["Predecir número","Predecir forma"])

        if predecir != "None":
            predecir = int(predecir)
        #if predecir_num and canvas:
        
        if (predecir == 1) or (predecir == 2):
            with hc.HyLoader('',hc.Loaders.standard_loaders,):
                canvas_result = st.session_state.canvas_result
                matriz_grises, imagen_grises = obtener_matriz_grises(canvas_result.json_data['objects'])

                matriz_grises_reshape = matriz_grises.reshape(1,28,28,1)
                if (predecir==1):
                    modelo_redes = tf.keras.models.load_model('modelos\\modelo_CNN_Adam.h5')
                else:
                    modelo_redes = tf.keras.models.load_model('modelos\\modelo_CNN_formas.h5')

                prediction = modelo_redes.predict(matriz_grises_reshape)

                st.session_state.matriz = matriz_grises.reshape(-1)

            columnas = st.columns(2)
            columnas2 = st.columns(2)

            c1 = columnas[0].container(border=False)
            c2 = columnas[1].container(border=False)
            co1 = columnas2[0].container(border=False)
            co2 = columnas2[1].container(border=False)
        
            col, coc, cor = co1.columns((2,3,1))
            container_c = coc.container(border=False)
            caption = "Imagen en escala de grises 28*28"
        
            container_c.image(imagen_grises,caption=caption, use_column_width= False, width=150)
            if (predecir==1):
                texto = "El número predicho por el modelo es: " + str(obtener_numero(prediction[0]))
            else:
                texto = "Forma predicha por el modelo: " + obtener_forma(prediction[0])
            co2.text(texto)
            
            calificar_resultado(co2)

    if st.session_state.canvas and (val == 2) and (st.session_state.control == 1):
        
        col = st.columns(3)
        col2 = st.columns(3)
        
        col1 = col[1].container(border=False)
        col2 = col2[1].container(border=False)

        if st.session_state.target == 1:
            numero = col1.number_input("Indique la forma o número que has dibujado: ",
                                    min_value=0,max_value=9,value=None,
                                    key="target_number",
                                    placeholder="Escriba la forma que has dibujado...")
            col2.button("Enviar informacion",
                    key="botoncito",
                    use_container_width=True) 
            
        if st.session_state.target == 2:
            selector = col1.selectbox("Indique la figura que a dibujado",
                options=["Círculo", "Cruz", "Triángulo","Cuadrado"],
                key="select_form",
                placeholder="Elige una forma..."
            )
            
        
        

    if (val==2) and (st.session_state.control == 2):
        st.markdown("<h3 style='text-align: center; color: grey;'>Información enviada</h3>", unsafe_allow_html=True)
        st.session_state.control = 0
else:
    md.error_session_message(authenticator)