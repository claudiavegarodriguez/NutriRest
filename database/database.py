import sqlite3 as sql
import csv
import openpyxl

#DB_PATH = "C:/Users/claau/Desktop/TFG/database/Ingredientes.db"
DB_PATH = "C:/Users/Asus/Desktop/TFG/database/Ingredientes.db"
def createDB():
    try:
        with sql.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS Ingredientes (
                               Description TEXT,
                               Calcium_Ca REAL,
                               Citric_acid REAL,
                               Copper_Cu REAL,
                               Fiber_total_dietary REAL,
                               Galactose REAL,
                               Glucose REAL,
                               Iron_Fe REAL,
                               Lactose REAL,
                               Magnesium_Mg REAL,
                               Malic_acid REAL,
                               Maltose REAL,
                               Manganese_Mn REAL,
                               Niacin REAL,
                               Nitrogen REAL,
                               Phosphorus_P REAL,
                               Potassium_K REAL,
                               Protein REAL,
                               Pyruvic_acid REAL,
                               Riboflavin REAL,
                               Sodium_Na REAL,
                               Sugars_Total REAL,
                               Thiamin REAL,
                               Total_lipid_fat REAL,
                               Vitamin_B_12 REAL,
                               Vitamin_B_6 REAL,
                               Vitamin_C_total_ascorbic_acid REAL,
                               Vitamin_D4 REAL,
                               Vitamin_E_alpha_tocopherol REAL,
                               Water REAL,
                               Zinc_Zn REAL,
                               Vegan BOOLEAN,
                               Vegetarian BOOLEAN,
                               Gluten_Free BOOLEAN
                )""")
    except sql.Error as e:
        print("Error al crear la base de datos:", e)

def addValues():
    try:
        # Cargar el archivo Excel
        wb = openpyxl.load_workbook('C:/Users/Asus/Desktop/TFG/cleaned_archivoFinal2.xlsx')
        sheet = wb.active  # Asumimos que los datos están en la primera hoja

        with sql.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            
            # Saltar la cabecera (suponemos que está en la primera fila)
            for fila in sheet.iter_rows(min_row=2, values_only=True):
                # El primer valor de la fila es el nombre del ingrediente
                nombre = fila[0]
                # Los valores restantes son los nutrientes
                nutrientes = fila[1:]
                
                cursor.execute("""INSERT INTO Ingredientes (Description, Calcium_Ca, Citric_acid, Copper_Cu, Fiber_total_dietary, Galactose, Glucose, Iron_Fe, Lactose, Magnesium_Mg, Malic_acid, Maltose, Manganese_Mn, Niacin, Nitrogen, Phosphorus_P, Potassium_K, Protein, Pyruvic_acid, Riboflavin, Sodium_Na, Sugars_Total, Thiamin, Total_lipid_fat, Vitamin_B_12, Vitamin_B_6, Vitamin_C_total_ascorbic_acid, Vitamin_D4, Vitamin_E_alpha_tocopherol, Water, Zinc_Zn, Vegan, Vegetarian, Gluten_Free) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                               (nombre, *nutrientes))

    except (sql.Error, FileNotFoundError, openpyxl.utils.exceptions.InvalidFileException) as e:
        print("Error al agregar valores a la base de datos:", e)

# No olvides cambiar 'archivo.xlsx' por el nombre real de tu archivo Excel.


def get_ingredient_info(filter_column, filter_value, comparison_operator = "="):
    try:
        with sql.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            query = f"SELECT * FROM Ingredientes WHERE {filter_column} {comparison_operator} ?"
            cursor.execute(query, (filter_value,))
            results = cursor.fetchall()
            if results:
                return results
            else:
                return []
    except sql.Error as e:
        print("Error al obtener información del ingrediente:", e)
        return None

def get_nutrients_from_ingredient(ingredient_name):
    try:
        with sql.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            query = """SELECT Vegan, Vegetarian, Gluten_Free, Lactose, Iron_Fe, Sugars_Total, Protein, Sodium_Na, Total_lipid_fat
                       FROM Ingredientes WHERE Description = ?"""
            cursor.execute(query, (ingredient_name,))
            result = cursor.fetchone()
            if result:
                return {
                    "Vegano": result[0],
                    "Vegetariano": result[1],
                    "Sin Gluten": result[2],
                    "Lactosa": result[3],
                    "Hierro": result[4],
                    "Azúcares": result[5],
                    "Proteínas": result[6],
                    "Sal": result[7],
                    "Grasas": result[8]
                }
            else:
                return None
    except sql.Error as e:
        print("Error al obtener los nutrientes del ingrediente:", e)
        return None

if __name__ == "__main__":
    createDB()
    addValues()
