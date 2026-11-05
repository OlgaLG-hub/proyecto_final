import pandas as pd

df = pd.read_csv("archive/food_waste_dataset.csv")
df.head()
print(df.head())

## Dataset
#-Archivo: food_waste_dataset.csv
#-Contenido: 8.000 registros de inventario de 2025 en 4 tipos de negocio
#-Variable a predecir: Waste_Quantity (cantidad desperdiciada, en unidades)

#Tamaño y tipos de datos
print("Filas y columnas:", df.shape)
df.info()

#Valores vacios y duplicados
print("Valores vacíos por columna:")
print(df.isnull().sum())
print()
print("Filas duplicadas:", df.duplicated().sum())

#Resumen de los números
df.describe()

#Categorias por columna
for columna in ["Business_Type", "Food_Category", "Promotion", "Weather", "Waste_Reason"]:
    print(columna)
    print(df[columna].value_counts())
    print()


print(df[["Purchase_Quantity", "Remaining_Stock", "Waste_Quantity"]].quantile([0.5, 0.9, 0.99, 0.999]))

#Limpieza de datos
## Arreglar la columna de fecha
df["Date"] = pd.to_datetime(df["Date"])

##Rellenar valores vacíos
# Números vacíos: usamos la mediana (el valor "del medio")
for columna in ["Shelf_Life_Days", "Storage_Temperature", "Daily_Demand"]:
    df[columna] = df[columna].fillna(df[columna].median())

# Textos vacíos
df["Weather"] = df["Weather"].fillna("Desconocido")
df["Donation_Made"] = df["Donation_Made"].fillna("No")

print("Vacíos que quedan:", df.isnull().sum().sum())

# Quitar valores extremos de las columnas numéricas
limite = df["Purchase_Quantity"].quantile(0.99)
df = df[df["Purchase_Quantity"] <= limite].copy()
print("Filas después de limpiar:", df.shape[0])

# Columnas nuevas
df["Month"] = df["Date"].dt.month
df["Day_Of_Week"] = df["Date"].dt.day_name()
df["Waste_Percent"] = df["Waste_Quantity"] / df["Purchase_Quantity"] * 100
df["Gap"] = df["Purchase_Quantity"] - df["Daily_Demand"]   # cuánto se compró de más

df.head()

#Guardamos el dataset limpio
df.to_csv("food_waste_limpio.csv", index=False)
print("Archivo guardado")

