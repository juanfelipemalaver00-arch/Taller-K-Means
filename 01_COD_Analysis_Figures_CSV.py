import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Configure graphics style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

print("--- STEP 01: RUNNING DATA ANALYSIS, CLUSTERING, PCA & GENERATING FIGURES/CSV ---")

# 1. Raw Data Definition (Table 1 from Instructions.pdf)
data = [
    {"City": "Bogotá", "Latitude": 4.7110, "Longitude": -74.0721, "Demand": 950},
    {"City": "Medellín", "Latitude": 6.2442, "Longitude": -75.5812, "Demand": 700},
    {"City": "Cali", "Latitude": 3.4516, "Longitude": -76.5320, "Demand": 620},
    {"City": "Barranquilla", "Latitude": 10.9639, "Longitude": -74.7964, "Demand": 480},
    {"City": "Cartagena", "Latitude": 10.3910, "Longitude": -75.4794, "Demand": 350},
    {"City": "Bucaramanga", "Latitude": 7.1193, "Longitude": -73.1227, "Demand": 300},
    {"City": "Pereira", "Latitude": 4.8087, "Longitude": -75.6906, "Demand": 220},
    {"City": "Manizales", "Latitude": 5.0689, "Longitude": -75.5174, "Demand": 180},
    {"City": "Cúcuta", "Latitude": 7.8939, "Longitude": -72.5078, "Demand": 260},
    {"City": "Santa Marta", "Latitude": 11.2408, "Longitude": -74.1990, "Demand": 210},
    {"City": "Ibagué", "Latitude": 4.4389, "Longitude": -75.2322, "Demand": 190},
    {"City": "Villavicencio", "Latitude": 4.1420, "Longitude": -73.6266, "Demand": 240},
    {"City": "Pasto", "Latitude": 1.2136, "Longitude": -77.2811, "Demand": 150},
    {"City": "Montería", "Latitude": 8.7479, "Longitude": -75.8814, "Demand": 170},
    {"City": "Neiva", "Latitude": 2.9273, "Longitude": -75.2819, "Demand": 160},
    {"City": "Popayán", "Latitude": 2.4448, "Longitude": -76.6147, "Demand": 130},
    {"City": "Valledupar", "Latitude": 10.4631, "Longitude": -73.2532, "Demand": 140},
    {"City": "Armenia", "Latitude": 4.5339, "Longitude": -75.6811, "Demand": 150},
    {"City": "Sincelejo", "Latitude": 9.3047, "Longitude": -75.3978, "Demand": 120},
    {"City": "Tunja", "Latitude": 5.5353, "Longitude": -73.3678, "Demand": 110}
]

df = pd.DataFrame(data)

# 2. Haversine Distance Function
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0088
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2.0)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2.0)**2
    c = 2.0 * np.arcsin(np.sqrt(a))
    return R * c

# 3. Global Center of Gravity (k=1)
tot_demand = df["Demand"].sum()
cog_lat = (df["Latitude"] * df["Demand"]).sum() / tot_demand
cog_lon = (df["Longitude"] * df["Demand"]).sum() / tot_demand

df["Dist_to_Global_CoG"] = haversine(df["Latitude"], df["Longitude"], cog_lat, cog_lon)
df["Weighted_Dist_Global_CoG"] = df["Dist_to_Global_CoG"] * df["Demand"]

weekly_dist_k1 = df["Weighted_Dist_Global_CoG"].sum()
annual_trans_k1 = weekly_dist_k1 * 52 * 0.05
fixed_k1 = 600000
total_k1 = annual_trans_k1 + fixed_k1

# 4. K-Means Clustering (k=2..5)
coords = df[["Latitude", "Longitude"]].values
weights = df["Demand"].values

results_k = []
results_k.append({
    "k": 1,
    "Type": "Global CoG",
    "Inertia": np.sum(df["Demand"] * ((df["Latitude"] - cog_lat)**2 + (df["Longitude"] - cog_lon)**2)),
    "Weekly_Pallet_Km": weekly_dist_k1,
    "Avg_Dist_Km": weekly_dist_k1 / tot_demand,
    "Annual_Transport_Cost": annual_trans_k1,
    "Fixed_Cost": fixed_k1,
    "Total_Annual_Cost": total_k1
})

centroids_dict = {1: [(cog_lat, cog_lon)]}

