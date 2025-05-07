import requests
import re


personajes_almacenados=[]
enemigos_almacenados=[]

def obtener_personaje(ID):
    regex = r"[a-fA-F0-9]{24}"
    patron = re.compile(regex)
    mo = patron.search(ID)
    while not mo:
        ID = input("ID con formato inválido, vuelva a intentarlo: ")
        mo = patron.search(ID)
    personaje = []
    try:
        url = f"https://zelda.fanapis.com/api/characters/{ID}"
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()
        #Se obtienen los datos escenciales de la clave data del diccionario
        #Este proceso no cambia ya que fue realizado desde la primera etapa
        datos_personaje = datos["data"]
        juegos = []
        for juego_url in datos_personaje["appearances"]:
            juegos_respuesta = requests.get(juego_url)
            juego = juegos_respuesta.json()
            datos_juego = juego["data"]
            juego_nombre = datos_juego["name"]
            juegos.append(juego_nombre)

        #Se guardan los datos extraidos en un diccionario único para cada personaje
        #Este proceso no cambia ya que fue realizado desde la primera etapa
        personaje = {
            "name": datos_personaje.get("name"),
            "gender": datos_personaje.get("gender"),
            "race": datos_personaje.get("race"),
            "description": datos_personaje.get("description"),
            "games": juegos
        }
        personajes_almacenados.append(personaje)
        return personaje
    except requests.exceptions.HTTPError:
        print(f"Error: El personaje con id {ID} no existe.")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar a la API: Verifica tu conexion")
    except requests.exceptions.Timeout:
        print("Error: La solicitud tardó demasiado en responder")
    except ValueError:
        print(f"Error: No se pudieron procesar los datos de id {ID}")
    return personaje

def obtener_enemigo(ID):
    regex = r"[a-fA-F0-9]{24}"
    patron = re.compile(regex)
    mo = patron.search(ID)
    while not mo:
        ID = input("ID con formato inválido, vuelva a intentarlo: ")
        mo = patron.search(ID)
    personaje = []
    try:
        url = f"https://zelda.fanapis.com/api/monsters/{ID}"
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()
        #Se obtienen los datos escenciales de la clave data del diccionario
        #Este proceso no cambia ya que fue realizado desde la primera etapa
        datos_enemigo = datos["data"]
        juegos = []
        for juego_url in datos_enemigo["appearances"]:
            juegos_respuesta = requests.get(juego_url)
            juego = juegos_respuesta.json()
            datos_juego = juego["data"]
            juego_nombre = datos_juego["name"]
            juegos.append(juego_nombre)

        #Se guardan los datos extraidos en un diccionario único para cada enemigo
        #Este proceso no cambia ya que fue realizado desde la primera etapa
        enemigo = {
            "name": datos_enemigo.get("name"),
            "race": datos_enemigo.get("race"),
            "description": datos_enemigo.get("description"),
            "games": juegos
        }
        enemigos_almacenados.append(enemigo)
        return enemigo
    except requests.exceptions.HTTPError:
        print(f"Error: El enemigo  con id {ID} no existe.")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar a la API: Verifica tu conexion")
    except requests.exceptions.Timeout:
        print("Error: La solicitud tardó demasiado en responder")
    except ValueError:
        print(f"Error: No se pudieron procesar los datos de id {ID}")
    return enemigo

def guardar_archivos_txt():
    with open("Personajes.txt", "w") as archivo:
        for personaje in personajes_almacenados:
            for clave, valor in personaje.items():
                archivo.write(f"{clave}: {valor}\n")
            archivo.write("\n----------\n")

    with open("Enemigos.txt", "w") as archivo:
        for enemigo in enemigos_almacenados:
            for clave, valor in enemigo.items():
                archivo.write(f"{clave}: {valor}\n")
            archivo.write("\n----------\n")

def menu():
    while True:
        print("---Menú de opciones---\n" \
        "Opción 1: Buscar personaje por ID \n" \
        "Opción 2: Buscar enemigo por ID \n" \
        "Opción 3: Ver la lista de personajes buscados \n" \
        "Opción 4: Ver la lista de enemigos buscados \n" \
        "Opción 5: Guardar y salir")
        
        op=int(input("Ingrese una de las opciones: "))
        if op==1:
            try:
                #Ejemplo de ID: 5f6d186f246bd9a0809d653c, 5f6d186f246bd9a0809d6117
                id_personaje = input("Ingrese el id del personaje: ")
            except ValueError as e:
                print(f"Error en la entrada: {e}. Intentalo de nuevo.")
            personaje=obtener_personaje(id_personaje)
            if personaje:
                for x,y in personaje.items():
                    print(f"{x}: {y}")
            print("")
        elif op==2:
            try:
                #Ejemplo de ID: 5f6d1715a837149f8b47a431, 5f6d1715a837149f8b47a166
                id_enemigo = input("Ingrese el id del enemigo: ")
            except ValueError as e:
                print(f"Error en la entrada: {e}. Intentalo de nuevo.")
            enemigo=obtener_enemigo(id_enemigo)
            if enemigo:
                for x,y in enemigo.items():
                    print(f"{x}: {y}")
            print("")
        elif op==3:
            print("\n---Lista de personajes guardados---")
            for personaje in personajes_almacenados:
                print("\n-Personaje- \n")
                for clave, valor in personaje.items():
                    print(f"{clave}: {valor}")
            print("")
        elif op==4:
            print("\n---Lista de enemigos guardados---")
            for enemigo in enemigos_almacenados:
                print("\n -Enemigo- \n") 
                for clave, valor in enemigo.items():
                    print(f"{clave}: {valor}")

            print("")
        elif op==5:
            guardar_archivos_txt()
            print("\n Gracias por usar el programa! \n")
            break
        else:
            print("\n Opción inválida \n")


if __name__=="__main__":
    menu()

    
    

