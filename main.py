import pygame
import random
from archivos import *
from Classpokemon import *
from Classbotones import *
from Classanimacion import *

# Colores
AZUL_CLARO = (0, 150, 255)
NEGRO = (0,0,0)
BLANCO = (255,255,255)


# Configuración de la ventana
ANCHO_VENTANA = 650 
ALTO_VENTANA = 720
TAMANO_VENTANA = (ANCHO_VENTANA, ALTO_VENTANA)

# Inicialización de Pygame
pygame.init()

# Cargar recursos
lista_pokemons = cargar_lista_pokemons('pokemons.csv')
lista_nombre = cargar_nombre_pokemons('pokemon_names_multilang.csv')
icono = pygame.image.load('Recursos\\Icono\\Pokeball.png')
reino_unido = pygame.image.load(r'Recursos\Banderas\Reino_Unido.png')
reino_unido = pygame.transform.scale(reino_unido, (25, 25))
francia = pygame.image.load(r'Recursos\Banderas\Francia.png')
francia = pygame.transform.scale(francia, (25, 25))
italia = pygame.image.load(r'Recursos\Banderas\Italia.png')
italia = pygame.transform.scale(italia, (25, 25))
alemania = pygame.image.load(r'Recursos\Banderas\Alemania.png')
alemania = pygame.transform.scale(alemania, (25, 25))
fuente = pygame.font.SysFont('consolas', 20)
fuente_titulo = pygame.font.SysFont('Arial', 40)

# Configurar la ventana
ventana = pygame.display.set_mode(TAMANO_VENTANA)
pygame.display.set_caption("Who's That Pokemon?")
pygame.display.set_icon(icono)
ventana.fill(AZUL_CLARO)

