# proyecto_final
Proyecto Final ImpulsIA

# Proyecto 2: El Rescatista de Alimentos

## Problema
Restaurantes y cafeterías desperdician comida porque no saben con exactitud
cuánta demanda tendrán cada día. Compran o producen de más y lo sobrante se pierde.

## Objetivo
Crear una herramienta que estime cuánto alimento se puede desperdiciar en un día,
según las condiciones de ese día (cantidad comprada, demanda esperada, tipo de
negocio, categoría de alimento, temperatura, clima y promociones).

## ¿Quién se beneficia?
- Dueños y gerentes de restaurantes, cafeterías y supermercados: ahorran dinero al comprar mejor.
- Cocineros y encargados de compras: saben cuánto preparar.
- El medio ambiente: menos comida a la basura.
- Bancos de alimentos y ONG: más excedentes disponibles para donar.

## Dataset
- Archivo: food_waste_dataset.csv
- Contenido: 8.000 registros de inventario de 2025 en 4 tipos de negocio
- Variable a predecir: Waste_Quantity (cantidad desperdiciada, en unidades)


PRIMERAS CONCLUSIONES
Prepared Food es la categoría con más desperdicio (6,65 unidades en promedio), seguida de Bakery (5,03). Dairy es la que menos desperdicia (3,46).
Los supermercados desperdician más unidades (6,69), pero en proporción a lo que compran todos los negocios están parecidos (alrededor de 3,5 %).
Comprar de más es el factor más fuerte: la diferencia entre lo comprado y la demanda tiene correlación de 0,78 con el desperdicio.
La sobreproducción causa el 57 % de todo lo desperdiciado; después vienen productos vencidos (25 %) y baja demanda (11 %).
Con temperatura de almacenamiento alta (más de 15°) el desperdicio promedio es 5,96, frente a 3,80 en frío.
Los días con promoción desperdician menos (3,08 vs. 5,03), y los días lluviosos muestran el mayor desperdicio promedio (10,89), aunque habría que confirmar con más datos si es una relación real.


SOLUCION PROPUESTA
"Rescatista de Alimentos"

Qué hace: una aplicación donde el usuario escribe las condiciones de su día y recibe una estimación de cuánto alimento se desperdiciará.

Datos que se introducen (entradas): Tipo de negocio, categoría de alimento, cantidad comprada, demanda esperada, vida útil (días), temperatura de almacenamiento, clima y si hay promoción.

Qué devuelve (salida): cantidad estimada de desperdicio (unidades).

Modelo: regresión con Scikit-learn (por ejemplo LinearRegression y RandomForestRegressor) entrenada con food_waste_limpio.csv.

Variables que NO usaremos para predecir: Remaining_Stock, Units_Sold, Waste_Reason, Waste_Level y Donation_Made, porque solo se conocen cuando el día ya terminó. Si las usáramos, el modelo "haría trampa".

Herramienta para la app: Streamlit (formularios sencillos en pocas líneas de Python).

Reto extra, recomendaciones según el resultado:

Desperdicio alto con compra mayor a la demanda: reducir la compra del día siguiente.
Temperatura alta: revisar la refrigeración.
Desperdicio alto y productos con poca vida útil: hacer promociones o donar el excedente.
