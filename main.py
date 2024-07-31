from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for, Response
from PIL import Image
from io import BytesIO
import os
import cv2 as cv
import numpy as np
# import desde efectos.py
#from efectos import removeBackgroud, bordesColor

app = Flask(__name__)

flag_imagen_recibida = True

# origenes para fusionar la imagen
# el video tiene una resolcion de 1920x1080
# la imagen se copia en el punto (1600, 500) 
x_img_o = 1600
y_img_o = 500
# el video de la fuente 2 se copia en (100, 400) 
x_vid_o = 100
y_vid_o = 400



# funcion aplicar filtro

@app.route('/aplicar_filtro', methods=['POST'])
def aplicar_filtro():
    
    data = request.json
    print(data)
    
    imagen_android = cv.imread('static/Images/imagen_recibida.png')

    ancho_img = imagen_android.shape[1]
    alto_img = imagen_android.shape[0]
    
 
    
    
    return jsonify({'status': 'Filtro aplicado'})


@app.route('/')
def index():
    global flag_imagen_recibida
    if flag_imagen_recibida:
        image_src = "static/Images/imagen_recibida.png"
        mensaje = "Imagen recibida correctamente"
    else:
        image_src = None
        mensaje = "Esperando imagen..."

    return render_template('index.html', mensaje=mensaje, image_src=image_src)

# Funcion para recibir la imagen, se llama desde la app android
@app.route('/recepcion', methods=['GET','POST'])
def recepcion():
    global flag_imagen_recibida

    if request.content_type == 'image/png':
        image = request.get_data()
        
        image_path = 'static/Images/imagen_recibida.png'
        with Image.open(BytesIO(image)) as img:
            img.save(image_path)
        flag_imagen_recibida = True
        print("imagen recibida")
    # solo para retornar algo
    return  jsonify({'mensaje': 'imagen recibida'})


@app.route('/recepciontxt', methods=['GET','POST'])
def recepcion_txt():
    global flag_imagen_recibida
    # Guarda el archivo .txt
    text_path = 'static/Images/datos.txt'
    # Guarda el contenido en un archivo
    text_data = request.get_data(as_text=True)
    with open(text_path, 'w') as text_file:
        text_file.write(text_data)
        
    print("Archivo .txt recibido")

    return jsonify({'mensaje': 'archivo .txt recibido'})
    
    

# Funcion para recibir la imagen, se llama desde la app android
@app.route('/recepcionpred', methods=['GET','POST'])
def recepcion_pred():
    global flag_imagen_recibida

    if request.content_type == 'image/png':
        image = request.get_data()
        
        image_path = 'static/Images/prediccion_recibida.png'
        with Image.open(BytesIO(image)) as img:
            img.save(image_path)
        flag_imagen_recibida = True
        print("imagen prediccion recibida")
    # solo para retornar algo
    return  jsonify({'mensaje': 'imagen recibida'})


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)



if __name__ == '__main__':
   
    app.run(debug=True, host="0.0.0.0")
