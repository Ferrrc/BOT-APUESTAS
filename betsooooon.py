import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

opcion = input("Ingresa una opcion: ")


# Opciones disponibles
opciones = ['l', 'e', 'v']

# Inicializar contadores
contador = {opcion: 0 for opcion in opciones}

# Conectar a la base de datos SQLite
conn = sqlite3.connect('resultados.db')
c = conn.cursor()

# Crear tabla si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        opcion TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')


# Función para predecir la siguiente opción usando SVM
def predecir_siguiente_opcion():
    df = pd.read_sql_query('SELECT * FROM resultados', conn)
    if len(df) < 10:  # Asegurarnos de tener suficientes datos para entrenar el modelo
        return opcion, {opcion: 1/3 for opcion in opciones}

    # Preparar los datos
    df['opcion'] = df['opcion'].apply(lambda x: opciones.index(x))
    X = df['id'].values.reshape(-1, 1)
    y = df['opcion']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear y entrenar el modelo SVM
    model = SVC(probability=True)
    model.fit(X_train, y_train)

    # Predecir la próxima opción
    prediccion = model.predict([[len(df) + 1]])
    probabilidades = model.predict_proba([[len(df) + 1]])[0]

    siguiente_opcion = opciones[prediccion[0]]
    probabilidades_dict = {opciones[i]: prob for i, prob in enumerate(probabilidades)}
    return siguiente_opcion, probabilidades_dict

# Función para recibir una nueva opción
def nueva_opcion(opcion):
    if opcion in opciones:
        contador[opcion] += 1
        # Guardar en la base de datos
        c.execute('INSERT INTO resultados (opcion) VALUES (?)', (opcion,))
        conn.commit()
        siguiente_opcion, probabilidades = predecir_siguiente_opcion()
        print(f"Anterior: {opcion}")
        print(f"Siguiente: {siguiente_opcion}")
        print(f"Probabilidades: {probabilidades}")
    else:
        print(f"Opción no válida. Por favor, elige una de las siguientes: {opciones}")
    

# Entrada de opciones
flag = True
cont = 0
cont_s = 0
cont_n = 0
while flag == True:    
    nueva_opcion(opcion)
    sn = input("Acerté? ")
    if sn == "s":
        cont_s+=1
    else:
        cont_n+=1
    opcion = input("Ingresa una opcion: ")
    cont += 1
    if opcion == "0":
        flag = False
    

print("Jugadas:", cont)
print("Acertadas: " , cont_s)
print("No Acertadas:", cont_n)