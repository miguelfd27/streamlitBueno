import streamlit as st
import matplotlib.pyplot as plt
from keras import Sequential
from keras.datasets import mnist  # En este módulo está MNIST en formato numpy
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.optimizers import Adam, RMSprop, Adagrad, SGD
from sklearn.metrics import classification_report,ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
import paquetes.modulo as md
import time
import paquetes.modulo_datos as mdd
import paquetes.modulo as md

md.menu()
(X_train, y_train), (X_test, y_test) = mdd.obtener_datos("resources\\bd_formas.csv", 0.8)
st.write("Dimension x_train:",X_train.shape)
st.write("Dimension y_train:",y_train.shape)
st.write("Dimension x_test:",X_test.shape)
st.write("Dimension y_test:",y_test.shape)

X_train = X_train.reshape(len(X_train),28,28,1)
X_test = X_test.reshape(len(X_test),28,28,1)

label_binarizer = LabelBinarizer()
y_train = label_binarizer.fit_transform(y_train)
y_test = label_binarizer.fit_transform(y_test)

model = Sequential()
mdd.red_convolucional(model)
model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])

H = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=4,
                batch_size= int(160/8))

modelo = "modelos\\modelo_CNN_formas.h5"   
model.save(modelo)