for k in range(2, 6):
    km = KMeans(n_clusters=k, random_state=42, n_init=20)
    km.fit(coords, sample_weight=weights)
    df[f"cluster_k{k}"] = km.labels_
    centroids_dict[k] = km.cluster_centers_
    
    tot_weighted_dist = 0
    for c_idx in range(k):
        c_mask = (km.labels_ == c_idx)
        c_df = df[c_mask]
        c_lat_cog = (c_df["Latitude"] * c_df["Demand"]).sum() / c_df["Demand"].sum()
        c_lon_cog = (c_df["Longitude"] * c_df["Demand"]).sum() / c_df["Demand"].sum()
        
        dists = haversine(c_df["Latitude"].values, c_df["Longitude"].values, c_lat_cog, c_lon_cog)
        tot_weighted_dist += np.sum(dists * c_df["Demand"].values)
        
    avg_d = tot_weighted_dist / tot_demand
    trans_c = tot_weighted_dist * 52 * 0.05
    fix_c = k * 600000
    tot_c = trans_c + fix_c
    
    results_k.append({
        "k": k,
        "Type": f"K-Means k={k}",
        "Inertia": km.inertia_,
        "Weekly_Pallet_Km": tot_weighted_dist,
        "Avg_Dist_Km": avg_d,
        "Annual_Transport_Cost": trans_c,
        "Fixed_Cost": fix_c,
        "Total_Annual_Cost": tot_c
    })

df_results_k = pd.DataFrame(results_k)
df["selected_cluster"] = df["cluster_k2"]

# 5. PCA Analysis
df["Dist_to_Capital"] = haversine(df["Latitude"], df["Longitude"], 4.7110, -74.0721)
df["Dist_to_Port"] = haversine(df["Latitude"], df["Longitude"], 10.3910, -75.4794)

pca_features = ["Latitude", "Longitude", "Demand", "Dist_to_Capital", "Dist_to_Port"]
X_scaled = StandardScaler().fit_transform(df[pca_features])

pca = PCA()
X_pca = pca.fit_transform(X_scaled)

for i in range(X_pca.shape[1]):
    df[f"PC{i+1}"] = X_pca[:, i]

# Save Out_01_andina_distribuciones_data.csv
csv_out = "Out_01_andina_distribuciones_data.csv"
df.to_csv(csv_out, index=False)
print(f"Saved dataset to {csv_out}")

# --- GENERATE Out_01 FIGURES ---

# Fig 1: Elbow Chart
fig, ax1 = plt.subplots(figsize=(8, 4.8))
color = '#1f77b4'
ax1.set_xlabel('Número de Clusters (k)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Inercia Ponderada', color=color, fontsize=11, fontweight='bold')
ax1.plot(df_results_k['k'], df_results_k['Inertia'], marker='o', color=color, linewidth=2.2, markersize=7)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(df_results_k['k'])

ax2 = ax1.twinx()
color = '#d62728'
ax2.set_ylabel('Costo Anual Total ($USD)', color=color, fontsize=11, fontweight='bold')
ax2.plot(df_results_k['k'], df_results_k['Total_Annual_Cost'], marker='s', color=color, linewidth=2.2, linestyle='--', markersize=7)
ax2.tick_params(axis='y', labelcolor=color)
ax2.yaxis.set_major_formatter('${x:,.0f}')

ax1.axvline(x=2, color='gray', linestyle=':', linewidth=1.5)
ax1.text(2.05, df_results_k.loc[df_results_k['k']==2, 'Inertia'].values[0] + 1500, 'Elbow & Mínimo de Costo (k=2)', fontsize=9, fontweight='bold')
plt.title('Figura 1: Método del Codo y Trade-Off de Costos Totales', fontsize=12, fontweight='bold', pad=12)
fig.tight_layout()
plt.savefig('Out_01_fig1_elbow_chart.png', dpi=300)
plt.close()

# Fig 2: Network Map k=2
fig, ax = plt.subplots(figsize=(8.5, 9.5))
colors = ['#1f77b4', '#ff7f0e']
labels_k2 = {0: 'Cluster 1: Interior & Pacífico (65.2%)', 1: 'Cluster 2: Caribe & Norte (34.8%)'}

for c_idx in range(2):
    c_df = df[df['cluster_k2'] == c_idx]
    ax.scatter(c_df['Longitude'], c_df['Latitude'], s=c_df['Demand']*0.8, color=colors[c_idx], alpha=0.75, edgecolors='black', linewidth=1.2, label=labels_k2[c_idx])
    for _, row in c_df.iterrows():
        ax.annotate(f"{row['City']}\n({row['Demand']}p)", (row['Longitude'], row['Latitude']), fontsize=8, ha='center', va='bottom', xytext=(0, 4), textcoords='offset points', fontweight='bold')

for c_idx, (lat_c, lon_c) in enumerate(centroids_dict[2]):
    ax.scatter(lon_c, lat_c, s=320, color='yellow', marker='*', edgecolors='black', linewidth=1.8, zorder=10)
    ax.annotate(f"CoG {c_idx+1}\n({lat_c:.2f}, {lon_c:.2f})", (lon_c, lat_c), fontsize=8.5, fontweight='bold', ha='right', va='top', bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.85))

