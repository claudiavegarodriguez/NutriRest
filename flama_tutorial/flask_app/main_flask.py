import csv
import os
from flask import Flask, jsonify, redirect, render_template, request, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flamapy.metamodels.fm_metamodel.transformations import UVLReader, JsonWriter
import flask
import pickle
import uuid

import sys
#sys.path.append('C:/Users/claau/Desktop/TFG')
sys.path.append('C:/Users/Asus/Desktop/TFG')

from database.database import get_ingredient_info,get_nutrients_from_ingredient

import utils
import pandas as pd

#mapeo_ingredientes = pd.read_csv('C:/Users/claau/Desktop/TFG/mapeo_ingredientes.csv')
mapeo_ingredientes = pd.read_csv('C:/Users/Asus/Desktop/TFG/mapeo_ingredientes.csv')
nutrientes_ingredientes = pd.read_csv('C:/Users/Asus/Desktop/TFG/output.csv')

#print(mapeo_ingredientes)
diccionario_ingredientes = dict(zip(mapeo_ingredientes['Ingrediente Modelo'], mapeo_ingredientes['Ingrediente BBDD']))

#fm = UVLReader(r'C:\Users\Asus\Desktop\TFG\flama_tutorial\models\Galerna_ensalada_es.uvl').transform()

# Create the App
app = flask.Flask(__name__,
                  template_folder='templates',
                  static_folder='static',
                  static_url_path='/static')

app.secret_key = 'your_secret_key'
hashed_password = generate_password_hash('1234')

# Configuración del directorio de subida

ALLOWED_EXTENSIONS = {'uvl'}
UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def obtener_clave_por_valor(diccionario, valor):
    for clave, valor_dic in diccionario.items():
        if valor_dic == valor:
            print(valor_dic)
            return clave
    return "Ingrediente no encontrado"

def obtener_informacion_nutricional(csv_path):
    informacion_nutricional = {}
    
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar la cabecera
        
        for row in reader:
            ingrediente = row[0]  # Primera columna: nombre del ingrediente
            nutricion = row[2]    # Tercera columna: información nutricional
            informacion_nutricional[ingrediente] = nutricion
    
    return informacion_nutricional

def mapear_lista_ingredientes(lista_ingredientes):
    ingredientes_modelo = []
    for ingrediente in lista_ingredientes:
        ingrediente_modelo = obtener_clave_por_valor(diccionario_ingredientes,ingrediente)
        ingredientes_modelo.append(ingrediente_modelo)
    return ingredientes_modelo

@app.route('/')
def root():
    return flask.redirect(flask.url_for('home'))

@app.route('/home')
def home():
    return flask.render_template('home.html')

