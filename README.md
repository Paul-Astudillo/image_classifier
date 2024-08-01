## Proyecto Integrador

## Vision por computador P64

### Autor: Diego Tapia (https://github.com/juandtap), Paul Astudillo (https://github.com/Paul-Astudillo)


### Android App

El codigo de la aplicacion de android se puede encontrar en https://github.com/Paul-Astudillo/ProyectoFinalII

### Servidor Flask para recepción de imágenes

### Parte 1: Detección rasgos faciales

Se recibe la imagen original, la imagen con las detecciones y un archivo de texto plano con las coordenadas de los rasgos faciales, con base en estas coordenadas se colocan iconos de ojos, boca, nariz y película de payaso.

#### Parte 2: Recepción de imágenes y predicción

Con HOG desde la app android se emplea un modelo de clasificación de prendas de vestir, esta envía al servidor la imagen y la predicción (en un archivo de texto) y se la muestra en la interfaz web

### Endpoints:

    1 ```/recepcion1original```
    2 ```/recepcion1deteccion```
    3 ```/recepcion1datos```
    4 ```/recepcion2original```
    5 ```/recepcion2prediccion```
    6 ```/recepcion2datos```







