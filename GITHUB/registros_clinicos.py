import pandas as pd

# 1. CARGA DE DATOS
df = pd.read_csv('registros_clinicos.csv')

# 2. LIMPIEZA DE DATOS 
df["Costo_Insumos"] = df["Costo_Insumos"].astype(str).str.replace(r"[\$\.]", "", regex=True).astype(float)

# Convertimos la fecha de ingreso a formato tiempo
df["Fecha_Ingreso"] = pd.to_datetime(df["Fecha_Ingreso"], errors="coerce", dayfirst=True)

# Limpiamos Frecuencia Cardíaca
df["Frecuencia_Cardiaca"] = pd.to_numeric(df["Frecuencia_Cardiaca"], errors="coerce")


# 3. ANÁLISIS MÉDICO/OPERATIVO
patologia_frecuente = df['Patologia'].value_counts()
print("--- PATOLOGÍAS MÁS COMUNES ---")
print(patologia_frecuente.head())

# ¿Qué patología genera, en promedio, la mayor Frecuencia Cardíaca al ingresar?
ritmo_cardiaco_diag = df.groupby('Patologia')['Frecuencia_Cardiaca'].mean().sort_values(ascending=False)
print("\n--- RITMO CARDÍACO PROMEDIO POR PATOLOGÍA ---")
print(ritmo_cardiaco_diag.head())


# 4. ANÁLISIS FINANCIERO
# Costo total y promedio por Patología
finanzas_diag = df.groupby('Patologia')['Costo_Insumos'].agg(['sum', 'mean']).rename(columns={'sum': 'Costo_Total', 'mean': 'Costo_Promedio'})

# Calculamos el porcentaje que gasta cada patología del total del hospital
total_hospital = df['Costo_Insumos'].sum()
finanzas_diag['Porcentaje_Gasto'] = (finanzas_diag['Costo_Total'] / total_hospital) * 100

print("\n--- ANÁLISIS FINANCIERO DE COSTOS ---")
print(finanzas_diag[['Costo_Total', 'Porcentaje_Gasto']].sort_values(by='Costo_Total', ascending=False).head())


# 5. TENDENCIAS DE TIEMPO
df['Mes_Ingreso'] = df['Fecha_Ingreso'].dt.month_name()
ingresos_mensuales = df['Mes_Ingreso'].value_counts()

print("\n--- MESES CON MAYOR CANTIDAD DE INGRESOS ---")
print(ingresos_mensuales.head())