# Ruta para el dueño (login)
@app.route('/dueno', methods=['GET', 'POST'])
def dueno():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Aquí debes validar el usuario y la contraseña
        if username == 'Claudia' and check_password_hash(hashed_password, password):  # Cambia esto por tu lógica de autenticación
            session['user'] = username
            return redirect(url_for('dueno_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

# Ruta para el dashboard del dueño
@app.route('/dueno_dashboard')
def dueno_dashboard():
    if 'user' in session:
        return render_template('dueno_dashboard.html')
    else:
        return redirect(url_for('dueno'))
    

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'user' in session:
        if 'file' not in request.files:
            flash('No se ha seleccionado ningún archivo')
            print("holi 1")
            return redirect(url_for('dueno_dashboard'))
        file = request.files['file']
        if file.filename == '':
            flash('No se ha seleccionado ningún archivo')
            print("holi 2")
            return redirect(url_for('dueno_dashboard'))
        
        if file and allowed_file(file.filename):
            archivo = str(file.filename)
            fm = UVLReader(archivo).transform()
            print("holi 5")

            # Crear un nombre de archivo único
            filename = f"{uuid.uuid4()}.pkl"
            filepath = os.path.join('C:/Users/Asus/Desktop/TFG', filename)
            
            # Guardar el objeto `fm` en un archivo
            with open(filepath, 'wb') as f:
                pickle.dump(fm, f)
            
            # Guardar la ruta del archivo en la sesión
            session['fm_filepath'] = filepath
            return redirect(url_for('index'))
        else:
            flash('Tipo de archivo no permitido')
            print("holi 3")
            return redirect(url_for('dueno_dashboard'))
    else:
        return redirect(url_for('dueno'))
     

@app.route('/restricciones', methods=['GET', 'POST'])
def restricciones():
    restricciones = []

    if request.method == 'POST':
        restricciones = request.form.getlist('restriccion')
        filtros = []
        
        if 'vegano' in restricciones:
            ingredientes_veganos = get_ingredient_info('Vegan', "True", "=")
            if ingredientes_veganos:
                filtros.append(set(ing[0] for ing in ingredientes_veganos))
        
        if 'anemia' in restricciones:
            ingredientes_altos_en_Fe = get_ingredient_info('Iron_Fe', 3.0, ">")
            if ingredientes_altos_en_Fe:
                filtros.append(set(ing[0] for ing in ingredientes_altos_en_Fe))

        if 'bajo_grasas' in restricciones:
            valor_bajo_en_grasa = request.form.get('bajo_grasas_value', type=float)
            ingredientes_bajos_grasa = get_ingredient_info('Total_lipid_fat', valor_bajo_en_grasa, "<")
            if ingredientes_bajos_grasa:
                filtros.append(set(ing[0] for ing in ingredientes_bajos_grasa))

        if 'hipertension' in restricciones:
            ingredientes_bajo_en_sal = get_ingredient_info('Sodium_Na', 1.0, "<")
            if ingredientes_bajo_en_sal:
                filtros.append(set(ing[0] for ing in ingredientes_bajo_en_sal))

        if 'intolerancia_lactosa' in restricciones:
            ingredientes_sin_lactosa = get_ingredient_info('Lactose', 0.0, "=")
            if ingredientes_sin_lactosa:
                filtros.append(set(ing[0] for ing in ingredientes_sin_lactosa))
        
        if 'vegetariano' in restricciones:
            ingredientes_vegetarianos = get_ingredient_info('Vegetarian', "True", "=")
            if ingredientes_vegetarianos:
                filtros.append(set(ing[0] for ing in ingredientes_vegetarianos))
       
        if 'sin_gluten' in restricciones:
            ingredientes_sin_gluten = get_ingredient_info('Gluten_Free', "True", "=")
            if ingredientes_sin_gluten:
                filtros.append(set(ing[0] for ing in ingredientes_sin_gluten))

        if 'alto_contenido_proteico' in restricciones:
            valor_proteina = request.form.get('proteinas_value', type=float)
            ingredientes_altos_en_proteina = get_ingredient_info('Protein', valor_proteina, ">")
            if ingredientes_altos_en_proteina:
                filtros.append(set(ing[0] for ing in ingredientes_altos_en_proteina))

        if 'sugars' in restricciones:
            valor_sugars= request.form.get('sugars_value', type = float)
            ingredientes_con_azucares = get_ingredient_info('Sugars_Total', valor_sugars, "<") ########revisar este nombre por si acaso##########
            if ingredientes_con_azucares:
                filtros.append(set(ing[0] for ing in ingredientes_con_azucares))
        if filtros:
            ingredientes_bdd = set.intersection(*filtros)
            ingredientes_modelo = mapear_lista_ingredientes(list(ingredientes_bdd))
            url_l = url_limpia(ingredientes_modelo)
            print(restricciones)
            return redirect(url_for('index', ingredientes=','.join(url_l), restricciones=restricciones))
        
        return redirect(url_for('index', restricciones=restricciones))
        
    restricciones = request.args.getlist('restricciones')
    print(restricciones)
    return render_template('index.html', restricciones=restricciones)


def url_limpia(ingredientes_con_valores_no_encontrado):
    url_l:list=[]
    for i in ingredientes_con_valores_no_encontrado:
        if i != "Ingrediente no encontrado":
            url_l.append(i)
    return url_l

@app.route('/index')
def index():
    fm_filepath = session.get('fm_filepath')  # Recupera el objeto transformado de la sesión
    if not fm_filepath:
        flash('No se ha procesado ningún archivo.')
        print("holi 4")
        return redirect(url_for('dueno_dashboard'))
    with open(fm_filepath, 'rb') as f:
        fm = pickle.load(f)
    
    filtros_query = request.args.get('ingredientes')
    nutrientes_data = obtener_informacion_nutricional('C:/Users/Asus/Desktop/TFG/output.csv')
    
    if filtros_query:
        ingredientes = filtros_query.split(',')
        map = utils.get_data_from_model(fm, ingredientes)  
    
    else:
        map = utils.get_data_from_model(fm, [])
        #print(map)
    return flask.render_template('index.html', data={'map': map, 'nutrientes_data': nutrientes_data})



# Define la nueva ruta para la página de agradecimiento
@app.route('/', methods=['POST'])
def thank_you():
    ingredientes = [key for key in request.form.keys()]
    return flask.render_template('thank_you.html', ingredientes=ingredientes)


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=5000, debug=True)



""" @app.route('/restricciones', methods=['GET', 'POST'])
def restricciones():
    if request.method == 'POST':
        restricciones = request.form.getlist('restriccion')
        filtros = []

        # Diccionario para asociar restricciones con las funciones de obtención de ingredientes
        restricciones_dict = {
            'vegano': ('Vegan', "True", "="),
            'anemia': ('Iron_Fe', request.form.get('anemia_value', type=float), ">"),
            'bajo_grasas': ('Total_lipid_fat', 10.0, "<"),
            'hipertension': ('Sodium_Na', 1.0, "<")
        }

        for restriccion, (atributo, valor, operador) in restricciones_dict.items():
            if restriccion in restricciones:
                ingredientes = get_ingredient_info(atributo, valor, operador)
                if ingredientes:
                    filtros.append(set(ing[0] for ing in ingredientes))

        if filtros:
            ingredientes_bdd = set.intersection(*filtros)
            if ingredientes_bdd:
                ingredientes_modelo = mapear_lista_ingredientes(list(ingredientes_bdd))
                url_l = url_limpia(ingredientes_modelo)
                return redirect(url_for('index', ingredientes=','.join(url_l), restricciones=restricciones))

        return redirect(url_for('index', restricciones=restricciones))

    return render_template('index.html', restricciones=restricciones)
 """