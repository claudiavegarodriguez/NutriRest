import pandas as pd

# Lee el archivo CSV
food_nutrient = pd.read_csv('dataset/food_nutrient.csv')

# Selecciona las columnas deseadas
columnas_deseadas = ["id", "fdc_id", "nutrient_id", "amount"]
food_nutrient = food_nutrient[columnas_deseadas]


food = pd.read_csv('dataset/food.csv')
columnas_deseadas2 = ["fdc_id", "description"]
food = food[columnas_deseadas2]

nutrient = pd.read_csv('dataset/nutrient.csv')


# Unir el primer y segundo archivo basándote en la columna "fdc_id"
fusion_1_2 = pd.merge(food_nutrient, food, left_on='fdc_id', right_on='fdc_id', how='inner')
fusion_1_2.to_csv('fusion12.csv', index=False)

fusion12 = pd.read_csv('fusion12.csv')

fusion_1_3 = pd.merge(fusion12, nutrient, left_on='nutrient_id', right_on='id', how='inner')
fusion_1_3 = fusion_1_3[['description', 'name','amount']]
fusion_1_3 = fusion_1_3.drop_duplicates()
fusion_1_3.to_csv('fusion13.csv', index=False)

# fusion_final = pd.merge(fusion_1_2, fusion_1_3, left_on='fdc_id', right_on='fdc_id', how='inner')
# print(fusion_final.head())
# fusion_final = fusion_final[['description', 'name', 'nutrient_nbr']]


# # Eliminar filas duplicadas
# datos_filtrados_sin_duplicados = fusion_final.drop_duplicates()

# # Guardar el resultado final sin duplicados en un nuevo archivo CSV
# datos_filtrados_sin_duplicados.to_csv('datos_filtrados_sin_duplicados.csv', index=False)












# Unir el resultado anterior con el tercer archivo basándote en la columna "fdc_id"
""" resultado_final = pd.merge(fusion_1_2, archivo3, left_on='description', right_on='name', how='inner')

# Seleccionar las columnas necesarias en el resultado final
resultado_final = resultado_final[['description', 'name', 'unit_name', 'nutrient_nbr']]

# Guardar el resultado final en un nuevo archivo CSV
resultado_final.to_csv('resultado_final.csv', index=False) """


# Tomar una muestra aleatoria del 10% de los datos originales
#muestra_aleatoria = resultado_final.sample(n=10000, random_state=42)
#muestra_aleatoria.to_csv('resultado_final.csv', index=False)


