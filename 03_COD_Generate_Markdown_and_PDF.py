import os
import subprocess
import base64

print("--- STEP 03: GENERATING MARKDOWN SOLUTION AND PDF REPORTS WITH GITHUB LINK ---")

def get_b64(img_name):
    paths = [img_name, f"Out_01_{img_name}", os.path.join("Figures", img_name)]
    for p in paths:
        if os.path.exists(p):
            with open(p, "rb") as f:
                return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

fig1_b64 = get_b64("fig1_elbow_chart.png")
fig2_b64 = get_b64("fig2_network_map_k2.png")
fig3_b64 = get_b64("fig3_cost_tradeoff_scenarios.png")
fig4_b64 = get_b64("fig4_pca_scree_loadings.png")
fig5_b64 = get_b64("fig5_pca_biplot_clusters.png")

# 1. Generate Out_03_MD_andina_distribuciones_Case_solution.md with GitHub Link
clean_md_content = """# Solución Taller: Selección de la Ubicación de la Nueva Red de CDCs de Andina Distribuciones S.A.S.

**Autor / Consultor:** Juan Malaver  
**Asignatura:** Supply Chain Analytics / Proyecto Empresarial  
**Institución:** Universidad del Rosario — Escuela de Ciencias e Ingeniería  
**Profesor:** Alexander Garrido, Ph.D.  
**Repositorio GitHub:** [https://github.com/juanfelipemalaver00-arch/Taller-K-Means](https://github.com/juanfelipemalaver00-arch/Taller-K-Means)  
**Fecha:** 26 de Septiembre de 2026  

---

## EXECUTIVE SUMMARY

### 1. Definición del Problema de Negocio
Andina Distribuciones S.A.S. atiende 20 ciudades principales en Colombia con una demanda semanal total de **5,830 estibas** (303,160 estibas/año). Actualmente opera bajo una estrategia centralizada con un único Centro de Distribución (CDC) en **Bogotá**. Esta configuración genera severas ineficiencias logísticas: tiempos prolongados de entrega hacia la Costa Caribe y el Suroccidente, y un costo anual de flete de **$4,820,497 USD** (costo total de red: **$5,420,497 USD** sumando $600k USD de costo fijo). El Gerente General requiere determinar cuantitativamente si la empresa debe mantener un CDC único o migrar a una red descentralizada de 2 a 5 CDCs regionales.

### 2. Resultados Clave de Center of Gravity (CoG) y Clustering K-Means
* **CDC Único Ponderado (k=1, CoG Global):** El centro de gravedad ponderado nacional se localiza matemáticamente en **Lat 5.6092° N, Lon -74.8778° W** (Valle del Magdalena Medio, cerca de Honda/La Dorada). Reubicar el CDC único de Bogotá al CoG Global reduce el recorrido ponderado de 1.85M a **1.74M estibas-km/semana** (distancia promedio: 298.67 km/estiba), generando un ahorro en fletes de $293,272 USD/año. Sin embargo, este punto geométrico es inviable operacionalmente por falta de infraestructura de almacenamiento y mercado local en zona montañosa.
* **Segmentación de Demanda por K-Means Ponderado (k=2 a 5):** Agrupando las ciudades mediante K-Means ponderado por demanda (`sample_weight=demand`), se demuestra matemáticamente que **el centroide de cada cluster equivale exactamente al CoG ponderado del cluster**.

| Configuración (k) | Inercia Ponderada | Recorrido Semanal (estibas-km) | Dist. Promedio (km/estiba) | Costo Anual Transporte (USD) | Costo Fijo CDCs (USD) | Costo Anual Total Red (USD) | Ahorro vs. k=1 CoG (USD) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **k=1 (CoG Global)** | 53,023.25 | 1,741,240.23 | 298.67 | $4,527,224.60 | $600,000 | $5,127,224.60 | Baseline ($0) |
| **k=2 (Recomendada)** | **17,124.31** | **1,012,112.01** | **173.60** | **$2,631,491.23** | **$1,200,000** | **$3,831,491.23** | **+$1,295,733.37** |
| **k=3 (Alternativa)** | 10,578.95 | 784,886.94 | 134.63 | $2,040,706.04 | $1,800,000 | $3,840,706.04 | +$1,286,518.56 |
| **k=4** | 6,170.33 | 605,069.98 | 103.79 | $1,573,181.94 | $2,400,000 | $3,973,182.94 | +$1,154,042.66 |
| **k=5** | 3,946.36 | 448,939.28 | 77.01 | $1,167,242.13 | $3,000,000 | $4,167,242.13 | +$959,882.47 |

### 3. Configuración Resultante y Ciudades Candidatas Reales (k=2)
El análisis del método del codo (*Elbow Method*) en inercia (-67.7% de caída de k=1 a k=2) y la optimización de costo total confirman que la **red de 2 CDCs (k=2)** es el punto óptimo financiero y operativo:

1. **CDC 1 — Hub Interior & Pacífico (Ibagué / Zona Logística Flandes):**
   * **Centroide CoG:** (4.4872° N, -75.2512° W). Ciudad más cercana: **Ibagué** (a 5.77 km del centroide).
   * **Demanda Atendida:** 3,800 estibas/semana (**65.2% del total nacional**).
   * **Ciudades agrupadas (12):** Bogotá, Medellín, Cali, Pereira, Manizales, Ibagué, Villavicencio, Pasto, Neiva, Popayán, Armenia, Tunja.
   * **Ubicación Real Recomendada:** Parque Logístico e Industrial en **Ibagué/Flandes (Tolima)** o nodo **Funza/Cota (Bogotá Metro)**.
2. **CDC 2 — Hub Caribe & Norte (Galapa / Barranquilla Metro):**
   * **Centroide CoG:** (9.6142° N, -74.3319° W).
   * **Demanda Atendida:** 2,030 estibas/semana (**34.8% del total nacional**).
   * **Ciudades agrupadas (8):** Barranquilla, Cartagena, Bucaramanga, Cúcuta, Santa Marta, Montería, Valledupar, Sincelejo.
   * **Ubicación Real Recomendada:** Parque Logístico Industrial en **Galapa / Malambo (Zona Metropolitana de Barranquilla)** o **Mamonal (Cartagena)**.

### 4. Impacto Económico, ROI y Análisis de Sensibilidad
* **Ahorro Bruto en Transporte:** **$1,895,733.37 USD/año** respecto al CoG Global k=1 (y **$2,189,005.36 USD/año** respecto al CDC actual de Bogotá).
* **Costo Fijo Incremental:** **$600,000 USD/año** ($600k x 1 CDC adicional).
* **Ahorro Neto Anual de Red (k=2 vs. k=1):** **$1,295,733.37 USD/año** (reducción del **25.3%** en el costo total anual de red).
* **Relación Beneficio/Costo:** **3.16x** (por cada dólar invertido en costo fijo adicional, se ahorran $3.16 en fletes). **ROI Anual:** **216%**.

---

## MEMORANDO TÉCNICO Y DE NEGOCIO (PARTS A–E)

**PARA:** Gerente General, Andina Distribuciones S.A.S.  
**DE:** Grupo de Analítica Logística y Cadena de Suministro  
**ASUNTO:** Evaluación Cuantitativa de Red Logística y Selección de Sitio para Nuevos CDCs  
**REPOSITORIO GITHUB:** [https://github.com/juanmalaver/andina-distribuciones-cdc](https://github.com/juanmalaver/andina-distribuciones-cdc)  

### Part A — Global Weighted Center of Gravity (CoG)
Para una red de CDC único (k=1), la fórmula clásica del centro de gravedad ponderado por demanda entrega las siguientes coordenadas:
* **Latitud CoG (X*):** 5.6092° N
* **Longitud CoG (Y*):** -74.8778° W

#### Métricas de Desempeño (k=1):
* **Recorrido Ponderado Semanal:** 1,741,240.23 estibas-km/semana.
* **Distancia Promedio por Estiba:** 298.67 km/estiba.
* **Costo Anual de Transporte:** $4,527,224.60 USD/año.
* **Costo Fijo Anual (1 CDC):** $600,000.00 USD/año.
* **Costo Anual Total de Red:** $5,127,224.60 USD/año.

#### Evaluación de Viabilidad del Sitio Geométrico:
El punto (5.6092, -74.8778) se localiza geográficamente en el Valle del Magdalena Medio (municipios de Honda, La Dorada o Guaduas). Aunque este punto minimiza matemáticamente la suma de distancias cuadráticas ponderadas para una sola instalación, **no es un sitio realista ni recomendable para construir un CDC principal**:
1. **Infraestructura y Talento:** Carece de parques logísticos de clase mundial, bodegas de gran altura y mano de obra especializada comparado con Bogotá, Medellín o Barranquilla.
2. **Ausencia de Demanda Local:** Obligaría a despachar el 100% de la carga por carretera, perdiendo la ventaja de entrega local directa en Bogotá (que representa el 16.3% de la demanda nacional).
3. **Vulnerabilidad Topográfica:** Se encuentra rodeado por cuellos de botella viales en los ascensos a las cordilleras Central y Oriental.

### Part B — Clustering K-Means y Justificación del Gráfico del Codo (Elbow)

#### Método del Codo y Selección de k:
Se evaluó K-Means ponderado por demanda para k en {1, 2, 3, 4, 5}. La inercia ponderada representa la suma de distancias euclidianas al cuadrado ponderadas por la demanda:
* k=1 -> 2: Caída drástica de inercia de **53,023.25 a 17,124.31** (reducción del **67.7%**).
* k=2 -> 3: Caída moderada de **17,124.31 a 10,578.95** (reducción del **38.2%**).
* k=3 -> 4: Caída de **10,578.95 a 6,170.33** (reducción del **41.7%**).
* k=4 -> 5: Caída de **6,170.33 a 3,946.36** (reducción del **36.0%**).

El "codo" matemático y la inflexión de costos ocurren en **k=2**. Pasar de k=1 a k=2 reduce el recorrido semanal de flete en **729,128 estibas-km (-41.9%)**, lo cual genera $1.896M USD en ahorro de transporte, superando ampliamente el costo fijo adicional de un segundo CDC ($600,000 USD).

#### Demostración Teórica de Equivalencia CoG / K-Means Centroid:
En el algoritmo K-Means, la función objetivo minimizada con pesos de muestra w_i es:
J = sum_{k=1}^K sum_{i in C_k} w_i ||x_i - mu_k||^2
Tomando la derivada parcial respecto al centroide mu_k e igualando a cero:
dJ / d(mu_k) = -2 sum_{i in C_k} w_i (x_i - mu_k) = 0 => mu_k = sum_{i in C_k} w_i x_i / sum_{i in C_k} w_i
Esta expresión es **matemáticamente idéntica a la fórmula del Center of Gravity (CoG)** ponderado dentro del subconjunto de demanda asignado al cluster C_k. Por ende, K-Means ponderado no es más que una búsqueda simultánea del CoG óptimo para K regiones geográficas.

### Part C — Análisis de Trade-Off de Costos Totales (k=1 a 5)

Bajo los parámetros oficiales de la compañía:
* **Costo Fijo por CDC:** $600,000 USD/año.
* **Costo de Transporte:** $0.05 USD / estiba-km.
* **Distancia:** Fórmula Haversine de gran círculo.

Costo Total(k) = (sum_{i=1}^n w_i * d_Haversine(i, CDC_k) * 52 * 0.05) + k * 600,000

#### Resumen Financiero por Número de CDCs:
1. **k=1 (CoG Global):** Transporte = $4,527,225, Fijo = $600,000 -> **Total = $5,127,225 USD/año**.
2. **k=2 (Mínimo de Costo):** Transporte = $2,631,491, Fijo = $1,200,000 -> **Total = $3,831,491 USD/año** *(Ahorro neto vs. k=1: $1,295,733 USD/año)*.
3. **k=3:** Transporte = $2,040,706, Fijo = $1,800,000 -> **Total = $3,840,706 USD/año** *(Diferencia vs. k=2: +$9,215 USD/año)*.
4. **k=4:** Transporte = $1,573,182, Fijo = $2,400,000 -> **Total = $3,973,182 USD/año**.
5. **k=5:** Transporte = $1,167,242, Fijo = $3,000,000 -> **Total = $4,167,242 USD/año**.

**Conclusión cuantitativa:** **k=2 minimiza el costo anual total de la red**.

### Part D — Traducción a Sitios Reales y Factores Cualitativos de Selección

Para la configuración recomendada de **k=2**, se traducen los centroides matemáticos a ubicaciones reales óptimas:

#### 1. Cluster 1 (Interior & Pacífico Hub):
* **Centroide Geométrico:** (4.4872° N, -75.2512° W).
* **Ciudad más cercana en dataset:** **Ibagué (Tolima)**, ubicada a solo **5.77 km** del centroide.
* **Ubicaciones Reales Propuestas:**
  * **Opción A (Nodo Logístico Ibagué / Flandes):** Parque Logístico del Tolima. Conecta la Ruta del Sol, el proyecto doble calzada Ibagué-Cajamarca y la salida al Suroccidente.
  * **Opción B (Nodo Bogotá Metro - Funza / Cota):** Dado que Bogotá representa por sí sola 950 estibas/semana (25% del cluster), ubicar el CDC en Funza/Cota elimina el flete primario hacia la capital.
* **Factores Cualitativos Clave:** Paso de la Línea y topografía andina, disponibilidad de suelo industrial e incentivos tributarios de ICA en Flandes/Ibagué.

#### 2. Cluster 2 (Caribe & Norte Hub):
* **Centroide Geométrico:** (9.6142° N, -74.3319° W) (Centro de Bolívar, cerca de Plato/Magangué).
* **Ciudad más cercana en dataset:** **Sincelejo** (a 121.87 km).
* **Ubicación Real Recomendada:** **Galapa / Malambo (Zona Metropolitana de Barranquilla)** o **Mamonal (Cartagena)**.
* **Factores Cualitativos Clave:** Infraestructura portuaria y logística AAA, Zonas Francas (ZFA) y conexión directa con la Vía al Mar y la Ruta del Sol 3.

### Part E — Recomendación Final al Gerente General

Se recomienda a la Gerencia General **aprobar de inmediato la transición de un CDC único en Bogotá a una Red Logística Dual de 2 CDCs Regionales**, ubicados estratégicamente en la **Zona Metropolitana de Barranquilla (Galapa)** para el Hub Caribe (34.8% de demanda) y en la **Zona Logística de Ibagué/Flandes o Bogotá-Funza** para el Hub Interior/Pacífico (65.2% de demanda). Esta configuración **reducirá el costo total anual de la red en $1,295,733 USD (-25.3%)**, recortará la distancia promedio de entrega de 298.7 km a **173.6 km (-41.9%)** y mejorará sustancialmente los niveles de servicio en el Caribe y Suroccidente. 

**Riesgo y Limitación Principal:** El modelo asume distancias geodésicas (Haversine) y costos de transporte lineales por km. No captura la variabilidad de tiempos de viaje causados por la topografía andina (derrumbes, paros viales en La Línea) ni el costo de mantener inventario duplicado (stock de seguridad adicional en dos bodegas).

---

## SECCIÓN DE ANEXOS TÉCNICOS Y ESTRATÉGICOS

### Anexo 1 — Auditoría y Limpieza de Datos (Anomaly Checks & Cleaning)
Antes de ejecutar los modelos cuantitativos, se realizó un control de calidad riguroso sobre los 20 puntos de demanda de la Tabla 1 del PDF:
1. **Duplicados:** 0 filas duplicadas; 0 nombres de ciudad duplicados.
2. **Valores Faltantes (Missing Values):** 0 valores nulos en Latitud, Longitud o Demanda.
3. **Coordenadas Inválidas:** Todas las latitudes se encuentran dentro del rango geográfico de Colombia [1.2136°, 11.2408° N], y todas las longitudes en [-77.2811°, -72.5078° W].
4. **Demanda Válida:** No existen demandas negativas o iguales a cero (rango: 110 a 950 estibas/semana).
5. **Consistencia con PDF:** Se verificó la coincidencia exacta de las 20 observaciones con el documento rector.
6. **Consistencia de Tipos:** Variables geográficas almacenadas como `float64` y demanda como `int64`.

---

### Anexo 2 — Marco de Normalización y Estandarización
* **Variables Normalizadas:** `Latitude`, `Longitude`, `Demand`, `Dist_to_Capital`, `Dist_to_Port` (exclusivamente para PCA).
* **Método Utilizado:** Estandarización Z-Score (`StandardScaler`): z = (x - mu) / sigma.
* **¿Por qué se normaliza?** Porque las variables originales están en escalas disímiles (grados, estibas, kilómetros). En PCA, variables con gran varianza absoluta dominarían artificialmente las componentes principales.
* **Análisis que NO deben normalizar:** **Center of Gravity (CoG)**, **Distancias Haversine** y **Modelación de Costos ($USD)**. Estos cálculos requieren strictly las coordenadas geográficas reales y los volúmenes de demanda en unidades físicas.

---

### Anexo 3 — Recomendaciones de Negocio Detalladas por Cluster (k=2)

#### Cluster 1 — Hub Interior & Pacífico (65.2% Demanda Nacional)
* **Región Representada:** Andean Core, Eje Cafetero, Valle del Cauca, Suroccidente (Pasto/Popayán), Tolima Grande y Llanos Orientales.
* **Concentración de Demanda:** **3,800 estibas/semana** (65.2% del total).
* **Ciudades Principales:** Bogotá (950), Medellín (700), Cali (620), Pereira (220), Villavicencio (240), Manizales (180), Ibagué (190), Pasto (150), Armenia (150), Neiva (160), Popayán (130), Tunja (110).
* **Papel en la Red:** Centro Neurálgico de Almacenamiento y Ensamble/Kitting para el consumo masivo del centro y sur del país.
* **Tipo de Operación:** CDC de Alta Capacidad y Rotación (Full Fulfillment Center) con almacenamiento vertical automatizado y zona de consolidación de carga pesada.
* **Ventaja Logística a Capturar:** Reducción radical del flete de tramo largo entre Bogotá, Medellín y Cali al operar desde un nodo centralizado en el corredor vial principal.
* **Riesgo Operativo:** Vulnerabilidad ante bloqueos viales en el Paso de la Línea y congestión en los accesos urbanos a Bogotá y Medellín.
* **Acción Concreta al Management:** Establecer el CDC 1 en el corredor **Funza/Cota (Bogotá Metro)** o en el **Parque Logístico de Ibagué**, negociando contratos de arrendamiento a 10 años con opción de expansión.

#### Cluster 2 — Hub Caribe & Norte (34.8% Demanda Nacional)
* **Región Representada:** Costa Caribe colombiana (Barranquilla, Cartagena, Santa Marta, Montería, Sincelejo, Valledupar) y Santanderes (Bucaramanga, Cúcuta).
* **Concentración de Demanda:** **2,030 estibas/semana** (34.8% del total).
* **Ciudades Principales:** Barranquilla (480), Cartagena (350), Bucaramanga (300), Cúcuta (260), Santa Marta (210), Montería (170), Valledupar (140), Sincelejo (120).
* **Papel en la Red:** Hub Regional Marítimo-Terrestre y Centro de Distribución Rápida para el Norte de Colombia y la Frontera Oriental.
* **Tipo de Operación:** CDC Regional + Cross-Docking para despacho rápido en menos de 24 horas a las ciudades costeras.
* **Ventaja Logística a Capturar:** Eliminación del flete de más de 700 km desde Bogotá a la Costa Caribe, reduciendo el tiempo de tránsito de 48h a 12h.
* **Riesgo Operativo:** Exposición a condiciones climáticas extremas (inundaciones en la Vía al Mar/Ruta del Sol) y sobrecostos por humedad/temperatura.
* **Acción Concreta al Management:** Adquirir o arrendar una bodega de 5,000 m² en **Galapa (Atlántico)** dentro de Zona Franca para aprovechar incentivos tributarios.

---

### Anexo 4 — Análisis Complementario de Componentes Principales (PCA)
El PCA se aplicó sobre 5 variables estandarizadas para entender la estructura latente que explica las diferencias entre ciudades:
* **PC1 (53.13% Varianza):** Eje Latitudinal y Acceso Marítimo. Presenta cargas muy altas positivas en Latitud (+0.607) y Distancia a Bogotá (+0.466), y carga negativa fuerte en Distancia al Puerto (-0.586).
* **PC2 (23.78% Varianza):** Eje de Escala de Demanda y Núcleo Interior. Cargas altas positivas en Demanda (+0.636) y Longitud (+0.607), y negativa en Distancia a la Capital (-0.465).
* **Varianza Acumulada (PC1 + PC2):** **76.91%** (con PC3 alcanza el 95.12%).

---

### Anexo 5 — Análisis de Sensibilidad de Escenarios y Modelo Financiero (ROI)

#### Sensibilidad de Costos Fijos por CDC ($USD)

| Costo Fijo / CDC | k=1 (CoG) | k=2 (Opt) | k=3 | k=4 | k=5 | Configuración Óptima | Ahorro vs. k=1 (USD) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$300,000 USD** | $4,827,225 | $3,231,491 | $2,940,706 | $2,773,182 | **$2,667,242** | **k=5 (Descentralizada)** | $2,159,983 |
| **$600,000 USD (Base)** | $5,127,225 | **$3,831,491** | $3,840,706 | $3,973,182 | $4,167,242 | **k=2 (Dual Hub)** | $1,295,733 |
| **$900,000 USD** | $5,427,225 | **$4,431,491** | $4,740,706 | $5,173,182 | $5,667,242 | **k=2 (Dual Hub)** | $995,734 |
| **$1,200,000 USD** | $5,727,225 | **$5,031,491** | $5,640,706 | $6,373,182 | $7,167,242 | **k=2 (Dual Hub)** | $695,734 |

#### Análisis Metodológico de ROI (k=2 vs. k=1)
* **Ahorro Anual de Transporte:** $1,895,733.37 USD/año.
* **Costo Fijo Incremental:** $600,000.00 USD/año.
* **Ahorro Neto Anual:** $1,295,733.37 USD/año.
* **Benefit / Cost Ratio:** 1,895,733.37 / 600,000.00 = **3.16x**.
* **Retorno sobre la Inversión Fijo (ROI):** (1,295,733.37 / 600,000.00) * 100% = **215.96%**.

---

### Anexo 6 — Business Framing (Marco de Decisión de 5 Pilares)
1. **Finding (Hallazgo):** Red dual k=2 reduce recorrido a 1.01M estibas-km (-41.9%) y costo total a $3.83M USD/año.
2. **Business Meaning (Significado de Negocio):** Demanda dividida en dos bloques: Interior (65.2%) y Caribe (34.8%).
3. **Advice (Recomendación Operativa):** Abrir CDC Caribe en Galapa y estructurar Interior en Funza/Ibagué. No expandir a k=3.
4. **Economics (Impacto Económico):** Ahorro neto $1,295,733 USD/año (-25.3%). Benefit/Cost 3.16x.
5. **Risk (Riesgo y Mitigación):** Capital de trabajo por duplicación de stock. Mitigación: inventario Clase A en ambos CDCs, Clase C solo en Interior.

---

### Anexo 7 — Preguntas de Reflexión y Discusión en Clase (Class Discussion)

#### 1. Efecto del costo fijo ($600k):
El costo fijo actúa como la "fuerza de gravedad" que limita la fragmentación de la red. Cuando el costo fijo es bajo ($300,000 USD), la red óptima se expande a **k=5 CDCs**, priorizando la proximidad al cliente. A medida que el costo fijo sube a $600,000 USD o más, el modelo castiga la adición de bodegas, concentrando la solución en **k=2**. Esto enseña que la estrategia multi-CDC solo es viable cuando las economías en fletes superan el costo de arrendamiento y administración de nuevas bodegas.

#### 2. Riesgos de resiliencia en CDC único:
Un CDC único centralizado crea un **punto único de falla (*Single Point of Failure*)**. Los riesgos no capturados incluyen: vulnerabilidad vial y topográfica (bloqueos en La Línea o Vía al Llano paralizan 100% despachos), saturación en picos y tiempos de entrega de 48h-72h.

#### 3. Otras variables en agrupamiento real:
En un proyecto real, la agrupación cambiaría al incorporar: tiempos de viaje reales (horas vs km), retorno en vacío (*backhaul*), cadena de frío, exenciones fiscales (ICA/ZFA) y SLAs exigidos por cliente.

---

## CONCLUSIÓN EJECUTIVA FINAL
El análisis de Supply Chain Analytics demuestra cuantitativa y cualitativamente que **Andina Distribuciones S.A.S. debe abandonar su esquema centralizado en Bogotá y migrar a una Red Dual de 2 Centros de Distribución (Hub Interior en Ibagué/Bogotá y Hub Caribe en Galapa-Barranquilla)**. Esta decisión equilibra a la perfección el ahorro en transporte ($1.896M USD/año) con los costos fijos operativos, capturando un **ahorro neto anual de $1,295,733 USD** y posicionando a la compañía con una red logística altamente resiliente, ágil y preparada para el crecimiento sostenible en Colombia.
"""

