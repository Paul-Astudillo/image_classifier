 # en este modulo se aplican los efectos
# se agrega figuras a la imagen recibida desde la app Android

import cv2 
import numpy as np
from deteccion_puntos import get_puntos_rostro

def filtro_payaso():
    
    rostro_path = './static/Images/imagen_recibida_1_original.png' 
    rostro = cv2.imread(rostro_path)

   
    clown_nose_path = './static/assets/clown-nose.png' 
    nariz_payaso = cv2.imread(clown_nose_path , cv2.IMREAD_UNCHANGED)
    clown_eyes_path_left = './static/assets/clown-eyes-left.png'  
    ojos_payaso_left = cv2.imread(clown_eyes_path_left , cv2.IMREAD_UNCHANGED)
    clown_eyes_path_right = './static/assets/clown-eyes-right.png'  
    ojos_payaso_right = cv2.imread(clown_eyes_path_right , cv2.IMREAD_UNCHANGED)

    clown_hair_top_path = './static/assets/clown-hair-top.png'  
    clown_hair_top = cv2.imread(clown_hair_top_path , cv2.IMREAD_UNCHANGED)

    clown_mouth_path = './static/assets/clown-lips.png'  
    clown_mouth = cv2.imread(clown_mouth_path, cv2.IMREAD_UNCHANGED)

    # dimensiones y coordenadas de las partes del rostro
    detecciones = get_puntos_rostro()
    # 0 Face, 1 Eyes, 2 nose, 3 mouth
    nariz_coords = detecciones[2][0][1]
    eyes_coords_left = detecciones[1][0][1]
    
    face_coords = detecciones[0][0][1]

    try:
        eyes_coords_right = detecciones[1][1][1]
    
    except IndexError:
  
        print("no se encontro coordenadas del ojo derecho")
        eyes_coords_right = None

    # algunas detecciones omiten la zono de la boca

    try:
        mouth_coords = detecciones[3][0][1]
   
    except IndexError:
    
        print("no se encontro coordenadas de la boca")
        mouth_coords = None
    
    
    x, y, w, h = nariz_coords

    # redimensionar la imagen de la nariz de payaso
    nariz_payaso_resized = cv2.resize(nariz_payaso, (w, h))
       
    if rostro.shape[2] == 3:
        # convierte la imagen de la nariz a 3 canales si es necesario
        if nariz_payaso_resized.shape[2] == 4:
            nariz_payaso_resized = cv2.cvtColor(nariz_payaso_resized, cv2.COLOR_BGRA2BGR)

    # Crear una ROI en la imagen del rostro
    roi = rostro[y:y+h, x:x+w]
    # crear una mascara y su inversa a partir del canal alfa de la imagen de la nariz de payaso
    nariz_payaso_gray = cv2.cvtColor(nariz_payaso_resized, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(nariz_payaso_gray, 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    
    roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # extraer solo la region de la nariz de payaso
    nariz_fg = cv2.bitwise_and(nariz_payaso_resized, nariz_payaso_resized, mask=mask)

    # copiar la nariz de payaso en la ROI
    dst = cv2.add(roi_bg, nariz_fg)
    rostro[y:y+h, x:x+w] = dst

    # se repite el proceso para el resto de las partes
    # Ojos
    # Ojo Izquierdo
    x, y, w, h = eyes_coords_left
     # Crear una ROI en la imagen del rostro
    roi = rostro[y:y+h, x:x+w]
    
    ojos_payaso_resized = cv2.resize(ojos_payaso_left, (w, h))
    
    if ojos_payaso_resized.shape[2] == 4:
        ojos_payaso_resized = cv2.cvtColor(ojos_payaso_resized, cv2.COLOR_BGRA2BGR)
    
    ojos_payaso_gray = cv2.cvtColor(ojos_payaso_resized, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(ojos_payaso_gray, 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
   
    roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

  
    ojos_fg = cv2.bitwise_and(ojos_payaso_resized, ojos_payaso_resized, mask=mask)

    
    dst = cv2.add(roi_bg, ojos_fg)
    rostro[y:y+h, x:x+w] = dst


    # Ojo derecho
    if eyes_coords_right is not None:

        x, y, w, h = eyes_coords_right
      
        roi = rostro[y:y+h, x:x+w]
        
        ojos_payaso_resized_right = cv2.resize(ojos_payaso_right, (w, h))
       
        if ojos_payaso_resized_right.shape[2] == 4:
            ojos_payaso_resized_right = cv2.cvtColor(ojos_payaso_resized_right, cv2.COLOR_BGRA2BGR)
        
        ojos_payaso_gray = cv2.cvtColor(ojos_payaso_resized_right, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(ojos_payaso_gray, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
       
        roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

        
        ojos_fg_right = cv2.bitwise_and(ojos_payaso_resized_right, ojos_payaso_resized_right, mask=mask)

        
        dst = cv2.add(roi_bg, ojos_fg_right)
        rostro[y:y+h, x:x+w] = dst

     # Cara

    x, y, w, h = face_coords
    
    h = h//2

    y = int (y - (y*0.5))



    roi = rostro[y:y+h, x:x+w]
  
    clown_hair_top_resized = cv2.resize(clown_hair_top, (w, h))
    
    if clown_hair_top_resized.shape[2] == 4:
        clown_hair_top_resized = cv2.cvtColor(clown_hair_top_resized, cv2.COLOR_BGRA2BGR)
  
    clown_hair_top_gray = cv2.cvtColor(clown_hair_top_resized, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(clown_hair_top_gray, 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
   
    roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

   
    clown_hair_fg = cv2.bitwise_and(clown_hair_top_resized, clown_hair_top_resized, mask=mask)

    
    dst = cv2.add(roi_bg, clown_hair_fg)
    rostro[y:y+h, x:x+w] = dst


    # BOCA

    if mouth_coords is not None:

        x, y, w, h = mouth_coords
      
        roi = rostro[y:y+h, x:x+w]
        
        clown_mouth_resized = cv2.resize(clown_mouth, (w, h))
        
        if clown_mouth_resized.shape[2] == 4:
             clown_mouth_resized = cv2.cvtColor( clown_mouth_resized, cv2.COLOR_BGRA2BGR)
        
        boca_payaso_gray = cv2.cvtColor(clown_mouth_resized, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(boca_payaso_gray, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        
        roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

        
        boca_fg = cv2.bitwise_and(clown_mouth_resized, clown_mouth_resized, mask=mask)

        
        dst = cv2.add(roi_bg, boca_fg)
        rostro[y:y+h, x:x+w] = dst

    #mostrar la imagen resultante
    #cv2.imshow('Rostro Payaso', rostro)




    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Guardar la imagen resultante
    cv2.imwrite('./static/Images/output.png', rostro)
    print("imagen filtro guardada")

    

#filtro_payaso()





