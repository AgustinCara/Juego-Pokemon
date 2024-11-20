from Classpokemon import *
import re
from funciones import *
import json


def cargar_lista_pokemons(path: str) -> list:
    """Carga una lista de objetos Pokemon desde un archivo.

    Args:
        path (str): Ruta del archivo CSV.

    Returns:
        list: Lista de objetos Pokemon.
    """
    lista = []

    with open(path, 'r') as archivo:
        archivo.readline()

        for line in archivo:
            lectura = re.split(',|\n', line)
            nombre = lectura[0]
            origen = (int(lectura[1]), int(lectura[2]))
            dimensiones = (int(lectura[3]), int(lectura[4]))
            imagen = lectura[5]
            audio = lectura[6]
            generacion = int(lectura[7])

            pokemon = Pokemon(nombre, origen, dimensiones, imagen, audio, generacion)

            lista.append(pokemon)

    return lista


def cargar_nombre_pokemons(path: str) -> list:
    """Carga una lista de nombres de Pokemon en diferentes idiomas desde un archivo.

    Args:
        path (str): Ruta del archivo CSV.

    Returns:
        list: Lista de nombres de Pokemon en diferentes idiomas.
    """
    lista = []

    with open(path, 'r') as archivo:
        archivo.readline()

        for line in archivo:
            lectura = re.split(',|\n', line)
            nombre = lectura[0]
            name_en = lectura[1]
            name_fr = lectura[2]
            name_it = lectura[3]
            name_de = lectura[4]

            nombre_pokemon = (nombre, name_en, name_fr, name_it, name_de)

            lista.append(nombre_pokemon)

    return lista


def guardar_estadisticas(path: str, aciertos: int, lista_tiempos: list):
    """Guarda las estadísticas del juego en un archivo JSON.

    Args:
        path (str): Ruta del archivo JSON.
        aciertos (int): Número de aciertos.
        lista_tiempos (list): Lista de tiempos.
    """
    estadisticas = leer_estadisticas(path)
    mejor_tiempo, peor_tiempo, tiempo_promedio = calcular_estadisticas(lista_tiempos)
    datos_a_guardar = {
        "aciertos": aciertos,
        "mejor_tiempo": mejor_tiempo,
        "peor_tiempo": peor_tiempo,
        "tiempo_promedio": tiempo_promedio,
        "tiempos": lista_tiempos
    }
    estadisticas.append(datos_a_guardar)
    with open(path, 'w') as archivo:
            json.dump(estadisticas, archivo, indent = 4)


def leer_estadisticas(path: str) -> list[dict]:
    """Lee las estadísticas del juego desde un archivo JSON.

    Args:
        path (str): Ruta del archivo JSON.

    Returns:
        list[dict]: Lista de diccionarios con las estadísticas del juego.
    """
    diccionario = []
    try:
        with open(path, 'r') as archivo:
            diccionario = json.load(archivo)
    except:
        print('Se creo el archivo')
    
    return diccionario


def record_aciertos(path: str, aciertos: int) -> int:
    """Registra el número máximo de aciertos en un archivo.

    Args:
        path (str): Ruta del archivo.
        aciertos (int): Número de aciertos.

    Returns:
        int: El récord de aciertos.
    """
    try:
        with open(path, 'r+') as archivo:
            contenido = archivo.read()
            if contenido:
                record_aciertos = int(contenido)
            else:
                record_aciertos = 0
            
            if aciertos > record_aciertos:
                archivo.seek(0)
                archivo.write(str(aciertos))
    except:
        print('El archivo no existe. Se creará uno nuevo.')
        with open(path, 'w') as archivo:
            archivo.write(str(aciertos))
        record_aciertos = aciertos
    
    return record_aciertos