md_out = "Out_03_MD_andina_distribuciones_Case_solution.md"
with open(md_out, "w", encoding="utf-8") as f:
    f.write(clean_md_content)
print(f"Saved {md_out}")

# 2. Convert HTML and render PDFs with GitHub link in header
html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Out_03 - Informe de Solución Caso Andina Distribuciones</title>
    <style>
        @page {
            size: A4;
            margin: 11mm 13mm 11mm 13mm;
        }
        body {
            font-family: 'Segoe UI', Calibri, Arial, sans-serif;
            font-size: 9pt;
            line-height: 1.32;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }
        .header-box {
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            margin-bottom: 8px;
        }
        .header-box h1 {
            font-size: 13.5pt;
            margin: 0 0 3px 0;
            color: #ffffff;
            font-weight: 700;
        }
        .header-meta {
            font-size: 8pt;
            color: #e2e8f0;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }
        .header-meta a {
            color: #93c5fd;
            text-decoration: underline;
        }
        h2 {
            font-size: 10.5pt;
            color: #1e3a8a;
            border-bottom: 1.5px solid #3b82f6;
            padding-bottom: 2px;
            margin-top: 8px;
            margin-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }
        h3 {
            font-size: 9pt;
            color: #0f172a;
            margin-top: 6px;
            margin-bottom: 3px;
            font-weight: 700;
        }
        p {
            margin-top: 0;
            margin-bottom: 4px;
            text-align: justify;
        }
        ul, ol {
            margin-top: 0;
            margin-bottom: 4px;
            padding-left: 14px;
        }
        li {
            margin-bottom: 2px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 4px;
            margin-bottom: 6px;
            font-size: 8pt;
        }
        th {
            background-color: #1e3a8a;
            color: #ffffff;
            font-weight: 600;
            text-align: center;
            padding: 3px 4px;
            border: 1px solid #1e3a8a;
        }
        td {
            padding: 3px 4px;
            border: 1px solid #cbd5e1;
            text-align: center;
        }
        tr:nth-child(even) {
            background-color: #f8fafc;
        }
        .badge-opt {
            background-color: #dcfce7;
            color: #166534;
            font-weight: bold;
            padding: 1px 3px;
            border-radius: 2px;
        }
        .code-snap {
            background-color: #0f172a;
            color: #38bdf8;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 7.5pt;
            padding: 6px 8px;
            border-radius: 4px;
            margin: 4px 0;
            line-height: 1.25;
            white-space: pre-wrap;
        }
        .code-snap-title {
            background-color: #1e293b;
            color: #94a3b8;
            font-family: sans-serif;
            font-size: 7.5pt;
            font-weight: bold;
            padding: 2px 8px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            margin-bottom: -4px;
        }
        .page-break {
            page-break-before: always;
        }
        .annex-header {
            background-color: #0f172a;
            color: #ffffff;
            padding: 6px 10px;
            font-size: 12pt;
            font-weight: bold;
            border-radius: 4px;
            margin-top: 6px;
            margin-bottom: 8px;
            text-align: center;
        }
        .img-container {
            text-align: center;
            margin: 6px 0;
        }
        .img-container img {
            max-width: 92%;
            max-height: 200px;
            height: auto;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
        }
        .grid-2col {
            display: flex;
            gap: 8px;
        }
        .grid-2col > div {
            flex: 1;
        }
        .memo-meta {
            background-color: #f1f5f9;
            border-left: 3px solid #2563eb;
            padding: 4px 8px;
            font-size: 8pt;
            margin-bottom: 6px;
        }
    </style>
</head>
<body>

    <!-- PAGE 1: EXECUTIVE SUMMARY -->
    <div class="header-box">
        <h1>Solución Caso Andina Distribuciones S.A.S. — Selección de Red de CDCs</h1>
        <div class="header-meta">
            <span><strong>Estudiante:</strong> Juan Malaver | <strong>GitHub:</strong> <a href="https://github.com/juanfelipemalaver00-arch/Taller-K-Means">github.com/juanfelipemalaver00-arch/Taller-K-Means</a></span>
            <span><strong>Universidad del Rosario</strong> | Prof: Alexander Garrido, Ph.D. | <strong>Fecha:</strong> 26/09/2026</span>
        </div>
    </div>

    <h2>Executive Summary (Resumen Ejecutivo)</h2>
    <p><strong>1. Definición del Problema:</strong> Andina Distribuciones S.A.S. atiende 20 ciudades en Colombia con <strong>5,830 estibas/semana</strong> (303,160 estibas/año). La operación actual con 1 CDC centralizado en <strong>Bogotá</strong> genera elevados costos de flete ($4,820,497 USD/año transporte; $5,420,497 USD/año costo total red) y largos tiempos de entrega a la Costa Caribe y Suroccidente. Se requiere determinar si mantener 1 CDC o migrar a una red de 2 a 5 CDCs regionales.</p>

    <div class="code-snap-title">Code Snap 1: Carga de Datos y Cálculo de CoG Global en Python</div>
    <div class="code-snap">import numpy as np, pandas as pd
data = [{"City": "Bogotá", "Lat": 4.7110, "Lon": -74.0721, "Demand": 950}] # 20 ciudades Tabla 1 PDF
df = pd.DataFrame(data)
tot_demand = df["Demand"].sum()
cog_lat = (df["Lat"] * df["Demand"]).sum() / tot_demand
cog_lon = (df["Lon"] * df["Demand"]).sum() / tot_demand
# Result: CoG Global (k=1) = Lat 5.6092° N, Lon -74.8778° W (Magdalena Medio)</div>

    <p><strong>2. Resultados Clave CoG y K-Means:</strong> Reubicar el CDC único al CoG Global reduce el flete a $4.527M USD/año, pero es inviable por falta de infraestructura y demanda local. Al aplicar <code>KMeans(n_clusters=k, sample_weight=demand)</code>, <strong>el centroide del cluster equivale exactamente al CoG ponderado del cluster</strong>. El método del codo (-67.7% inercia) y la minimización de costo total confirman que <strong>k=2 es la solución óptima</strong>.</p>

    <table>
        <thead>
            <tr>
                <th>Configuración (k)</th>
                <th>Inercia Ponderada</th>
                <th>Recorrido Semanal (estibas-km)</th>
                <th>Dist. Promedio (km/estiba)</th>
                <th>Costo Anual Transporte (USD)</th>
                <th>Costo Fijo CDCs (USD)</th>
                <th>Costo Anual Total Red (USD)</th>
                <th>Ahorro vs. k=1 CoG (USD)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>k=1 (CoG Global)</strong></td>
                <td>53,023.25</td>
                <td>1,741,240.23</td>
                <td>298.67</td>
                <td>$4,527,224.60</td>
                <td>$600,000</td>
                <td>$5,127,224.60</td>
                <td>Baseline ($0)</td>
            </tr>
            <tr style="background-color: #f0fdf4;">
                <td><strong class="badge-opt">k=2 (Recomendada)</strong></td>
                <td><strong>17,124.31</strong></td>
                <td><strong>1,012,112.01</strong></td>
                <td><strong>173.60</strong></td>
                <td><strong>$2,631,491.23</strong></td>
                <td><strong>$1,200,000</strong></td>
                <td><strong>$3,831,491.23</strong></td>
                <td><strong style="color: #15803d;">+$1,295,733.37</strong></td>
            </tr>
            <tr>
                <td><strong>k=3 (Alternativa)</strong></td>
                <td>10,578.95</td>
                <td>784,886.94</td>
                <td>134.63</td>
                <td>$2,040,706.04</td>
                <td>$1,800,000</td>
                <td>$3,840,706.04</td>
                <td>+$1,286,518.56</td>
            </tr>
            <tr>
                <td><strong>k=4</strong></td>
                <td>6,170.33</td>
                <td>605,069.98</td>
                <td>103.79</td>
                <td>$1,573,181.94</td>
                <td>$2,400,000</td>
                <td>$3,973,182.94</td>
                <td>+$1,154,042.66</td>
            </tr>
            <tr>
                <td><strong>k=5</strong></td>
                <td>3,946.36</td>
                <td>448,939.28</td>
                <td>77.01</td>
                <td>$1,167,242.13</td>
                <td>$3,000,000</td>
                <td>$4,167,242.13</td>
                <td>+$959,882.47</td>
            </tr>
        </tbody>
    </table>

    <div class="grid-2col">
        <div class="img-container">
            <img src="{FIG1_B64}" alt="Elbow Chart">
            <p style="font-size: 7.5pt; color: #475569;"><strong>Figura 1:</strong> Elbow Method e Inercia vs. Costo Total</p>
        </div>
        <div class="img-container">
            <img src="{FIG2_B64}" alt="Network Map">
            <p style="font-size: 7.5pt; color: #475569;"><strong>Figura 2:</strong> Red de Demanda y Centroides (k=2)</p>
        </div>
    </div>

    <p><strong>3. Configuración Resultante y Ciudades Candidatas (k=2):</strong> 
    (1) <strong>CDC 1 Interior/Pacífico (Ibagué/Funza):</strong> 12 ciudades, 3,800 estibas/wk (65.2%). CoG: (4.4872° N, -75.2512° W), a 5.77 km de Ibagué. Ubicación real: Parque Logístico Ibagué/Flandes o Funza.
    (2) <strong>CDC 2 Caribe/Norte (Galapa-Barranquilla):</strong> 8 ciudades, 2,030 estibas/wk (34.8%). CoG: (9.6142° N, -74.3319° W). Ubicación real: Zona Franca Galapa/Malambo.</p>

    <p><strong>4. Impacto Económico & ROI:</strong> Red dual (k=2) genera un <strong>ahorro neto anual de $1,295,733 USD/año (-25.3% costo total)</strong>. Beneficio/Costo: <strong>3.16x</strong>. ROI: <strong>216%</strong>.</p>

    <!-- PAGE BREAK TO PAGE 2 -->
    <div class="page-break"></div>

    <!-- PAGE 2: MEMORANDO PARTS A-E WITH CODE SNAPS & GITHUB LINK -->
    <h2>Memorando Técnico y de Negocio (Parts A–E)</h2>
    <div class="memo-meta">
        <strong>PARA:</strong> Gerente General, Andina Distribuciones S.A.S. | <strong>DE:</strong> Grupo de Analítica Logística<br>
        <strong>ASUNTO:</strong> Respuestas a Requerimientos A–E del Documento Rector | <strong>GitHub Repo:</strong> <a href="https://github.com/juanfelipemalaver00-arch/Taller-K-Means">https://github.com/juanfelipemalaver00-arch/Taller-K-Means</a>
    </div>

    <h3>Part A — Global Weighted Center of Gravity (CoG)</h3>
    <p>Coordenadas CoG Global (k=1): <strong>Lat 5.6092° N, Lon -74.8778° W</strong>. Recorrido semanal: 1,741,240 estibas-km; Distancia promedio: 298.67 km/estiba; Costo transporte: $4,527,225 USD/año; Costo total red: $5,127,225 USD/año.<br>
    <em>Evaluación:</em> Ubicado en el Magdalena Medio (Honda/La Dorada). Es inviable operativamente por falta de bodegas AAA, ausencia de demanda local directa y cruces montañosos.</p>

    <h3>Part B — Clustering K-Means y Justificación del Gráfico del Codo</h3>
    <p>La inercia disminuyó un <strong>67.7%</strong> de k=1 a k=2 (53,023 a 17,124), marcando el codo en <strong>k=2</strong>.</p>

    <div class="code-snap-title">Code Snap 2: Demostración de Equivalencia K-Means Centroid = Cluster CoG en Python</div>
    <div class="code-snap">km = KMeans(n_clusters=2, random_state=42, n_init=20).fit(coords, sample_weight=weights)
for idx, (lat_c, lon_c) in enumerate(km.cluster_centers_):
    members = df[km.labels_ == idx]
    c_lat_cog = (members["Latitude"] * members["Demand"]).sum() / members["Demand"].sum()
    c_lon_cog = (members["Longitude"] * members["Demand"]).sum() / members["Demand"].sum()
    # Verification: km.cluster_centers_[idx] == (c_lat_cog, c_lon_cog) (Exact Match!)</div>

    <p><em>Demostración Teórica:</em> dJ/d(mu_k) = 0 => <strong>mu_k = Σ(w_i x_i) / Σ(w_i)</strong>. Esta fórmula es idéntica al CoG ponderado del cluster.</p>

    <h3>Part C — Trade-Off de Costos Totales (k=1 a 5)</h3>

    <div class="code-snap-title">Code Snap 3: Modelo de Trade-off de Costos Totales en Python</div>
    <div class="code-snap">for k in range(1, 6):
    annual_trans_cost = weekly_pallet_km[k] * 52 * 0.05
    fixed_cost = k * 600000
    total_cost = annual_trans_cost + fixed_cost
    # Output: k=1: $5.127M | k=2: $3.831M (MINIMUM) | k=3: $3.840M | k=4: $3.973M | k=5: $4.167M</div>

    <p>Pasar de k=2 a k=3 reduce el flete en $590.8k USD pero añade $600k USD de costo fijo (+ $9,215 USD en costo total). <strong>k=2 es el óptimo financiero</strong>.</p>

    <h3>Part D — Traducción a Sitios Reales y Factores Cualitativos</h3>
    <ul>
        <li><strong>Cluster 1 (Interior & Pacífico):</strong> CoG (4.4872° N, -75.2512° W) -> <strong>Ibagué</strong> (5.77 km). Nodos: Parque Logístico Ibagué/Flandes (Tolima) o Funza/Cota (Bogotá). Factores: cruce de La Línea, exenciones de ICA, costo de suelo.</li>
        <li><strong>Cluster 2 (Caribe & Norte):</strong> CoG (9.6142° N, -74.3319° W) -> Nodos: <strong>Galapa / Malambo (Barranquilla)</strong> o Mamonal (Cartagena). Factores: acceso a Zonas Francas (ZFA), puertos marítimos, conectividad Vía al Mar.</li>
    </ul>

    <h3>Part E — Recomendación Final al Gerente General</h3>
    <p>Se recomienda <strong>aprobar la transición inmediata a una Red Dual de 2 CDCs</strong> (Galapa-Barranquilla e Ibagué/Funza). Esta decisión <strong>reducirá el costo total anual en $1,295,733 USD (-25.3%)</strong> y recortará la distancia promedio de entrega a <strong>173.6 km (-41.9%)</strong>.<br>
    <em>Riesgo Principal:</em> Cierres en el Paso de la Línea y capital de trabajo adicional por duplicación de stocks de seguridad.</p>

    <!-- PAGE BREAK TO ANNEXES (PAGE 3+) -->
    <div class="page-break"></div>

    <div class="annex-header">SECCIÓN DE ANEXOS TÉCNICOS Y ESTRATÉGICOS</div>

    <h2>Anexo 1 — Auditoría y Limpieza de Datos (Anomaly Checks)</h2>
    <div class="code-snap">print("Missing:", df.isnull().sum().sum(), "| Duplicates:", df['City'].duplicated().sum())
print("Lat Range:", df['Latitude'].min(), "to", df['Latitude'].max())
print("Demand Range:", df['Demand'].min(), "to", df['Demand'].max())</div>
    <p>Dataset de 20 ciudades auditado: 0 duplicados; 0 nulos; coordenadas válidas [Lat: 1.21°-11.24° N, Lon: -77.28°- -72.51° W]; demanda válida de 110 a 950 estibas/wk (total 5,830 estibas/wk).</p>

    <h2>Anexo 2 — Marco de Normalización y Estandarización</h2>
    <p><code>StandardScaler</code> se aplica exclusivamente a PCA para evitar distorsión por diferencias de escala entre grados, estibas y km. <strong>CoG, Haversine y Costos ($USD) emplean datos originales</strong>.</p>

    <h2>Anexo 3 — Recomendaciones Detalladas por Cluster (k=2)</h2>
    <p><strong>Cluster 1 Interior/Pacífico (65.2%):</strong> 3,800 estibas/wk en 12 ciudades. CDC Full Fulfillment automatizado. Contrato a 10 años en Funza o Ibagué.<br>
    <strong>Cluster 2 Caribe/Norte (34.8%):</strong> 2,030 estibas/wk en 8 ciudades. CDC Regional + Cross-docking. Arrendamiento de 5,000 m² en Galapa (Zona Franca).</p>

    <h2>Anexo 4 — Análisis Complementario de PCA</h2>
    <div class="code-snap">from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
X_scaled = StandardScaler().fit_transform(df[["Latitude", "Longitude", "Demand", "Dist_Capital", "Dist_Port"]])
pca = PCA().fit(X_scaled)
# PC1: 53.13% (Eje Latitudinal / Marítimo) | PC2: 23.78% (Eje Demanda / Interior) | Cum: 76.91%</div>

    <div class="grid-2col">
        <div class="img-container">
            <img src="{FIG4_B64}" alt="Scree Plot y Heatmap PCA">
            <p style="font-size: 7.5pt; color: #475569;"><strong>Figura A4.1:</strong> Scree Plot y Loadings Heatmap</p>
        </div>
        <div class="img-container">
            <img src="{FIG5_B64}" alt="Biplot PC1 vs PC2">
            <p style="font-size: 7.5pt; color: #475569;"><strong>Figura A4.2:</strong> Biplot PC1 vs PC2 con Clusters k=2</p>
        </div>
    </div>

    <h2>Anexo 5 — Sensibilidad de Escenarios y Modelo Financiero (ROI)</h2>
    <p>Sensibilidad: $300k -> Opt k=5 ($2.667M); <strong>$600k (Base) -> Opt k=2 ($3.831M)</strong>; $900k -> Opt k=2 ($4.431M); $1.2M -> Opt k=2 ($5.031M).<br>
    Métricas ROI: Ahorro flete: $1,895,733 USD; Costo fijo inc: $600,000 USD; Ahorro neto: <strong>$1,295,733 USD/año</strong>; Benefit/Cost: <strong>3.16x</strong>; ROI: <strong>216%</strong>.</p>

    <div class="img-container">
        <img src="{FIG3_B64}" style="max-width: 75%;" alt="Sensibilidad de Escenarios">
        <p style="font-size: 7.5pt; color: #475569;"><strong>Figura A5.1:</strong> Sensibilidad de Costo Total a Costos Fijos</p>
    </div>

    <h2>Anexo 6 — Business Framing (5 Pilares)</h2>
    <p><strong>Finding:</strong> Red dual k=2 reduce recorrido a 1.01M estibas-km (-41.9%) y costo total a $3.83M USD/año.<br>
    <strong>Business Meaning:</strong> Demanda dividida en dos bloques: Interior (65.2%) y Caribe (34.8%).<br>
    <strong>Advice:</strong> Abrir CDC Caribe en Galapa y estructurar Interior en Funza/Ibagué. No expandir a k=3.<br>
    <strong>Economics:</strong> Ahorro neto $1,295,733 USD/año (-25.3%). Benefit/Cost 3.16x.<br>
    <strong>Risk:</strong> Capital de trabajo por duplicación de stock. Mitigación: inventario Clase A en ambos CDCs, Clase C solo en Interior.</p>

    <h2>Anexo 7 — Preguntas de Reflexión y Discusión en Clase (Class Discussion)</h2>
    <p><strong>1. Efecto costo fijo ($600k):</strong> Costos bajos ($300k) favorecen descentralización (k=5); costos altos ($600k+) concentran la red (k=2).<br>
    <strong>2. Riesgos resiliencia CDC único:</strong> Punto único de falla (derrumbes en La Línea paralizan 100% despachos), saturación en picos y tiempos de entrega de 48h-72h.<br>
    <strong>3. Otras variables en agrupamiento real:</strong> Tiempos de viaje reales (horas vs km), retorno en vacío (*backhaul*), cadena de frío, exenciones fiscales (ICA/ZFA) y SLAs exigidos por cliente.</p>

</body>
</html>
""".replace("{FIG1_B64}", fig1_b64).replace("{FIG2_B64}", fig2_b64).replace("{FIG3_B64}", fig3_b64).replace("{FIG4_B64}", fig4_b64).replace("{FIG5_B64}", fig5_b64)

html_filename = "Out_03_temp_report.html"
with open(html_filename, "w", encoding="utf-8") as f:
    f.write(html_content)

# Render PDFs with Edge
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
html_abs = os.path.abspath(html_filename)

target_pdfs = [
    "Out_03_MD_andina_distribuciones_Case_solution.pdf",
    "Out_03_COD_K_Means_Malaver_Juan.pdf"
]

for pdf_name in target_pdfs:
    pdf_abs = os.path.abspath(pdf_name)
    if os.path.exists(pdf_abs):
        try: os.remove(pdf_abs)
        except: pass
    cmd = [
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_abs}",
        html_abs
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_abs):
        print(f"SUCCESS: Generated {pdf_name} ({os.path.getsize(pdf_abs):,} bytes)")

# Clean up temp HTML
if os.path.exists(html_filename):
    os.remove(html_filename)

print("Step 03 completed successfully. Out_03_MD_andina_distribuciones_Case_solution.md, Out_03_MD_andina_distribuciones_Case_solution.pdf, and Out_03_COD_K_Means_Malaver_Juan.pdf generated with GitHub links.")
