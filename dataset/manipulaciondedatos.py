import csv

def leer_csv(nombre_archivo):
    datos = {}
    with open(nombre_archivo, newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            # Usa el primer elemento de la fila como clave del diccionario
            # y el resto de los elementos como valores
            datos[fila[0]] = {i: v for i, v in enumerate(fila[1:], start=1)}
    return datos

# Llama a la función para leer y parsear el archivo CSV
datos = leer_csv('datos_finales.csv')

# Imprime los datos para verificar que se han leído correctamente
print(datos)

