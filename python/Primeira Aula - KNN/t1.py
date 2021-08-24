import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier


df = pd.read_csv("../vinho.csv")

shape = df.shape

scaler = MinMaxScaler()
df[:] = scaler.fit_transform(df[:])
target = 'is good'
features = df.columns.to_list()
features.remove(target)
X_train, X_val, y_train, y_val = train_test_split(df[features], df[target], test_size=0.2, random_state=0)

clf = KNeighborsClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_val)


acc = accuracy_score(y_val, y_pred)

print(f'A acurácia foi de {acc * 100:.2f}%')

n_vizinhos = [3, 5, 7, 9, 11, 13, 17, 19, 23, 29]
resultados = []
for k in n_vizinhos:
    ##############################################################
    #                       PREENCHA AQUI:                       #
    #  - Crie um kNN com k vizinhos e utilizando distância       #
    # Manhattan                                                  #
    # - Treine esse modelo com X_train e y_train                 #
    # - Calcule a acurácia do modelo que você treinou e salve    #
    # o resultado na lista resultados                            #
    ##############################################################
    clf = KNeighborsClassifier(k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_val)
    acc = accuracy_score(y_val, y_pred)   
    resultados.append(acc)
    ##############################################################

for k, acc in zip(n_vizinhos, resultados):
    print(f'{k:02d} vizinhos => Acurácia {acc * 100:.2f}%')
