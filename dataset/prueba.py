
""" # Leer el archivo CSV con los datos filtrados
datos_filtrados = pd.read_csv('datos_filtrados_sin_duplicados.csv')

# Utilizar pivot_table para consolidar los datos
datos_consolidados = datos_filtrados.pivot_table(index='description', columns='name', values=['unit_name', 'nutrient_nbr'], aggfunc=lambda x: ', '.join(str(v) for v in x))

# Resetear el índice para que 'description' vuelva a ser una columna
datos_consolidados = datos_consolidados.reset_index()
print(datos_consolidados.head())

# Guardar el resultado final en un nuevo archivo CSV
datos_consolidados.to_csv('datos_consolidados.csv', index=False) """

import pandas as pd

 # Leer el archivo CSV con los datos filtrados
datos_filtrados = pd.read_csv('fusion13.csv')

# Filtrar filas que contienen "Ash" o "Nitrogen" en la columna "name"
datos_filtrados_filtrados = datos_filtrados[datos_filtrados['name'].isin(['Water', 'Total lipid (fat)', 'Sugars, Total', 'Protein', 'Nitrogen', 'Phosphorus, P', 'Manganese, Mn', 'Potassium, K', 'Calcium, Ca', 'Sodium, Na', 'Magnesium, Mg', 'Iron, Fe', 'Copper, Cu', 'Zinc, Zn', 
                                                                          'Riboflavin','Niacin','Maltose', 'Glucose', 
                                                                          'Lactose', 'Frutcose', 'Maltose', 'Galactose','Fiber, total dietary', 'Vitamin C, total ascorbic acid', 'Thiamin', 'Vitamin B-6', 'Vitamin E (alpha-tocopherol)', 'Vitamin B-12', 'Vitamin A', 'Vitamin D2', 'Vitamin D4', 
                                                                          'Malic acid', 'Oxalic Acid', 'Citric acid', 'Pyruvic acid'])]

# Guardar el resultado final en un nuevo archivo CSV
datos_filtrados_filtrados.to_csv('datos_filtrados_filtrados.csv', index=False) 
# Leer el archivo CSV con los datos filtrados
# datos_filtrados = pd.read_csv('datos_filtrados_filtrados.csv')

# # Utilizar pivot_table para consolidar los datos
# datos_finales = datos_filtrados.pivot_table(index='description', columns='name', values=['nutrient_nbr'], aggfunc=lambda x: ', '.join(str(v) for v in x))

# # Resetear el índice para que 'description' vuelva a ser una columna
# datos_finales = datos_finales.reset_index()

# # Eliminar el nombre de las columnas después de la pivotación
# datos_finales.columns = datos_finales.columns.droplevel()

# # Guardar el resultado final en un nuevo archivo CSV
# datos_finales.to_csv('datos_finales.csv', index=False)

""" datos_finales = datos_filtrados_filtrados.pivot_table(index='description', columns='name', values=['unit_name', 'nutrient_nbr'], aggfunc=lambda x: ', '.join(str(v) for v in x))

# Resetear el índice para que 'description' vuelva a ser una columna
datos_finales = datos_finales.reset_index()
print(datos_finales.head())

# Guardar el resultado final en un nuevo archivo CSV
datos_finales.to_csv('datos_finales.csv', index=False)  """
