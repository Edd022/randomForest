import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import tree
import matplotlib.pyplot as plt

# Ruta del archivo CSV
ruta_csv = r"C:\Users\Edward Julian Garcia\Documents\Código\randomForest\solucion.csv"

# Cargar el archivo CSV
datos = pd.read_csv(ruta_csv, delimiter=';')

# Verificar que las columnas necesarias estén presentes
if 'PASO' not in datos.columns or 'OPERACIÓN' not in datos.columns:
    raise ValueError("El archivo debe contener las columnas 'PASO' y 'OPERACIÓN'.")

# Preprocesar los datos (convertir texto a números si es necesario)
datos['PASO'] = datos['PASO'].astype(str)  # Asegurar que los PASOS sean cadenas
X = datos[['PASO']].copy()  # Entrada: PASO
y = datos['OPERACIÓN']  # Salida: OPERACIÓN

# Convertir las entradas categóricas a valores numéricos
X_encoded = pd.get_dummies(X, columns=['PASO'])

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Crear y entrenar el árbol de decisión
modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X_train, y_train)

# Evaluar el modelo (precisión)
precision = modelo.score(X_test, y_test)
print(f"Precisión del modelo: {precision:.2f}")

# Visualizar el árbol (opcional)
#plt.figure(figsize=(12, 8))
#tree.plot_tree(modelo, feature_names=X_encoded.columns, class_names=modelo.classes_, filled=True)
#plt.show()

# Hacer predicciones
def predecir_operacion(paso_input):
    # Convertir el input a la misma codificación utilizada en el entrenamiento
    paso_df = pd.DataFrame({'PASO': [paso_input]})
    paso_encoded = pd.get_dummies(paso_df, columns=['PASO'])
    paso_encoded = paso_encoded.reindex(columns=X_encoded.columns, fill_value=0)  # Asegurar columnas consistentes
    prediccion = modelo.predict(paso_encoded)
    return prediccion[0]

# Ejemplo de uso
paso_ejemplo = "DRIL11"  # Cambia esto por un PASO real de tu base de datos
operacion_predicha = predecir_operacion(paso_ejemplo)
print(f"La operación para el PASO {paso_ejemplo} es: {operacion_predicha}")
