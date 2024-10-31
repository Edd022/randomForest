import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Función para cargar y preprocesar los datos desde el nuevo CSV
def cargar_datos(csv_path):
    # Cargar los datos del nuevo CSV con delimitador de punto y coma
    data = pd.read_csv(csv_path, delimiter=';')

    # Renombrar columnas y mapear datos para que coincidan con los nombres que el modelo espera
    data = data.rename(columns={
        'Diámetro Hueco (in)': 'Profundidad (m)',
        'OPERACIÓN': 'Solución_aplicada',
        'TIEMPO PLANEADO (hr)': 'Tiempo_identificación (min)',
        'TIEMPO EJECUTADO (hr)': 'Tiempo_arreglar_npt (min)'
    })

    # Convertir "Diámetro Hueco (in)" a metros
    data['Profundidad (m)'] = data['Profundidad (m)'] * 0.0254

    # Convertir tiempos de horas a minutos
    data['Tiempo_identificación (min)'] = data['Tiempo_identificación (min)'] * 60
    data['Tiempo_arreglar_npt (min)'] = data['Tiempo_arreglar_npt (min)'] * 60

    # Rellenar la columna 'NPT_comunes_no_comunes' basado en condiciones de ejemplo
    data['NPT_comunes_no_comunes'] = np.where(data['Solución_aplicada'].str.contains("TIEMPO NO PRODUCTIVO"), 'No común', 'Común')

    # Manejar valores NaN en la columna de objetivo llenándolos con la mediana
    data['Tiempo_arreglar_npt (min)'] = data['Tiempo_arreglar_npt (min)'].fillna(data['Tiempo_arreglar_npt (min)'].median())

    # Seleccionar solo las columnas necesarias para el modelo
    data = data[['Profundidad (m)', 'NPT_comunes_no_comunes', 'Tiempo_identificación (min)', 'Solución_aplicada', 'Tiempo_arreglar_npt (min)']]
    return data

# Función para preprocesar los datos y prepararlos para el modelo
def preprocesar_datos(data):
    # One-hot encoding para variables categóricas
    data = pd.get_dummies(data, columns=['NPT_comunes_no_comunes', 'Solución_aplicada'])
    X = data.drop('Tiempo_arreglar_npt (min)', axis=1)
    y = data['Tiempo_arreglar_npt (min)']

    # Estandarización de variables numéricas
    scaler = StandardScaler()
    X[['Profundidad (m)', 'Tiempo_identificación (min)']] = scaler.fit_transform(X[['Profundidad (m)', 'Tiempo_identificación (min)']])

    return X, y, scaler

# Función para entrenar el modelo Random Forest
def entrenar_modelo(X, y):
    model = RandomForestRegressor(n_estimators=500, max_depth=15, random_state=42)
    model.fit(X, y)
    return model

# Función para evaluar el modelo
def evaluar_modelo(model, X_test, y_test):
    y_pred = model.predict(X_test)

    # Calcular métricas de evaluación
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # Mostrar resultados
    print(f"R^2: {r2:.2f}")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

    return r2, mae, rmse

# Función para predecir el tiempo de arreglo con nuevos datos
def predecir_tiempo(model, scaler, profundidad, tipo_npt, tiempo_identificacion, solucion, X_train_columns):
    # Crear un DataFrame con los nuevos datos básicos
    nuevos_datos = pd.DataFrame({
        'Profundidad (m)': [profundidad],
        'Tiempo_identificación (min)': [tiempo_identificacion],
        'NPT_comunes_no_comunes_Común': [1 if tipo_npt == 'Común' else 0],
        'NPT_comunes_no_comunes_No común': [1 if tipo_npt == 'No común' else 0]
    })

    # One-hot encoding para 'Solución_aplicada' con la columna específica para 'solucion'
    solucion_column = f'Solución_aplicada_{solucion}'
    nuevos_datos[solucion_column] = 1

    # Crear un diccionario para las columnas que faltan
    columnas_faltantes = {col: 0 for col in X_train_columns if col not in nuevos_datos.columns}

    # Agregar las columnas faltantes en un solo paso
    nuevos_datos = pd.concat([nuevos_datos, pd.DataFrame(columnas_faltantes, index=[0])], axis=1)

    # Escalar las columnas numéricas
    nuevos_datos[['Profundidad (m)', 'Tiempo_identificación (min)']] = scaler.transform(
        nuevos_datos[['Profundidad (m)', 'Tiempo_identificación (min)']]
    )

    # Reordenar columnas para que coincidan con el orden de X_train
    nuevos_datos = nuevos_datos[X_train_columns]

    # Realizar la predicción
    tiempo_estimado = model.predict(nuevos_datos)[0]
    return tiempo_estimado


# Método main para ejecutar el flujo completo del modelo y realizar predicciones
def main():
    # Cargar y preprocesar los datos
    data = cargar_datos('UAS.csv')
    X, y, scaler = preprocesar_datos(data)

    # Dividir en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar el modelo
    model = entrenar_modelo(X_train, y_train)

    # Evaluar el modelo en el conjunto de prueba
    evaluar_modelo(model, X_test, y_test)

    # Hacer una predicción con datos de entrada específicos
    profundidad_test = 17.50*0.0254    # Ejemplo en metros
    tipo_npt_test = 'NPT'
    tiempo_identificacion_test = 0.00 * 60  # en minutos
    solucion_test = 'TIEMPO NO PRODUCTIVO NO OPERACIONAL (CLIMA, SOCIAL, LOCACIÓN)'

    # Realizar predicción
    tiempo_estimado = predecir_tiempo(model, scaler, profundidad_test, tipo_npt_test, tiempo_identificacion_test, solucion_test, X_train.columns)
    print(f"Tiempo estimado de arreglo: {tiempo_estimado:.2f} minutos")

# Ejecutar el método main
if __name__ == "__main__":
    main()
