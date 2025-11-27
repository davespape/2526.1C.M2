Arkanoid M2 - Proyecto Python

Esta es una implementación académica del clásico juego arcade Arkanoid, desarrollada utilizando Python y la biblioteca pygame para el hito de programación M2.

*Descripción*

El objetivo del juego es despejar la pantalla de bloques rebotando una bola con una pala móvil. El jugador pierde una vida si la bola toca el suelo. El juego incluye:

- Sistema de físicas con rebotes angulares.

- Puntuación y vidas.

- Carga dinámica de niveles desde ficheros de texto.

- Diferentes tipos de bloques con distintas puntuaciones.

*Requisitos*

Para ejecutar este juego necesitas:

- Python 3.10 o superior.

- La librería pygame.

Si no la tienes instalada, ejecuta:

pip install pygame


*Cómo Jugar*

Ejecución

Para jugar al nivel por defecto (demo.txt):

python arkanoid_game.py


Para cargar un nivel personalizado (por ejemplo nivel_final):

python arkanoid_game.py niveles/nivel_final.txt


Controles

Tecla: Flecha Izquierda / A
Accion: Mover paleta a la izquierda

Tecla: Flecha Derecha / D
Accion: Mover paleta a la derecha


Tecla: ESC
Accion: Salir del juego

*Leyenda del Mapa*

Los niveles se diseñan en archivos .txt usando estos símbolos:

- #: Bloque Rojo (Estándar) - 50 Puntos.

- @: Bloque Azul (Reforzado) - 75 Puntos.

- %: Bloque Dorado (Bonus) - 120 Puntos.

- .: Espacio vacío.

*Autor*

David Espina Apellaniz

