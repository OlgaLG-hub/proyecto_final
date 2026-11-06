import streamlit as st
import pandas as pd
import joblib

# Cargar el modelo y las columnas
modelo = joblib.load("modelo_desperdicio.pkl")
columnas = joblib.load("columnas_modelo.pkl")

#Función para predecir el desperdicio

def predecir(negocio, alimento, clima, promocion, compra, demanda, vida_util, temperatura):
    dia = pd.DataFrame([{
        "Business_Type": negocio,
        "Food_Category": alimento,
        "Weather": clima,
        "Promotion": promocion,
        "Purchase_Quantity": compra,
        "Daily_Demand": demanda,
        "Shelf_Life_Days": vida_util,
        "Storage_Temperature": temperatura,
    }])
    dia["Gap"] = dia["Purchase_Quantity"] - dia["Daily_Demand"]
    dia = pd.get_dummies(dia)
    dia = dia.reindex(columns=columnas, fill_value=0)
    return max(0, modelo.predict(dia)[0])


# ---------- Título ----------
st.title("🍽️ Rescatista de Alimentos")
st.write("Introduce las condiciones de tu día y estima cuánto alimento podrías desperdiciar.")

# ---------- Formulario ----------
col1, col2 = st.columns(2)

with col1:
    negocio = st.selectbox("Tipo de negocio",
                           ["Restaurant", "Cafeteria", "Supermarket", "Cloud Kitchen"])
    alimento = st.selectbox("Categoría de alimento",
                            ["Prepared Food", "Bakery", "Meat", "Fruits", "Vegetables", "Dairy"])
    clima = st.selectbox("Clima", ["Sunny", "Cloudy", "Hot", "Rainy"])
    promocion = st.radio("¿Hay promoción hoy?", ["No", "Yes"], horizontal=True)

with col2:
    compra = st.number_input("Cantidad comprada (unidades)", min_value=1, max_value=300, value=100)
    demanda = st.number_input("Demanda esperada (unidades)", min_value=1, max_value=300, value=90)
    vida_util = st.slider("Vida útil del alimento (días)", 1, 14, 4)
    temperatura = st.slider("Temperatura de almacenamiento (°C)", -5, 40, 10)

# ---------- Botón ----------
if st.button("Calcular desperdicio"):
    estimado = predecir(negocio, alimento, clima, promocion, compra, demanda, vida_util, temperatura)

    st.subheader("Resultado")
    st.metric("Desperdicio estimado", f"{estimado:.1f} unidades")

    # ---------- Reto extra: recomendaciones ----------
    st.subheader("Recomendaciones")
    hay_consejos = False

    if compra > demanda * 1.1:
        # Calculamos qué pasaría si compramos justo lo que se demanda
        ahorro_estimado = predecir(negocio, alimento, clima, promocion, demanda, demanda, vida_util, temperatura)
        st.warning(f"Estás comprando {compra - demanda} unidades más de lo que esperas vender. "
                   f"Si compras {demanda}, el desperdicio estimado bajaría a {ahorro_estimado:.1f} unidades.")
        hay_consejos = True

    if temperatura > 15:
        st.warning("La temperatura de almacenamiento es alta. Revisa la refrigeración para alargar la vida útil.")
        hay_consejos = True

    if vida_util <= 3 and estimado > 5:
        st.warning("El alimento dura pocos días. Considera hacer una promoción o donar el excedente antes de que venza.")
        hay_consejos = True

    if promocion == "No" and estimado > 10:
        st.info("Una promoción de último momento podría ayudar a vender el sobrante.")
        hay_consejos = True

    if not hay_consejos:
        st.success("¡Buen trabajo! Tus condiciones son adecuadas y el desperdicio esperado es bajo.")