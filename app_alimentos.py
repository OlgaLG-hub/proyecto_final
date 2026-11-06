import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# ---------- Configuración de la página ----------
st.set_page_config(page_title="Rescatista de Alimentos", page_icon="🌱", layout="wide")

# ---------- Estilos (colores de las tarjetas) ----------
st.markdown("""
<style>
.encabezado {
    background: linear-gradient(90deg, #2E7D32, #66BB6A);
    padding: 24px 30px;
    border-radius: 14px;
    color: white;
    margin-bottom: 20px;
}
.encabezado h1 { color: white; margin: 0; font-size: 2.2rem; }
.encabezado p  { margin: 6px 0 0 0; font-size: 1.05rem; opacity: 0.95; }

.tarjeta {
    background: white;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-top: 6px solid #2E7D32;
}
.tarjeta .titulo { font-size: 0.95rem; color: #5b7a5e; }
.tarjeta .valor  { font-size: 2.2rem; font-weight: 700; }

.consejo {
    background: white;
    border-left: 6px solid #F9A825;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
</style>
""", unsafe_allow_html=True)

# ---------- Cargar el modelo ----------
modelo = joblib.load("modelo_desperdicio.pkl")
columnas = joblib.load("columnas_modelo.pkl")


# ---------- Función que hace la predicción ----------
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


# ---------- Función del semáforo ----------
def nivel(porcentaje):
    if porcentaje < 5:
        return "Bajo", "🟢", "#2E7D32"
    elif porcentaje < 10:
        return "Medio", "🟡", "#F9A825"
    else:
        return "Alto", "🔴", "#C62828"


def tarjeta(titulo, valor, color="#2E7D32"):
    return f"""<div class="tarjeta" style="border-top-color:{color}">
                 <div class="titulo">{titulo}</div>
                 <div class="valor" style="color:{color}">{valor}</div>
               </div>"""


