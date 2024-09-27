import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

class RandomForestModel:
    def __init__(self, filepath):
        self.data = self.cargar_datos(filepath)
        self.X, self.y, self.scaler = self.preprocesar_datos(self.data)
        self.model = self.entrenar_modelo()

    def cargar_datos(self, filepath):
        return pd.read_csv(filepath)

    def preprocesar_datos(self, data):
        data = pd.get_dummies(data, columns=['NPT_comunes_no_comunes', 'Solución_aplicada'])
        X = data.drop('Tiempo_arreglar_npt (min)', axis=1)
        y = data['Tiempo_arreglar_npt (min)']
        scaler = StandardScaler()
        X[['Profundidad (m)', 'Tiempo_identificación (min)']] = scaler.fit_transform(X[['Profundidad (m)', 'Tiempo_identificación (min)']])
        return X, y, scaler

    def entrenar_modelo(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=10000, max_depth=10, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(f"MSE: {mean_squared_error(y_test, y_pred)}")
        print(f"R²: {r2_score(y_test, y_pred)}")
        return model

    def predecir_tiempo(self, profundidad, npt_comun, tiempo_identificacion, solucion=None):
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
        input_df[['Profundidad (m)', 'Tiempo_identificación (min)']] = self.scaler.transform(input_df[['Profundidad (m)', 'Tiempo_identificación (min)']])

        return self.model.predict(input_df)[0]
