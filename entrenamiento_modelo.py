#ENTRENAMIENTO DEL MODELO
#Paso 1. Importar herramientas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

df = pd.read_csv("food_waste_limpio.csv")

#Paso 2. Elegir las variables que usara el modelo

# Variables que se conocen ANTES de que termine el día
columnas_entrada = ["Business_Type", "Food_Category", "Weather", "Promotion",
                    "Purchase_Quantity", "Daily_Demand", "Shelf_Life_Days",
                    "Storage_Temperature"]

X = df[columnas_entrada].copy()   # entradas
y = df["Waste_Quantity"]          # lo que queremos predecir

# Columna extra: cuánto se compró de más que la demanda
X["Gap"] = X["Purchase_Quantity"] - X["Daily_Demand"]

X.head()

#Paso 3. Convertir texto a numeros

X = pd.get_dummies(X)

print("Columnas del modelo:", X.shape[1])
X.head()

#Paso 4. Separar datos de entrenamiento y de prueba. 80-20

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Para entrenar:", X_train.shape[0])
print("Para probar:", X_test.shape[0])


#Paso 5. Modelo de Comparacion
#Siempre predice el promedio, es un paso de prueba.

promedio = y_train.mean()
pred_base = [promedio] * len(y_test)

print("Error promedio (MAE):", round(mean_absolute_error(y_test, pred_base), 2))
print("R2:", round(r2_score(y_test, pred_base), 3))

#Paso 6. Entrenar el primer modelo. Regresion Lineal

modelo_lineal = LinearRegression()
modelo_lineal.fit(X_train, y_train)

pred_lineal = modelo_lineal.predict(X_test)

print("Error promedio (MAE):", round(mean_absolute_error(y_test, pred_lineal), 2))
print("R2:", round(r2_score(y_test, pred_lineal), 3))

#Paso 7. Entrenar el segundo modelo: Random Forest

modelo_bosque = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_bosque.fit(X_train, y_train)

pred_bosque = modelo_bosque.predict(X_test)

print("Error promedio (MAE):", round(mean_absolute_error(y_test, pred_bosque), 2))
print("R2:", round(r2_score(y_test, pred_bosque), 3))

# Paso 8. Comparar los resultados

resultados = pd.DataFrame({
    "Modelo": ["Promedio (base)", "Regresión Lineal", "Random Forest"],
    "Error MAE": [
        mean_absolute_error(y_test, pred_base),
        mean_absolute_error(y_test, pred_lineal),
        mean_absolute_error(y_test, pred_bosque),
    ],
    "R2": [
        r2_score(y_test, pred_base),
        r2_score(y_test, pred_lineal),
        r2_score(y_test, pred_bosque),
    ],
}).round(2)

resultados

# Paso 9. Gráfico: predicción vs. realidad

plt.figure(figsize=(6, 6))
plt.scatter(y_test, pred_bosque, alpha=0.3, color="steelblue")
maximo = y_test.max()
plt.plot([0, maximo], [0, maximo], color="red")
plt.title("Desperdicio real vs. predicho")
plt.xlabel("Real")
plt.ylabel("Predicho")
plt.show()

# Paso 10. ¿Qué variables pesan más?

importancia = pd.Series(modelo_bosque.feature_importances_, index=X.columns)
importancia = importancia.sort_values().tail(8)

importancia.plot(kind="barh", color="seagreen", figsize=(8, 4))
plt.title("Variables más importantes para predecir el desperdicio")
plt.show()

# Paso 11. Probar una predicción de un día

# Un día de ejemplo: cambiar estos valores y volver a ejecutar
dia = pd.DataFrame([{
    "Business_Type": "Restaurant",
    "Food_Category": "Prepared Food",
    "Weather": "Rainy",
    "Promotion": "No",
    "Purchase_Quantity": 200,
    "Daily_Demand": 100,
    "Shelf_Life_Days": 2,
    "Storage_Temperature": 20,
}])

dia["Gap"] = dia["Purchase_Quantity"] - dia["Daily_Demand"]
dia = pd.get_dummies(dia)
dia = dia.reindex(columns=X.columns, fill_value=0)   # misma estructura que el entrenamiento

resultado = modelo_bosque.predict(dia)[0]
print("Desperdicio estimado:", round(resultado, 1), "unidades")

# Paso 12. Guardar el modelo para la aplicación

joblib.dump(modelo_bosque, "modelo_desperdicio.pkl")
joblib.dump(list(X.columns), "columnas_modelo.pkl")
print("Modelo guardado")