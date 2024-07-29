 # en este modulo se aplican los efectos
# se agrega figuras a la imagen recibida desde la app Android

import cv2 
import numpy as np
from deteccion_puntos import get_puntos_rostro

def filtro_payaso():
    # Cargar la imagen del rostro
    rostro_path = './static/Images/imagen_recibida.png' 
    rostro = cv2.imread(rostro_path)

   
    clown_nose_path = './static/assets/clown-nose.png'  # Ruta de la imagen de la nariz de payaso
    nariz_payaso = cv2.imread(clown_nose_path , cv2.IMREAD_UNCHANGED)

    # Dimensiones y coordenadas de la nariz
    detecciones = get_puntos_rostro()
    # 0 Face, 1 Eyes, 2 nose, 3 mouth
    nariz_coords = detecciones[2][0][1]
    
    x, y, w, h = nariz_coords

    # Redimensionar la imagen de la nariz de payaso
    nariz_payaso_resized = cv2.resize(nariz_payaso, (w, h))
        # Asegurarse de que la imagen del rostro tenga 3 canales
    if rostro.shape[2] == 3:
        # Convertir la imagen de la nariz de payaso a 3 canales si es necesario
        if nariz_payaso_resized.shape[2] == 4:
            nariz_payaso_resized = cv2.cvtColor(nariz_payaso_resized, cv2.COLOR_BGRA2BGR)

    # Crear una ROI en la imagen del rostro
    roi = rostro[y:y+h, x:x+w]
    # Crear una máscara y su inversa a partir del canal alfa de la imagen de la nariz de payaso
    nariz_payaso_gray = cv2.cvtColor(nariz_payaso_resized, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(nariz_payaso_gray, 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    # Hacer la región del rostro donde se colocará la nariz negra
    roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # Extraer solo la región de la nariz de payaso
    nariz_fg = cv2.bitwise_and(nariz_payaso_resized, nariz_payaso_resized, mask=mask)

    # Poner la nariz de payaso en la ROI y modificar la imagen del rostro
    dst = cv2.add(roi_bg, nariz_fg)
    rostro[y:y+h, x:x+w] = dst

    # Mostrar la imagen resultante
    cv2.imshow('Rostro con Nariz de Payaso', rostro)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Guardar la imagen resultante
    cv2.imwrite('./static/Images/output.png', rostro)

    

filtro_payaso()





