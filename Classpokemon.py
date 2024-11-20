import pygame

class Pokemon:
    def __init__(self, nombre: str, origen: tuple, dimensiones: tuple, imagen: str, audio: str, generacion: int):
        """Inicializa un objeto Pokemon.

        Args:
            nombre (str): Nombre del Pokemon.
            origen (tuple): Coordenadas del centro del Pokemon en la pantalla.
            dimensiones (tuple): Dimensiones de la imagen del Pokemon.
            imagen (str): Ruta de la imagen del Pokemon.
            audio (str): Ruta del archivo de audio del Pokemon.
            generacion (int): Generación del Pokemon.
        """
        self.nombre = nombre
        self.imagen = pygame.image.load(imagen)
        self.imagen = pygame.transform.scale(self.imagen, dimensiones)
        self.rectangulo = self.imagen.get_rect()
        self.rectangulo.center = origen
        self.generacion = generacion
        self.audio = audio


    def dibujar(self, pantalla: pygame.Surface, mostrar_silueta: bool, dificultad: str):
        """Dibuja el Pokemon en la pantalla según la dificultad y si se muestra la silueta.

        Args:
            pantalla (pygame.Surface): Superficie donde se dibuja el Pokemon.
            mostrar_silueta (bool): Indica si se muestra la silueta del Pokemon.
            dificultad (str): Nivel de dificultad.
        """
        silueta = self.imagen.copy()
        silueta.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)

        if dificultad == ['Easy']:
            pantalla.blit(self.imagen, self.rectangulo)
        elif dificultad == ['Hard']:
            silueta_pixelada = pygame.transform.scale(silueta, (silueta.get_width() // 10, silueta.get_height() // 10))
            silueta_pixelada = pygame.transform.scale(silueta_pixelada, silueta.get_size())
            if mostrar_silueta:
                pantalla.blit(silueta_pixelada, self.rectangulo)
                pantalla.blit(silueta_pixelada, self.rectangulo)
            else:
                pantalla.blit(self.imagen, self.rectangulo)
        else:
            if mostrar_silueta:
                pantalla.blit(silueta, self.rectangulo)
            else:
                pantalla.blit(self.imagen, self.rectangulo)


    def nombres(self, lista_nombres: list, fuente: pygame.font.Font, color: tuple, pantalla: pygame.Surface):
        """Dibuja los nombres del Pokemon en diferentes idiomas en la pantalla.

        Args:
            lista_nombres (list): Lista de nombres en diferentes idiomas.
            fuente (pygame.font.Font): Fuente para renderizar el texto.
            color (tuple): Color del texto.
            pantalla (pygame.Surface): Superficie donde se dibujan los nombres.
        """
        for nombre in lista_nombres:
            name_en = self.nombre
            name_fr = self.nombre
            name_it = self.nombre
            name_de = self.nombre

            if self.nombre == nombre[0]:
                name_en = nombre[1]
                name_fr = nombre[2]
                name_it = nombre[3]
                name_de = nombre[4]
                break

        texto_1 = fuente.render(name_en, True, color)
        texto_2 = fuente.render(name_fr, True, color)
        texto_3 = fuente.render(name_it, True, color)
        texto_4 = fuente.render(name_de, True, color)

        pantalla.blit(texto_1, (30, 170))
        pantalla.blit(texto_2, (30, 220))
        pantalla.blit(texto_3, (30, 270))  
        pantalla.blit(texto_4, (30, 320))


    def filtrar_pokemons(self, lista_pokemons: list, generaciones: list) -> list:
        """Filtra una lista de Pokemon por generaciones especificadas.

        Args:
            lista_pokemons (list): Lista de objetos Pokemon.
            generaciones (list): Lista de generaciones a filtrar.

        Returns:
            list: Lista de Pokemon filtrados por generación.
        """
        pokemons_filtrados = []

        if not generaciones:
            pokemons_filtrados = lista_pokemons
        else:
            for pokemon in lista_pokemons:
                if pokemon.generacion in generaciones:
                    pokemons_filtrados.append(pokemon)

        return pokemons_filtrados