ax.scatter(cog_lon, cog_lat, s=280, color='red', marker='X', edgecolors='black', linewidth=1.5, zorder=10, label='CoG Global (k=1)')
ax.set_xlabel('Longitud', fontsize=11, fontweight='bold')
ax.set_ylabel('Latitud', fontsize=11, fontweight='bold')
ax.set_title('Figura 2: Red Geográfica de Demanda y Centroides (k=2)', fontsize=13, fontweight='bold', pad=12)
ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('Out_01_fig2_network_map_k2.png', dpi=300)
plt.close()

# Fig 3: Fixed Cost Sensitivity Scenarios
scenarios = [300000, 600000, 900000, 1200000]
fig, ax = plt.subplots(figsize=(8.5, 5))
styles = ['o-', 's--', '^-.', 'd:']
colors_scen = ['#2ca02c', '#d62728', '#1f77b4', '#9467bd']

for idx, fc in enumerate(scenarios):
    costs = [res['Annual_Transport_Cost'] + res['k'] * fc for res in results_k]
    ax.plot(df_results_k['k'], costs, styles[idx], color=colors_scen[idx], linewidth=2, markersize=6.5, label=f'Costo Fijo = ${fc/1000:,.0f}k / CDC')

ax.set_xlabel('Número de CDCs (k)', fontsize=11, fontweight='bold')
ax.set_ylabel('Costo Anual Total Red ($USD)', fontsize=11, fontweight='bold')
ax.set_xticks(df_results_k['k'])
ax.yaxis.set_major_formatter('${x:,.0f}')
ax.set_title('Figura 3: Sensibilidad de Costo Total a Costos Fijos', fontsize=12, fontweight='bold', pad=12)
ax.legend(loc='upper right', frameon=True, facecolor='white')
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('Out_01_fig3_cost_tradeoff_scenarios.png', dpi=300)
plt.close()

# Fig 4: PCA Scree & Loadings
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
pcs = [f'PC{i+1}' for i in range(len(pca.explained_variance_ratio_))]
var_exp = pca.explained_variance_ratio_ * 100
cum_var = np.cumsum(var_exp)

ax1.bar(pcs, var_exp, color='#1f77b4', alpha=0.7, label='Individual (%)')
ax1.plot(pcs, cum_var, color='#d62728', marker='o', linewidth=2, label='Acumulada (%)')
for i, v in enumerate(var_exp):
    ax1.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=8.5, fontweight='bold')
ax1.set_ylabel('Varianza Explicada (%)', fontsize=10, fontweight='bold')
ax1.set_title('Scree Plot de PCA', fontsize=11, fontweight='bold')
ax1.set_ylim(0, 110)
ax1.legend(loc='center right')
ax1.grid(True, linestyle='--', alpha=0.5)

loadings_df = pd.DataFrame(pca.components_[:3].T, index=pca_features, columns=['PC1', 'PC2', 'PC3'])
sns.heatmap(loadings_df, annot=True, cmap='coolwarm', fmt='.3f', ax=ax2, cbar=True, vmin=-0.8, vmax=0.8, linewidths=0.5)
ax2.set_title('Matriz de Cargas (Loadings PC1–PC3)', fontsize=11, fontweight='bold')

plt.suptitle('Figura 4: Análisis de Componentes Principales (PCA)', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('Out_01_fig4_pca_scree_loadings.png', dpi=300)
plt.close()

# Fig 5: PCA Biplot PC1 vs PC2
fig, ax = plt.subplots(figsize=(8, 5.5))
for c_idx in range(2):
    c_df = df[df['cluster_k2'] == c_idx]
    ax.scatter(c_df['PC1'], c_df['PC2'], s=c_df['Demand']*0.7, color=colors[c_idx], alpha=0.75, edgecolors='black', linewidth=1.2, label=labels_k2[c_idx])
    for _, row in c_df.iterrows():
        ax.annotate(row['City'], (row['PC1'], row['PC2']), fontsize=8, ha='center', va='bottom', xytext=(0, 4), textcoords='offset points')

ax.set_xlabel(f'PC1: Eje Latitudinal / Acceso Marítimo ({pca.explained_variance_ratio_[0]*100:.1f}%)', fontsize=10, fontweight='bold')
ax.set_ylabel(f'PC2: Eje de Escala de Demanda / Interior ({pca.explained_variance_ratio_[1]*100:.1f}%)', fontsize=10, fontweight='bold')
ax.set_title('Figura 5: Biplot PC1 vs PC2 con Clusters K-Means (k=2)', fontsize=12, fontweight='bold', pad=12)
ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax.axvline(0, color='gray', linestyle='--', linewidth=0.8)
ax.legend(loc='upper right', frameon=True, facecolor='white')
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('Out_01_fig5_pca_biplot_clusters.png', dpi=300)
plt.close()

print("Step 01 completed successfully. Generated figures: Out_01_fig1 to Out_01_fig5 and Out_01_andina_distribuciones_data.csv")