# ---------- Encabezado ----------
st.markdown("""
<div class="encabezado">
    <h1>🌱 Rescatista de Alimentos</h1>
    <p>Estima cuánta comida podrías desperdiciar hoy y descubre cómo evitarlo.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Barra lateral: formulario ----------
st.sidebar.header("🥗 Datos del día")

negocio = st.sidebar.selectbox("🏪 Tipo de negocio",
                               ["Restaurant", "Cafeteria", "Supermarket", "Cloud Kitchen"])
alimento = st.sidebar.selectbox("🍎 Categoría de alimento",
                                ["Prepared Food", "Bakery", "Meat", "Fruits", "Vegetables", "Dairy"])
clima = st.sidebar.selectbox("🌦️ Clima", ["Sunny", "Cloudy", "Hot", "Rainy"])
promocion = st.sidebar.radio("🏷️ ¿Hay promoción hoy?", ["No", "Yes"], horizontal=True)

st.sidebar.divider()

compra = st.sidebar.number_input("🛒 Cantidad comprada (unidades)", min_value=1, max_value=300, value=100)
demanda = st.sidebar.number_input("👥 Demanda esperada (unidades)", min_value=1, max_value=300, value=90)
vida_util = st.sidebar.slider("⏳ Vida útil (días)", 1, 14, 4)
temperatura = st.sidebar.slider("🌡️ Temperatura de almacenamiento (°C)", -5, 40, 10)

calcular = st.sidebar.button("Calcular desperdicio", type="primary")

# ---------- Pantalla principal ----------
if not calcular:
    st.info("👈 Completa los datos en la barra lateral y pulsa **Calcular desperdicio**.")
else:
    estimado = predecir(negocio, alimento, clima, promocion, compra, demanda, vida_util, temperatura)
    porcentaje = estimado / compra * 100
    texto_nivel, emoji, color = nivel(porcentaje)

    # --- Tres tarjetas ---
    c1, c2, c3 = st.columns(3)
    c1.markdown(tarjeta("Desperdicio estimado", f"{estimado:.1f} unid.", color), unsafe_allow_html=True)
    c2.markdown(tarjeta("De lo que compraste", f"{porcentaje:.1f} %", color), unsafe_allow_html=True)
    c3.markdown(tarjeta("Nivel de desperdicio", f"{emoji} {texto_nivel}", color), unsafe_allow_html=True)

    st.write("")

    # --- Gráfico: tu compra vs. compra ajustada ---
    st.subheader("📊 ¿Qué pasaría si compras justo lo que necesitas?")
    ajustado = predecir(negocio, alimento, clima, promocion, demanda, demanda, vida_util, temperatura)

    nombres = [f"Tu compra\n({compra} unid.)", f"Compra ajustada\n({demanda} unid.)"]
    valores = [estimado, ajustado]

    fig, ax = plt.subplots(figsize=(6, 3))
    fig.patch.set_facecolor("#F4F9F1")
    ax.set_facecolor("#F4F9F1")
    barras = ax.bar(nombres, valores, color=[color, "#2E7D32"], width=0.5)
    ax.bar_label(barras, fmt="%.1f", fontsize=13, fontweight="bold", padding=3)
    ax.set_ylabel("Unidades desperdiciadas")
    ax.set_ylim(0, max(valores) * 1.25 + 1)
    ax.spines[["top", "right"]].set_visible(False)
    col_grafico, _ = st.columns([3, 1])   # el gráfico ocupa 3/4 del ancho
    col_grafico.pyplot(fig)

    if compra > demanda and estimado > ajustado:
        st.success(f"Ajustando la compra a la demanda evitarías unas **{estimado - ajustado:.1f} unidades** de desperdicio.")

    # --- Recomendaciones ---
    st.subheader("💡 Recomendaciones")
    consejos = []

    if compra > demanda * 1.1:
        consejos.append(f"🛒 <b>Reduce la compra.</b> Estás comprando {compra - demanda} unidades más de lo que esperas vender.")
    if temperatura > 15:
        consejos.append("🌡️ <b>Revisa la refrigeración.</b> La temperatura de almacenamiento es alta y acorta la vida útil.")
    if vida_util <= 3 and estimado > 5:
        consejos.append("⏳ <b>Actúa rápido.</b> El alimento dura pocos días: haz una promoción o dona el excedente antes de que venza.")
    if promocion == "No" and estimado > 10:
        consejos.append("🏷️ <b>Prueba una promoción</b> de último momento para vender el sobrante.")

    if consejos:
        for texto in consejos:
            st.markdown(f'<div class="consejo">{texto}</div>', unsafe_allow_html=True)
    else:
        st.success("✅ ¡Buen trabajo! Tus condiciones son adecuadas y el desperdicio esperado es bajo.")
        
# ---------- Análisis general del desperdicio ----------
st.divider()
st.header("📈 Análisis general del desperdicio")
st.write("Explora los patrones de desperdicio alimentario según los datos históricos.")

@st.cache_data
def cargar_datos():
    return pd.read_csv("food_waste_limpio.csv")

try:
    datos = cargar_datos()

    # --- Gráfico 1: Desperdicio medio por categoría ---
    if {"Food_Category", "Waste_Quantity"}.issubset(datos.columns):
        st.subheader("🥗 Desperdicio medio por categoría")

        desperdicio_categoria = (
            datos.groupby("Food_Category")["Waste_Quantity"]
            .mean()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(9, 4))
        desperdicio_categoria.plot(kind="bar", ax=ax, color="#66BB6A")
        ax.set_ylabel("Unidades desperdiciadas")
        ax.set_xlabel("Categoría de alimento")
        ax.set_title("Desperdicio medio por categoría")
        ax.tick_params(axis="x", rotation=30)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # --- Gráfico 2: Desperdicio por motivo ---
    if {"Waste_Reason", "Waste_Quantity"}.issubset(datos.columns):
        st.subheader("🔎 Desperdicio según el motivo")

        desperdicio_motivo = (
            datos.groupby("Waste_Reason")["Waste_Quantity"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(9, 4))
        desperdicio_motivo.plot(kind="bar", ax=ax, color="#FFA726")
        ax.set_ylabel("Unidades desperdiciadas")
        ax.set_xlabel("Motivo")
        ax.set_title("Cantidad de desperdicio por motivo")
        ax.tick_params(axis="x", rotation=30)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # --- Gráfico 3: Evolución temporal ---
    if {"Date", "Waste_Quantity"}.issubset(datos.columns):
        st.subheader("📅 Evolución del desperdicio en el tiempo")

        datos["Date"] = pd.to_datetime(datos["Date"], errors="coerce")
        datos_tiempo = datos.dropna(subset=["Date"]).copy()

        datos_tiempo["Mes"] = (
            datos_tiempo["Date"].dt.to_period("M").astype(str)
        )

        desperdicio_mes = (
            datos_tiempo.groupby("Mes")["Waste_Quantity"].sum()
        )

        fig, ax = plt.subplots(figsize=(10, 4))
        desperdicio_mes.plot(kind="line", marker="o", ax=ax, color="#2E7D32")
        ax.set_ylabel("Unidades desperdiciadas")
        ax.set_xlabel("Mes")
        ax.set_title("Evolución mensual del desperdicio")
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

except FileNotFoundError:
    st.error("No se encuentra el archivo food_waste_limpio.csv.")
