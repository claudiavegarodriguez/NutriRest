import openpyxl
import sqlite3 as sql

DB_PATH = "C:/Users/claau/Desktop/TFG/codigo/database/Ingredientes.db"

def createDB():
    try:
        with sql.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS Ingredientes (
                               Nombre TEXT,
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
                               Vegan BOOLEAN 
                )""")
    except sql.Error as e:
        print("Error al crear la base de datos:", e)

def addValues():
    try:
        workbook = openpyxl.load_workbook('datos_finales.xlsx')
        sheet = workbook.active
        with sql.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            for row in sheet.iter_rows(values_only=True):
                nombre = row[0]
                nutrientes = row[1:]
                cursor.execute("""INSERT INTO Ingredientes (Nombre, Calcium_Ca, Citric_acid, Copper_Cu, Fiber_total_dietary, Galactose, Glucose, Iron_Fe, Lactose, Magnesium_Mg, Malic_acid, Maltose, Manganese_Mn, Niacin, Nitrogen, Phosphorus_P, Potassium_K, Protein, Pyruvic_acid, Riboflavin, Sodium_Na, Sugars_Total, Thiamin, Total_lipid_fat, Vitamin_B_12, Vitamin_B_6, Vitamin_C_total_ascorbic_acid, Vitamin_D4, Vitamin_E_alpha_tocopherol, Water, Zinc_Zn, Vegan) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)""",
                               (nombre, *nutrientes))
    except (sql.Error, FileNotFoundError) as e:
        print("Error al agregar valores a la base de datos:", e)


if __name__ == "__main__":
    createDB()
    addValues()
