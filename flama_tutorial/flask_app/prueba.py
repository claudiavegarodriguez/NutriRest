import csv
import sqlite3
import sys

import pandas as pd
sys.path.append('C:/Users/Asus/Desktop/TFG')
from flamapy.metamodels.fm_metamodel.transformations import UVLReader, JsonWriter
 

from database.database import get_ingredient_info, get_nutrients_from_ingredient

# fm = UVLReader(r'C:\Users\Asus\Desktop\TFG\flama_tutorial\models\Galerna_ensalada_es.uvl').transform()
# print(fm)
def process_csv(input_csv_path, output_csv_path):
    # Leer el archivo CSV
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        # Obtener los encabezados
        headers = next(reader)
        # Añadir un encabezado para la tercera columna
        headers.append('Nutrients')

        # Preparar los datos procesados
        processed_data = [headers]

        for row in reader:
            # Llamar a la función get_nutrients_from_ingredient con el valor de la segunda columna
            ingredient_name = row[1]
            nutrients = get_nutrients_from_ingredient(ingredient_name)
            # Añadir los nutrientes obtenidos a la fila
            row.append(nutrients)
            # Añadir la fila procesada a la lista de datos procesados
            processed_data.append(row)

    # Escribir los datos procesados en un nuevo archivo CSV
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(processed_data)

# Ejemplo de uso
input_csv_path = 'C:/Users/Asus/Desktop/TFG/mapeo_ingredientes.csv'  # Ruta al archivo CSV de entrada
output_csv_path = 'output.csv'  # Ruta al archivo CSV de salida
process_csv(input_csv_path, output_csv_path)

