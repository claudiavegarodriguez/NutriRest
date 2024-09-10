import pandas as pd

# Cargar el archivo CSV para revisar su contenido
file_path = 'datos_filtrados_filtrados.csv'
data = pd.read_csv(file_path)

# Mostrar las primeras filas del archivo y las columnas para entender su estructura
print(data.head(), data.columns)

# Agrupar por 'description' y agregar los valores de 'name' y 'nutrient_nbr' en la misma fila
grouped_data = data.groupby('description').agg({
    'name': lambda x: ', '.join(x.unique()),
    'nutrient_nbr': lambda x: ', '.join(map(str, x.unique()))
}).reset_index()

# Mostrar el resultado agrupado
print(grouped_data.head())
