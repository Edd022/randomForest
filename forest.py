import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

class ModeloRF:
    def __init__(self, data_path):
        # Leer el archivo CSV actualizado
        df = pd.read_csv(data_path, delimiter=';', encoding='utf-8', on_bad_lines='skip')

        # Seleccionar solo columnas numéricas y eliminar filas con valores faltantes
        numerical_df = df.select_dtypes(include=[np.number]).dropna()

        # Definir la variable objetivo (target) y las características (features)
        X = numerical_df.drop(columns=['TIEMPO EJECUTADO (hr)'], errors='ignore')
        y = numerical_df['TIEMPO EJECUTADO (hr)']

        # Dividir los datos en conjunto de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Escalar las características para un mejor rendimiento
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Inicializar y entrenar el modelo de Random Forest
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)

        # Realizar predicciones para calcular las métricas de rendimiento
        y_pred = self.model.predict(X_test_scaled)
        self.metrica_mse = mean_squared_error(y_test, y_pred)
        self.metrica_mae = mean_absolute_error(y_test, y_pred)
        self.metrica_r2 = r2_score(y_test, y_pred)
        self.metrica_rmse = np.sqrt(self.metrica_mse)

        # Guardar nombres de columnas para usar en predicciones
        self.feature_columns = X.columns

    def predecir_tiempo(self, profundidad, tiempo_iden):
        # Crear un DataFrame con las columnas necesarias para la predicción, con valores predeterminados
        entrada = pd.DataFrame([[profundidad, tiempo_iden]], columns=self.feature_columns[:2])

        # Asegurar que todas las columnas estén presentes, usando un valor predeterminado si falta alguna
        for col in self.feature_columns:
            if col not in entrada.columns:
                entrada[col] = 0  # O usa otro valor predeterminado si es necesario

        # Reordenar las columnas para coincidir con el orden original
        entrada = entrada[self.feature_columns]

        # Escalar la entrada
        entrada_scaled = self.scaler.transform(entrada)

        # Realizar la predicción
        prediccion = self.model.predict(entrada_scaled)
        return prediccion[0]

    def obtener_métricas(self):
        return {
            "MSE": self.metrica_mse,
            "MAE": self.metrica_mae,
            "R2": self.metrica_r2,
            "RMSE": self.metrica_rmse
        }

# Ruta al archivo actualizado
file_path = 'UAS_COMPLETO.csv'

# Inicializar y entrenar el modelo
modelo_rf = ModeloRF(file_path)

# Obtener métricas y mostrar
métricas = modelo_rf.obtener_métricas()
print(f"Error Cuadrático Medio (MSE): {métricas['MSE']}")
print(f"Error Absoluto Medio (MAE): {métricas['MAE']}")
print(f"Coeficiente de Determinación (R²): {métricas['R2']}")
print(f"Raíz del Error Cuadrático Medio (RMSE): {métricas['RMSE']}")

# Ejemplo de predicción y conversión a formato estándar
profundidad = 10.0  # Valor de ejemplo para 'DIAMETRO DEL HUECO (in)'
tiempo_iden = 2.0   # Valor de ejemplo para 'TIEMPO PLANEADO (hr)'
tiempo_estimado = modelo_rf.predecir_tiempo(profundidad, tiempo_iden)

# Convertir el tiempo a horas y minutos
horas = int(tiempo_estimado)
minutos = int((tiempo_estimado - horas) * 60)

# Mostrar el tiempo en formato estándar
print(f"Tiempo estimado de arreglo: {horas} horas y {minutos} minutos")
