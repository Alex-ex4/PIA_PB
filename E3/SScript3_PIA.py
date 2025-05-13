import re
import json
from statistics import mode, mean, median, stdev, StatisticsError


def leer_datos(archivo):
    with open(archivo,"r") as file:
        contenido= file.read()
    contenido=contenido.strip()
    secciones=contenido.split("----------")
    datos=[]
    for seccion in secciones:
        if not seccion.strip():
            continue
        diccionario={}
        seccion=seccion.strip()
        lineas=seccion.split("\n")
        for linea in lineas:
            if ": " in linea:
                clave,valor=linea.split(": ",1)
                diccionario[clave.strip()]=valor.strip()
        datos.append(diccionario)
    return datos

def validar_datos(datos):
    patron = re.compile(r"[A-Za-z0-9\s]+")
    for diccionario in datos:
        nombre=diccionario.get("name")
        if not patron.search(nombre):
            print(f"Advertencia: nombre inválido detectado -> {diccionario.get('name')}")
    print("Validación completada.\n")

def estandarizar_datos(diccionario):
    for clave, valor in diccionario.items():
        if type(valor)==str:
            diccionario[clave] = valor.capitalize()
    return diccionario

def contar_juegos(diccionario):
    if "games" in diccionario:
        valor = diccionario["games"]
        try:
            juegos = json.loads(valor)
            if type(juegos)==list:
                diccionario["games_number"] = len(juegos)
            else:
                diccionario["games_number"] = 1 
        except json.JSONDecodeError:
            if valor.strip():
                diccionario["games_number"] = 1
            else:
                diccionario["games_number"] = 0
    return diccionario

def analisis_estadistico(personajes_almacenados, enemigos_almacenados):
    juegos_personajes = []
    for personaje in personajes_almacenados:
        cantidad = personaje.get("games_number")
        juegos_personajes.append(cantidad)

    juegos_enemigos = []
    for enemigo in enemigos_almacenados:
        cantidad = enemigo.get("games_number")
        juegos_enemigos.append(cantidad)

    if juegos_personajes:
        print("\n--- Análisis Estadístico de Personajes ---")
        print(f"Media de apariciones: {mean(juegos_personajes)}")
        print(f"Mediana: {median(juegos_personajes)}")
        try:
            print(f"Moda: {mode(juegos_personajes)}")
        except StatisticsError:
            print("Moda: No hay una moda")
        if len(juegos_personajes) > 1:
            print(f"Desviación estándar: {stdev(juegos_personajes)}")
        else:
            print("Desviación estándar: No se puede calcular con un solo valor")

    
    print("\n--- Análisis Estadístico de Enemigos ---")
    print(f"Media de apariciones: {mean(juegos_enemigos)}")
    print(f"Mediana: {median(juegos_enemigos)}")
    try:
        print(f"Moda: {mode(juegos_enemigos)}")
    except StatisticsError:
        print("Moda: No hay una moda clara")
    if len(juegos_enemigos) > 1:
        print(f"Desviación estándar: {stdev(juegos_enemigos)}")
    else:
        print("Desviación estándar: No se puede calcular con un solo valor")

def main():
    personajes = leer_datos("Personajes.txt")
    enemigos = leer_datos("Enemigos.txt")
    
    print("Validando datos de personajes")
    validar_datos(personajes)

    print("Validando datos de enemigos")
    validar_datos(enemigos)
   
    print("Datos de personajes")
    print(f"{len(personajes)} personaje(s) leído(s).\n")
    for personaje in personajes:
        personaje = estandarizar_datos(personaje)
        personaje = contar_juegos(personaje)
        for x, y in personaje.items():
            print(f"{x} --> {y}")
        print("\n---------------\n")
    
    print("Datos de enemigos")
    print(f"{len(enemigos)} enemigo(s) leído(s).\n")
    for enemigo in enemigos:
        enemigo = estandarizar_datos(enemigo)
        enemigo = contar_juegos(enemigo)
        for x, y in enemigo.items():
            print(f"{x} --> {y}")
        print("\n---------------\n")
    
    analisis_estadistico(personajes, enemigos)

if __name__ == "__main__":
    main()