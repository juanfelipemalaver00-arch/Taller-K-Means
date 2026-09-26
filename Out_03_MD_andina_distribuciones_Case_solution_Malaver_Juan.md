# Solución Taller: Selección de la Ubicación de la Nueva Red de CDCs de Andina Distribuciones S.A.S.

**Autor / Consultor:** Juan Malaver  
**Asignatura:** Supply Chain Analytics / Proyecto Empresarial  
**Institución:** Universidad del Rosario — Escuela de Ciencias e Ingeniería  
**Profesor:** Alexander Garrido, Ph.D.  
**Fecha:** 26 de Septiembre de 2026  
**Github Repo para detalles** https://github.com/juanfelipemalaver00-arch/Taller-K-Means


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
* **Análisis que NO deben normalizar:** **Center of Gravity (CoG)**, **Distancias Haversine** y **Modelación de Costos ($USD)**. Estos cálculos requieren estrictamente las coordenadas geográficas reales y los volúmenes de demanda en unidades físicas.

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
---

## CONCLUSIÓN EJECUTIVA FINAL
El análisis de Supply Chain Analytics demuestra cuantitativa y cualitativamente que **Andina Distribuciones S.A.S. debe abandonar su esquema centralizado en Bogotá y migrar a una Red Dual de 2 Centros de Distribución (Hub Interior en Ibagué/Bogotá y Hub Caribe en Galapa-Barranquilla)**. Esta decisión equilibra a la perfección el ahorro en transporte ($1.896M USD/año) con los costos fijos operativos, capturando un **ahorro neto anual de $1,295,733 USD** y posicionando a la compañía con una red logística altamente resiliente, ágil y preparada para el crecimiento sostenible en Colombia.
