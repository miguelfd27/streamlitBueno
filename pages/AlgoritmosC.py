import argparse

import paquetes.modulo as md
import pandas as pd
import time
import streamlit as st
import matplotlib.pyplot as plt
from keras.datasets import mnist  # En este módulo está MNIST en formato numpy
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB, ComplementNB
from sklearn.svm import SVC
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import roc_curve, auc,RocCurveDisplay

plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')

from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

#funcion para calcular el promedio roc de todas las clases
def promedio_roc(clases, conjunto_test, conjunto_pred):
    auc_score = []
    tam_clases = len(clases)
    for i in range(tam_clases):
        fpr, tpr, aux = roc_curve(conjunto_test.loc[:, clases[i]], conjunto_pred.loc[:, clases[i]])
        auc_score.append(auc(fpr, tpr)) 
 
    promedio_roc = sum(auc_score) / tam_clases

    return promedio_roc, auc_score

def menu():
    #Muestra el nuevo menú
    st.sidebar.page_link("pages/MNIST.py", label="MNIST")

@st.cache_data
def cargar_datos():
    return mnist.load_data()

@st.cache_data
def laberized_datos(y_train):
    label_binarizer = LabelBinarizer().fit(y_train)
    y_onehot_test = label_binarizer.transform(y_test)
    return label_binarizer, y_onehot_test

menu()

authenticator = md.obtener_auth()

if st.session_state["authentication_status"]:
    md.menu()
    md.logout(authenticator)

    tipo_opti = st.selectbox(
            "Algortimo",
            options = ("None","K-vecinos","Naive Bayes G","Naive Bayes B","Naive Bayes C","Naive Bayes M","SVM OvsR", "SVM OvsO Radial", "SVM OvsO Lineal"),
            index=None,
            placeholder="Elija un algoritmo",
        )

    if st.button("Entrenar Algortimo"):
        (X_train, y_train), (X_test, y_test) = cargar_datos()

        X_train = X_train.reshape((X_train.shape[0], 28 * 28 * 1))
        X_test = X_test.reshape((X_test.shape[0], 28 * 28 * 1))

        X_train = X_train.astype('float32') / 255.0
        X_test = X_test.astype('float32') / 255.0

        lb, y_onehot_test = laberized_datos(y_train)

        n_neighbors = 9
        
        inicio = time.time()
        with st.spinner('Entrenando el modelo, podría llevar unos minutos...(1/4)'):
            if tipo_opti == "K-vecinos":
                modelo_clasificacion = KNeighborsClassifier(n_neighbors)
            elif tipo_opti == "Naive Bayes G":
                modelo_clasificacion = GaussianNB()
            elif tipo_opti == "Naive Bayes M":
                modelo_clasificacion = MultinomialNB()
            elif tipo_opti == "Naive Bayes B":
                modelo_clasificacion = BernoulliNB()
            elif tipo_opti == "Naive Bayes C":
                modelo_clasificacion = ComplementNB()
            elif tipo_opti == "SVM OvsR":
                modelo_clasificacion = LogisticRegression(multi_class='ovr')
            elif tipo_opti == "SVM OvsO Radial":
                modelo_clasificacion = SVC(decision_function_shape='ovo')
            elif tipo_opti == "SVM OvsO Lineal":
                modelo_clasificacion = SVC(decision_function_shape='ovo', kernel='linear')

            modelo_clasificacion.fit(X_train,y_train)
            
            test_score = modelo_clasificacion.score(X_test, y_test)
        final = time.time()
        
        with st.spinner('Cargando...                    (2/4)'):
            predicts = modelo_clasificacion.predict(X_test)
            y_onehot_pred = lb.transform(predicts)
        
        with st.spinner('Cargando matriz de confusión...(3/4)'):
            title = "Matriz de confusión"
            display = ConfusionMatrixDisplay.from_estimator(
                modelo_clasificacion,
                X_test,
                y_test,
                display_labels=["0","1","2","3","4","5","6","7","8","9"],
                cmap=plt.cm.Blues,
                normalize=None,
            )
            display.ax_.set_title(title)
            fig = display.figure_


        with st.spinner('Cargando curva ROC...(4/4)'):
            clase = "siete"
        
            clases = ["cero","uno","dos","tres","cuatro","cinco","seis","siete","ocho","nueve"]
            df_test = pd.DataFrame(y_onehot_test, columns=clases)
            df_pred = pd.DataFrame(y_onehot_pred, columns=clases)

            pr_roc, lista_roc = promedio_roc(clases,df_test,df_pred)

            title2 = "Curva ROC " + clases[6]

            print("[INFO] Creando imagenes")
            display2 = RocCurveDisplay.from_predictions(
                df_test.loc[:, clase],
                df_pred.loc[:, clase],
                name=f"{clase} vs el resto",
                color="darkorange",
            )
            display2.ax_.set(
                xlabel="False Positive Rate",
                ylabel="True Positive Rate",
                title="curva One-vs-Rest: \n" + clase,
            )
            fig2 = display2.figure_
        
        st.write('Precisión en el conjunto de test: {:.4f}'
            .format(test_score))
        st.write('Tiempo de entrenamiento: ', round(final-inicio,2), "s")
        st.pyplot(fig)
        st.pyplot(fig2)
        
        st.write("Promedio ROC para el algortimo ",tipo_opti,": ",round(pr_roc,2))

md.error_session_message(authenticator)
