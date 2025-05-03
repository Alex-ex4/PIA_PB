import requests

def obtener_personaje(ID):
    personaje=[]
    try:
        url = f"https://zelda.fanapis.com/api/characters/{ID}"
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()
        datos_personaje=datos["data"]
        juegos = []
        for juego_url in datos_personaje["appearances"]:
            juegos_respuesta = requests.get(juego_url)
            juego = juegos_respuesta.json()
            datos_juego=juego["data"]
            juego_nombre = datos_juego["name"]
            juegos.append(juego_nombre)
        
        personaje = {
            "name": datos_personaje.get("name"),
            "gender": datos_personaje.get("gender"),
            "race": datos_personaje.get("race"),
            "description": datos_personaje.get("description"),
            "games": juegos
        }
    except requests.exceptions.HTTPError:
            print(f"Error: El personaje con id {ID} no existe.")
    except requests.exceptions.ConnectionError:
            print("Error: No se pudo conectar a la API: Verifica tu conexion")
    except requests.exceptions.Timeout:
            print("Error: La solicitud tardó demasiado en responder")
    except ValueError:
            print(f"Error: No se pudieron procesar los datos de id {ID}")
    return personaje


try:
    #Ejemplo de ID: 5f6d186f246bd9a0809d653c
    entrada = input("Ingrese el id del personaje: ")
except ValueError as e:
    print(f"Error en la entrada: {e}. Intentalo de nuevo.")

personaje=obtener_personaje(entrada)

if personaje:
    for x,y in personaje.items():
        print(f"{x}: {y}")
