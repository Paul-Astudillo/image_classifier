from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for, Response
from PIL import Image
from io import BytesIO
import os
import cv2 as cv
import numpy as np

from efectos import filtro_payaso

app = Flask(__name__)

flag_imagen_recibida = True
flag_imagen_filtro = True
flag_prediccion = True


@app.route('/aplicar_filtro', methods=['POST'])
def aplicar_filtro():
    
    data = request.json
    print(data)
    
    filtro_payaso()
 
    flag_imagen_filtro = True
    
    return jsonify({'status': 'Filtro aplicado'})


@app.route('/')
def index():
    global flag_imagen_recibida
    if flag_imagen_recibida:
        image_src_1 = "static/Images/imagen_recibida_1_original.png"
        image_src_2 = "static/Images/imagen_recibida_1_deteccion.png"
        image_src_3 = "static/Images/imagen_recibida_2_original.png"
        image_src_4 = "static/Images/imagen_recibida_2_prediccion.png"
        mensaje= "Imagen recibida correctamente"
        
        
    else:
        image_src_1 = None
        mensaje = "Esperando imagen..."

    if flag_imagen_filtro:
        image_output = "static/Images/output.png"
    else: 
        image_output = None


    if flag_prediccion:

        texto_prediccion = "static/Images/datos_2.txt"

        with open(texto_prediccion, 'r', encoding='utf-8') as file:
            prediccion = file.read()
    else: 
        prediccion = ""


    return render_template('index.html', mensaje=mensaje,image_src_1=image_src_1,
                           image_src_2=image_src_2,image_src_3=image_src_3,
                           image_src_4=image_src_4,image_output=image_output,prediccion=prediccion)

# Funcion para recibir la imagen, se llama desde la app android
@app.route('/recepcion1original', methods=['POST'])
def recepcion():
    global flag_imagen_recibida

    
    image = request.get_data()
        
    image_path = 'static/Images/imagen_recibida_1_original.png'
        
       
    with Image.open(BytesIO(image)) as img:
        img.save(image_path)
    flag_imagen_recibida = True
    print("imagen recibida")
    # solo para retornar algo
    return  jsonify({'mensaje': 'imagen recibida'})


# Funcion para recibir la imagen, se llama desde la app android
@app.route('/recepcion1deteccion', methods=['GET','POST'])
def recepcion_deteccion():
    global flag_imagen_recibida

    
    image = request.get_data()
    print("LEE el PNG")
            
    image_path = 'static/Images/imagen_recibida_1_deteccion.png'
        
    with Image.open(BytesIO(image)) as img:
        img.save(image_path)
    flag_imagen_recibida = True
    print("imagen recibida")
    # solo para retornar algo
    return  jsonify({'mensaje': 'imagen recibida'})


@app.route('/recepcion1datos', methods=['GET','POST'])
def recepcion_datos_txt():
    global flag_imagen_recibida
    
    text_path = 'static/Images/datos_1.txt'
   
    text_data = request.get_data(as_text=True)
    with open(text_path, 'w') as text_file:
        text_file.write(text_data)
        
    print("Archivo .txt recibido")

    return jsonify({'mensaje': 'archivo .txt recibido'})
    
    
# Funcion para recibir la imagen, se llama desde la app android
@app.route('/recepcion2original', methods=['GET','POST'])
def recepcion_pred_original():
    global flag_imagen_recibida

    #if request.content_type == 'image/png':
    image = request.get_data()
        
    image_path = 'static/Images/imagen_recibida_2_original.png'
    with Image.open(BytesIO(image)) as img:
        img.save(image_path)
    flag_imagen_recibida = True
    print("imagen prediccion recibida")
    # solo para retornar algo
    return  jsonify({'mensaje': 'imagen recibida'})



# Funcion para recibir la imagen, se llama desde la app android
@app.route('/recepcion2prediccion', methods=['GET','POST'])
def recepcion_pred():
    global flag_imagen_recibida

    #if request.content_type == 'image/png':
    image = request.get_data()
        
    image_path = 'static/Images/imagen_recibida_2_prediccion.png'
    with Image.open(BytesIO(image)) as img:
        img.save(image_path)
    flag_imagen_recibida = True
    print("imagen prediccion recibida")
    # solo para retornar algo
    return  jsonify({'mensaje': 'imagen recibida'})


@app.route('/recepcion2datos', methods=['GET','POST'])
def recepcion_datos_prediccion_txt():
    global flag_imagen_recibida
    # Guarda el archivo .txt
    text_path = 'static/Images/datos_2.txt'
    # Guarda el contenido en un archivo
    text_data = request.get_data(as_text=True)
    with open(text_path, 'w') as text_file:
        text_file.write(text_data)
        
    print("Archivo .txt recibido")

    return jsonify({'mensaje': 'archivo .txt recibido'})

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)



if __name__ == '__main__':
   
    app.run(debug=True, host="0.0.0.0")
