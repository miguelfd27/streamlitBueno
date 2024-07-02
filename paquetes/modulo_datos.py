from keras import Sequential
from keras.datasets import mnist  # En este módulo está MNIST en formato numpy
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.optimizers import Adam, RMSprop, Adagrad, SGD
import csv
import numpy as np

def red_convolucional(model):
    model.add(Conv2D(filters = 8, kernel_size = (5,5),padding = 'Same', 
                    activation ='relu', input_shape = (28,28,1)))
    model.add(MaxPool2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
            #
    model.add(Conv2D(filters = 16, kernel_size = (3,3),padding = 'Same', 
                            activation ='relu'))
    model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))
    model.add(Dropout(0.25))
            # fully connected
    model.add(Flatten())
    model.add(Dense(256, activation = "relu"))
    model.add(Dropout(0.5))
    model.add(Dense(4, activation = "softmax"))

def obtener_datos(resource, porcentaje):
    lista_total = []
    with open(resource,newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
           lista_enteros = list(map(int, row))
           lista_total.append(lista_enteros)

    tam_lista = len(lista_total)
    control = tam_lista*porcentaje
    aux = 0

    input_train = []
    target_train = []
    input_test = []
    target_test = []

    for i in lista_total:
        if aux < control: 
            i_np = np.array(i[:-1]).reshape((28,28))
            input_train.append(i_np)
            target_train.append(i[-1])
        else:
            i_np = np.array(i[:-1]).reshape((28,28))
            input_test.append(i_np)
            target_test.append(i[-1])
        aux+=1

    input_test = np.array(input_test)
    input_train = np.array(input_train)
    target_test = np.array(target_test)
    target_train = np.array(target_train)

    return (input_train, target_train), (input_test, target_test)