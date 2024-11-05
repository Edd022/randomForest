import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
import numpy as np

class RandomForestModel:
    def __init__(self, file_path):
        # Cargar y preprocesar los datos
        self.data = pd.read_csv(file_path, delimiter=';', on_bad_lines='skip')
        self.data = self.data.dropna(subset=['GAP (hr)'])
        self.data['TIEMPO PLANEADO (hr)'] = self.data['TIEMPO PLANEADO (hr)'].fillna(self.data['TIEMPO PLANEADO (hr)'].mean())
        self.data['TIEMPO EJECUTADO (hr)'] = self.data['TIEMPO EJECUTADO (hr)'].fillna(self.data['TIEMPO EJECUTADO (hr)'].mean())

        # Codificar la columna categórica "OPERACIÓN"
        encoder = OneHotEncoder()
        operacion_encoded = encoder.fit_transform(self.data[['OPERACIÓN']]).toarray()
        operacion_df = pd.DataFrame(operacion_encoded, columns=encoder.get_feature_names_out(['OPERACIÓN']))

        # Combinar datos
        self.features = pd.concat([self.data[['Diámetro Hueco (in)', 'TIEMPO PLANEADO (hr)', 'TIEMPO EJECUTADO (hr)']], operacion_df], axis=1)
        self.features = self.features.dropna().reset_index(drop=True)
        self.target = self.data['GAP (hr)'].reset_index(drop=True)

        # Ajuste para tener el mismo tamaño
        min_length = min(len(self.features), len(self.target))
        self.features = self.features.iloc[:min_length]
        self.target = self.target.iloc[:min_length]

        # Dividir en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(self.features, self.target, test_size=0.2, random_state=42)

        # Entrenar el modelo
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Calcular las métricas de evaluación en el conjunto de prueba
        y_pred = self.model.predict(X_test)
        self.mse = mean_squared_error(y_test, y_pred)
        self.rmse = np.sqrt(self.mse)
        self.mae = mean_absolute_error(y_test, y_pred)
        self.r2 = r2_score(y_test, y_pred)

    def obtener_métricas(self):
        # Retornar las métricas en un formato legible
        return {
            'R2': self.r2,
            'MAE': self.mae,
            'RMSE': self.rmse
        }

    def predecir_tiempo(self, profundidad, tipo_npt, tiempo_iden, solucion):
        # Realizar el mismo preprocesamiento para la entrada
        input_data = pd.DataFrame({
            'Diámetro Hueco (in)': [profundidad],
            'TIEMPO PLANEADO (hr)': [tiempo_iden],
            'TIEMPO EJECUTADO (hr)': [0],  # Valor arbitrario si necesario
        })

        # Codificación de la operación (solución)
        operacion_encoded = np.zeros(len(self.features.columns) - 3)  # Inicializar el vector de operaciones
        if f'OPERACIÓN_{solucion}' in self.features.columns:
            operacion_encoded[self.features.columns.get_loc(f'OPERACIÓN_{solucion}') - 3] = 1  # Ajuste del índice

        # Concatenar características
        input_data = pd.concat([input_data, pd.DataFrame([operacion_encoded], columns=self.features.columns[3:])], axis=1)

        # Predicción
        pred = self.model.predict(input_data)
        return pred[0]  # Retorna el valor predicho
