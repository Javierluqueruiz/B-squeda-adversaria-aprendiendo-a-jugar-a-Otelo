import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import BatchNormalization, Dropout, Input, Dense, Flatten
from keras.optimizers import SGD, Adam
from keras.utils import set_random_seed
set_random_seed(394868)


print("Cargando el conjunto de datos...")

X = np.load("datasets/dataset_tableros.npy")
Y = np.load("datasets/dataset_etiquetas.npy")

print(f"Forma de los tableros (X): {X.shape}")
print(f"Forma de las etiquetas (Y): {Y.shape}")


(atributos_entrenamiento, atributos_prueba,
    objetivo_entrenamiento, objetivo_prueba) = train_test_split(X, Y, test_size=0.2, random_state=42)

print(f"Conjunto de entrenamiento: {atributos_entrenamiento.shape[0]} tableros"
      f" | Conjunto de prueba: {atributos_prueba.shape[0]} tableros")

def entrenar_modelo(nombre_archivo, activacion_oculta, optimizador):
    print(f"Entrenando {nombre_archivo}...")


    red_otelo = Sequential()
    red_otelo.add(Input(shape=(8, 8)))
    red_otelo.add(Flatten())
    red_otelo.add(Dense(64, activation=activacion_oculta))
    red_otelo.add(Dense(32, activation=activacion_oculta))
    red_otelo.add(Dense(1, activation='tanh'))

    red_otelo.compile(
        optimizer=optimizador,
        loss='mean_squared_error',
        metrics=['mean_absolute_error']
    )

    red_otelo.fit(
        atributos_entrenamiento, objetivo_entrenamiento,
        epochs=50,
        batch_size=256,
        validation_data=(atributos_prueba, objetivo_prueba),
        verbose=1
    )

    red_otelo.save(f"modelos/{nombre_archivo}.keras")
    print(f"Guardado {nombre_archivo}.keras")



entrenar_modelo("otelo_A", "relu", SGD(learning_rate=0.01))
entrenar_modelo("otelo_B", "sigmoid", SGD(learning_rate=0.01))
entrenar_modelo("otelo_C", "relu", Adam(learning_rate=0.001))

def entrenar_modelo_D(nombre_archivo):
    print(f"Entrenando {nombre_archivo}...")

    red = Sequential()
    red.add(Input(shape=(8, 8)))
    red.add(Flatten())

    red.add(Dense(128, activation='relu'))
    red.add(BatchNormalization())
    red.add(Dropout(0.3))

    red.add(Dense(64, activation='relu'))
    red.add(BatchNormalization())
    red.add(Dropout(0.3))

    red.add(Dense(32, activation='relu'))
    red.add(BatchNormalization())
    red.add(Dropout(0.3))

    red.add(Dense(1, activation='tanh'))

    red.compile(
        optimizer=Adam(learning_rate=0.0005),
        loss='mean_squared_error',
        metrics=['mean_absolute_error']
    )

    red.fit(
        atributos_entrenamiento, objetivo_entrenamiento,
        epochs=500,
        batch_size=256,
        validation_data=(atributos_prueba, objetivo_prueba),
        verbose=1
    )

    red.save(f"modelos/{nombre_archivo}.keras")
    print(f"Guardado {nombre_archivo}.keras")

entrenar_modelo_D("otelo_D")
