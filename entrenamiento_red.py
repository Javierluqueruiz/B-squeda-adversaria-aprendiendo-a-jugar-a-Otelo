import numpy as np
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Input, Dense, Flatten
from keras.optimizers import SGD

print("Cargando el conjunto de datos...")

X = np.load("datasets/dataset_tableros.npy")
Y = np.load("datasets/dataset_etiquetas.npy")

print(f"Forma de los tableros (X): {X.shape}")
print(f"Forma de las etiquetas (Y): {Y.shape}")


(atributos_entrenamiento, atributos_prueba,
    objetivo_entrenamiento, objetivo_prueba) = train_test_split(X, Y, test_size=0.2 )

print(f"Conjunto de entrenamiento: {atributos_entrenamiento.shape[0]} tableros"
      f" | Conjunto de prueba: {atributos_prueba.shape[0]} tableros")

#Arquitectura de la red neuronal
red_otelo = Sequential()
red_otelo.add(Input(shape=(8, 8)))
red_otelo.add(Flatten())

red_otelo.add(Dense(64, activation='relu'))
red_otelo.add(Dense(32, activation='relu'))
red_otelo.add(Dense(1, activation='tanh'))
red_otelo.summary()

red_otelo.compile(
    optimizer=SGD(learning_rate=0.01),
    loss='mean_squared_error',
    metrics=['mean_absolute_error']
)

historial = red_otelo.fit(
    atributos_entrenamiento, 
    objetivo_entrenamiento,
    epochs=50,
    batch_size=256,
    validation_data=(atributos_prueba, objetivo_prueba)
)

red_otelo.save("modelos/otelo.keras")
