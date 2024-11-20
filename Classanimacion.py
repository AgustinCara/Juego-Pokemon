import pygame
import os

class Animacion:
    def __init__(self, ruta_frames: str, tiempo_maximo: int, tamano=(70, 70)):
        """Inicializa la clase Animacion.

        Args:
            ruta_frames (str): Ruta a la carpeta donde se encuentran los frames de la animación.
            tiempo_maximo (int): Tiempo total que dura la animación en milisegundos.
            tamano (tuple): Tamaño al cual escalar los frames de la animación.
        """
        self.frames = []
        self.cargar_frames(ruta_frames, tamano)
        self.tiempo_maximo = tiempo_maximo
        self.tiempo_por_frame = tiempo_maximo / len(self.frames)
        self.frame_actual = 0
        self.tiempo_inicial = 0


    def cargar_frames(self, ruta_frames: str, tamano: tuple):
        """Carga los frames de la animación desde la ruta especificada y los escala al tamaño dado.

        Args:
            ruta_frames (str): Ruta a la carpeta donde se encuentran los frames de la animación.
            tamano (tuple): Tamaño al cual escalar los frames de la animación.
        """
        for i in range(1, 31):
            filename = f'frame-{i:02d}.gif'
            frame = pygame.image.load(os.path.join(ruta_frames, filename))
            frame = pygame.transform.scale(frame, tamano)
            self.frames.append(frame)


    def iniciar(self, tiempo_actual: int):
        """Inicia la animación.

        Args:
            tiempo_actual (int): El tiempo actual en milisegundos.
        """
        self.tiempo_inicial = tiempo_actual


    def actualizar(self, tiempo_actual: int):
        """Actualiza el frame actual de la animación basado en el tiempo transcurrido.

        Args:
            tiempo_actual (int): El tiempo actual en milisegundos.
        """
        if self.tiempo_inicial > 0:
            contador_tiempo = tiempo_actual - self.tiempo_inicial
            self.frame_actual = int((contador_tiempo / self.tiempo_por_frame) % len(self.frames))
            if contador_tiempo >= self.tiempo_maximo:
                self.tiempo_inicial = 0


    def dibujar(self, ventana: pygame.Surface, posicion: tuple):
        """Dibuja el frame actual de la animación en la ventana en la posición especificada.

        Args:
            ventana (pygame.Surface): Superficie donde se dibuja la animación.
            posicion (tuple): Posición (x, y) donde se dibuja el frame actual.
        """
        if self.tiempo_inicial > 0:
            ventana.blit(self.frames[self.frame_actual], posicion)