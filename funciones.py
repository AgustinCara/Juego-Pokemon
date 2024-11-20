def calcular_estadisticas(lista_tiempos: list) -> tuple:
    """Calcula las estadísticas de una lista de tiempos.

    Args:
        lista_tiempos (list): Lista de tiempos en milisegundos.

    Returns:
        tuple: Contiene el mejor tiempo, peor tiempo y tiempo promedio.
    """
    if lista_tiempos:
        mejor_tiempo = min(lista_tiempos, key=lambda x: x)
        peor_tiempo = max(lista_tiempos, key=lambda x: x)
        tiempo_promedio = sum(lista_tiempos) / len(lista_tiempos)
    else:
        mejor_tiempo = 0
        peor_tiempo = 0
        tiempo_promedio = 0

    return mejor_tiempo, peor_tiempo, tiempo_promedio