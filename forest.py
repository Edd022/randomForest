import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

def cargar_datos(filepath):
    """Cargar los datos desde un archivo CSV."""
    return pd.read_csv(filepath)

def preprocesar_datos(data):
    """Preprocesar los datos, incluyendo codificación y normalización."""
    data = pd.get_dummies(data, columns=['NPT_comunes_no_comunes', 'Solución_aplicada'])
    X = data.drop('Tiempo_arreglar_npt (min)', axis=1)
    y = data['Tiempo_arreglar_npt (min)']

    # Normalizar las características numéricas
    scaler = StandardScaler()
    X[['Profundidad (m)', 'Tiempo_identificación (min)']] = scaler.fit_transform(X[['Profundidad (m)', 'Tiempo_identificación (min)']])

    return X, y, scaler

def entrenar_modelo(X, y):
    """Entrenar el modelo RandomForest y devolverlo."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=10000, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"MSE: {mse}")
    print(f"R²: {r2}")

    return model

def predecir_tiempo(model, scaler, profundidad, npt_comun, tiempo_identificacion, solucion=None):
    """Predecir el tiempo de arreglo del NPT basado en los datos proporcionados."""
    input_data = {
        'Profundidad (m)': [profundidad],
        'Tiempo_identificación (min)': [tiempo_identificacion],
        'NPT_comunes_no_comunes_Común': [1 if npt_comun == 'Común' else 0],
        'NPT_comunes_no_comunes_No común': [1 if npt_comun == 'No común' else 0],
    }

    for sol in ['Ajuste de bomba', 'Ajuste de presión', 'Ajuste de válvula', 'Inspección y limpieza',
                'Limpieza de tubería', 'Reemplazo completo', 'Reemplazo de pieza', 'Reparación estructural',
                'Reparación soldadura', 'Sustitución de junta']:
        input_data[f'Solución_aplicada_{sol}'] = [1 if solucion == sol else 0] if solucion else [0]

    input_df = pd.DataFrame(input_data)
    input_df[['Profundidad (m)', 'Tiempo_identificación (min)']] = scaler.transform(input_df[['Profundidad (m)', 'Tiempo_identificación (min)']])

    return model.predict(input_df)[0]

def recomendar_solucion(data, profundidad, npt_comun):
    """Recomendar la solución más común basada en los datos históricos."""
    rango_profundidad = 100
    data_filtrada = data[(data['Profundidad (m)'].between(profundidad - rango_profundidad, profundidad + rango_profundidad)) &
                         (data['NPT_comunes_no_comunes'] == npt_comun)]
    return data_filtrada['Solución_aplicada'].mode()[0] if not data_filtrada.empty else 'No hay sugerencias'

def main():
    # Cargar y preprocesar datos
    data = cargar_datos('datos_npt.csv')
    X, y, scaler = preprocesar_datos(data)

    # Entrenar el modelo
    model = entrenar_modelo(X, y)

    # Nuevos datos para predecir
    nueva_profundidad = 2000
    nuevo_npt_comun = 'No común'
    nuevo_tiempo_identificacion =28

    # Predecir el tiempo de arreglo
    tiempo_estimado = predecir_tiempo(model, scaler, nueva_profundidad, nuevo_npt_comun, nuevo_tiempo_identificacion)
    print(f"Tiempo estimado de arreglo: {tiempo_estimado:.2f} minutos")

    # Recomendar una solución basada en datos históricos
    solucion_sugerida = recomendar_solucion(data, nueva_profundidad, nuevo_npt_comun)
    print(f"Solución sugerida: {solucion_sugerida}")

if __name__ == "__main__":
    main()