# Inicializar botones
botones_generaciones = Botones()
botones_dificultad = Botones()
boton_salir = Botones()
boton_reiniciar = Botones()
botones_generaciones.crear_botones_generacion(75, 45, 3, 3, (50, 550), 1)
botones_dificultad.crear_botones_dificultad(110, 45, 3, 1, (500, 550), 1)
boton_salir.crear_boton(ANCHO_VENTANA - 250, ALTO_VENTANA // 2 - 100, 200, 50, NEGRO, "Salir")
boton_reiniciar.crear_boton(ANCHO_VENTANA - 250, ALTO_VENTANA // 2 - 170, 200, 50, NEGRO, "Volver a jugar")

# Inicializar banderas
banderas = {
    "mostrar_silueta": True,
    "siguiente": False,
    "activo": False,
    "flag": True,
    "aplicar_filtro": False,
    "mostrar_nombres": False,
    "juego": True,
    "juego_terminado": False
}

# Inicializar contadores
contadores = {
    "contador_tiempo": 0,
    "contador_pokemons": 0,
    "tiempo_inicial": pygame.time.get_ticks(),
    "aciertos": 0,
    "lista_tiempos": [],
    "pokemons_adivinados": [],
    "tiempo_ultima_respuesta": 0,
    "max_aciertos": 0
}

# Configurar input
input_rect = pygame.Rect(0, 0, 200, 32)
input_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 1.7 + 1)
texto = ''

# Ruta y configuración de la animación
ruta_frames = 'Recursos/frames-gif'
animacion = Animacion(ruta_frames, 3000)

# Seleccionar Pokémon inicial
pokemon_actual = random.choice(lista_pokemons)
print(pokemon_actual.nombre)
print(pokemon_actual.generacion)

# Configuración inicial
contadores['max_aciertos'] = record_aciertos('./record_aciertos.txt', contadores['aciertos'])

# Bucle principal
while banderas['flag']:
    lista_eventos = pygame.event.get()
    tiempo_actual = pygame.time.get_ticks()
    contadores['contador_tiempo'] = (tiempo_actual - contadores['tiempo_inicial']) // 1000

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            banderas['flag'] = False

        elif evento.type == pygame.KEYDOWN:
            if banderas['activo']:
                if evento.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                elif evento.key == pygame.K_RETURN:
                    if pokemon_actual.nombre.lower() == texto.lower():
                        animacion.iniciar(tiempo_actual)
                        contadores['tiempo_inicial'] = tiempo_actual + 3000
                        contadores['lista_tiempos'].append(contadores['contador_tiempo'])
                        contadores['tiempo_ultima_respuesta'] = contadores['contador_tiempo']
                        contadores['contador_pokemons'] += 1
                        contadores['aciertos'] += 1
                        contadores['pokemons_adivinados'].append({'nombre': pokemon_actual.nombre, 'generacion': pokemon_actual.generacion})
                        if contadores['aciertos'] > contadores['max_aciertos']:
                            contadores['max_aciertos'] = contadores['aciertos']
                            record_aciertos('./record_aciertos.txt', contadores['aciertos'])
                        
                        banderas['juego'] = True
                    else:
                        banderas['juego'] = False

                    contadores['tiempo_inicial'] = tiempo_actual + 3000
                    texto = ""
                    banderas['mostrar_silueta'] = False
                    banderas['mostrar_nombres'] = True

                else:
                    texto += evento.unicode

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_salir.boton_clickeado(evento.pos):
                banderas['flag'] = False
            elif boton_reiniciar.boton_clickeado(evento.pos):
                contadores = {
                    "contador_tiempo": 0,
                    "contador_pokemons": 0,
                    "tiempo_inicial": pygame.time.get_ticks(),
                    "aciertos": 0,
                    "lista_tiempos": [],
                    "pokemons_adivinados": [],
                    "tiempo_ultima_respuesta": 0,
                    "max_aciertos": 0
                }
                contadores['max_aciertos'] = record_aciertos('./record_aciertos.txt', contadores['aciertos'])
                banderas['juego'] = True
                banderas['juego_terminado'] = False
            elif input_rect.collidepoint(evento.pos):
                banderas['activo'] = not banderas['activo']
            else:
                banderas['activo'] = False

            pos = evento.pos
            botones_generaciones.actualizar_color_boton(pos)
            botones_dificultad.actualizar_color_boton(pos)
            banderas['aplicar_filtro'] = True

    if banderas['juego'] and contadores['aciertos'] < 10:
        if banderas['siguiente']:
            if banderas['aplicar_filtro']:
                generaciones_seleccionadas = botones_generaciones.obtener_generaciones_seleccionadas()
                lista_pokemons_filtrada = pokemon_actual.filtrar_pokemons(lista_pokemons, generaciones_seleccionadas)
                banderas['aplicar_filtro'] = False

            if lista_pokemons_filtrada:
                pokemon_actual = random.choice(lista_pokemons_filtrada)
                print(pokemon_actual.nombre)
                print(pokemon_actual.generacion)
            banderas['mostrar_silueta'] = True
            banderas['mostrar_nombres'] = False
            banderas['siguiente'] = False

        if not banderas['mostrar_silueta'] and tiempo_actual - animacion.tiempo_inicial >= animacion.tiempo_maximo:
            tiempo_inicio_respuesta = pygame.time.get_ticks()
            pokemon_actual = random.choice(lista_pokemons)
            banderas['mostrar_silueta'] = True 
            animacion.tiempo_inicial = 0
            banderas['siguiente'] = True
            banderas['mostrar_nombres'] = False

        ventana.fill(AZUL_CLARO)

        botones_generaciones.dibujar_botones_generacion(ventana, NEGRO, fuente)
        botones_dificultad.dibujar_botones_dificultad(ventana, NEGRO, fuente)
        dificultad_seleccionada = botones_dificultad.obtener_dificutlad_seleccionada()
        
        pokemon_actual.dibujar(ventana, banderas['mostrar_silueta'], dificultad_seleccionada)

        pygame.draw.rect(ventana, BLANCO, input_rect)
        superficie_texto = fuente.render(texto, True, NEGRO)
        contador_aciertos = fuente.render(f'{contadores["aciertos"]}/10', True, NEGRO)
        ventana.blit(superficie_texto, (input_rect.x + 5, input_rect.y + (input_rect.height - superficie_texto.get_height()) // 2))
        ventana.blit(fuente_titulo.render("Who's That Pokemon?", True, BLANCO), (ANCHO_VENTANA // 2 - fuente_titulo.size("Who's That Pokemon?")[0] // 2, 50))
        ventana.blit(fuente.render('Generation', True, NEGRO), (110, 515))
        ventana.blit(fuente.render('Difficulty', True, NEGRO), (498, 515))
        ventana.blit(contador_aciertos, (ANCHO_VENTANA // 2 - 20, ALTO_VENTANA // 2 + 85))

        # nombre_pokemon = fuente.render(f'{pokemon_actual.nombre} {pokemon_actual.generacion}', True, NEGRO)
        # ventana.blit(nombre_pokemon, (50, 50))

        animacion.actualizar(tiempo_actual)
        animacion.dibujar(ventana, (input_rect.right + 50, input_rect.y + (input_rect.height - 90) // 2))
    
        if banderas['mostrar_nombres']:
            pokemon_actual.nombres(lista_nombre, fuente, NEGRO, ventana)
            ventana.blit(reino_unido, (0, 168))
            ventana.blit(francia, (0, 218))
            ventana.blit(italia, (0, 268))
            ventana.blit(alemania, (0, 318))

        ventana.blit(fuente.render(f'Tiempo última respuesta: {contadores["tiempo_ultima_respuesta"]}s', True, NEGRO), (2, 2))

        if contadores['lista_tiempos']:
            tiempo_promedio_actual = sum(contadores['lista_tiempos']) / len(contadores['lista_tiempos'])
        else:
            tiempo_promedio_actual = 0

        ventana.blit(fuente.render(f'Tiempo promedio: {tiempo_promedio_actual:.2f}s', True, NEGRO), (2, 22))
        ventana.blit(fuente.render(f'Aciertos: {contadores["aciertos"]}', True, NEGRO), (420, 22))
        ventana.blit(fuente.render(f'Record Aciertos: {contadores["max_aciertos"]}', True, NEGRO), (420, 2))

    else:
        if not banderas['juego_terminado']:
            banderas['juego_terminado'] = True
            ventana.fill(AZUL_CLARO)
            guardar_estadisticas('./estadisticas.json', contadores['aciertos'], contadores['lista_tiempos'])

        pygame.draw.rect(ventana, BLANCO, (30, 30, 600, 650))

        mejor_tiempo, peor_tiempo, tiempo_promedio = calcular_estadisticas(contadores['lista_tiempos'])
        ventana.blit(fuente_titulo.render("Resultados del Juego", True, NEGRO), (ANCHO_VENTANA // 2 - fuente_titulo.size("Resultados del Juego")[0] // 2, 50))
        ventana.blit(fuente.render(f'Aciertos: {contadores["aciertos"]}', True, NEGRO), (50, 150))
        ventana.blit(fuente.render(f'Mejor tiempo: {mejor_tiempo:.2f}s', True, NEGRO), (50, 200))
        ventana.blit(fuente.render(f'Peor tiempo: {peor_tiempo:.2f}s', True, NEGRO), (50, 250))
        ventana.blit(fuente.render(f'Tiempo promedio: {tiempo_promedio:.2f}s', True, NEGRO), (50, 300))

        y = 350
        for pokemon in contadores['pokemons_adivinados']:
            ventana.blit(fuente.render(f'{pokemon["nombre"]} (Generacion {pokemon["generacion"]})', True, NEGRO), (50, y))
            y += 30

        boton_salir.dibujar_boton(ventana, fuente)
        boton_reiniciar.dibujar_boton(ventana, fuente)

    pygame.display.update()

pygame.quit()