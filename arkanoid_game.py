"""Plantilla del juego Arkanoid para el hito M2."""
# He añadido esto para forzar que se muestre la pantalla.
import os
os.environ["DISPLAY"] = "1"

from arkanoid_core import *



@arkanoid_method
def cargar_nivel(self) -> list[str]:
    """Lee el fichero de nivel y devuelve la cuadrícula como lista de filas."""
    path = self.level_path
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"No se encuentra el fichero de nivel: {path}")
    texto = path.read_text(encoding="utf-8")
    lineas = texto.splitlines()
    self.layout = [l for l in lineas if l.strip()]
    if not self.layout:
        raise ValueError("El fichero de nivel está vacío.")
    ancho_referencia = len(self.layout[0])
    for i, fila in enumerate(self.layout):
        if len(fila) != ancho_referencia:
            raise ValueError(f"Error en fila {i}: Longitud incorrecta.")
    
    return self.layout

@arkanoid_method
def preparar_entidades(self) -> None:
    """Posiciona paleta y bola, y reinicia puntuación y vidas."""
    center_x = self.SCREEN_WIDTH // 2
    bottom_y = self.SCREEN_HEIGHT - self.PADDLE_OFFSET
    self.paddle.midbottom = (center_x, bottom_y)
    self.score = 0
    self.lives = 3
    self.end_message = ""
    self.reiniciar_bola()
    

@arkanoid_method
def crear_bloques(self) -> None:
    """Genera los rectángulos de los bloques en base a la cuadrícula."""
    # Limpiar listas previas 
    self.blocks.clear()
    self.block_colors.clear()
    self.block_symbols.clear()
    
    # Recorrer la matriz de texto (self.layout)
    for fila_idx, fila_str in enumerate(self.layout):
        for col_idx, caracter in enumerate(fila_str):
            
        
            # Uso el diccionario BLOCK_COLORS definido en el Core
            if caracter in self.BLOCK_COLORS:
                
                # Calcular posición y crear Rectángulo
                bloque_rect = self.calcular_posicion_bloque(fila_idx, col_idx)
                
                # Guardar en las listas paralelas
                self.blocks.append(bloque_rect)
                self.block_colors.append(self.BLOCK_COLORS[caracter])
                self.block_symbols.append(caracter)

    

@arkanoid_method
def procesar_input(self) -> None:
    """Gestiona la entrada de teclado para mover la paleta."""
    
    # Obtener estado de teclas
    keys = self.obtener_estado_teclas()

    # Movimiento izquierda (Flecha o A)
    if keys[self.KEY_LEFT] or keys[self.KEY_A]:
        self.paddle.x -= self.PADDLE_SPEED

    # Movimiento derecha (Flecha o D)
    if keys[self.KEY_RIGHT] or keys[self.KEY_D]:
        self.paddle.x += self.PADDLE_SPEED

    # Mantener dentro de la pantalla (Clamping)
    # Si intentamos salir por la izquierda, nos quedamos en 0
    if self.paddle.left < 0:
        self.paddle.left = 0
    # Si intentamos salir por la derecha, nos quedamos en el ancho máximo
    if self.paddle.right > self.SCREEN_WIDTH:
        self.paddle.right = self.SCREEN_WIDTH 

@arkanoid_method
def actualizar_bola(self) -> None:
    """Actualiza la posición de la bola y resuelve colisiones."""
   
    # Si el juego ha terminado (victoria o derrota), no movemos la bola
    if self.end_message:
        return

    # Mover la bola
    self.ball_pos += self.ball_velocity
    ball_rect = self.obtener_rect_bola()

    # Rebote en paredes
    if ball_rect.left <= 0:
        self.ball_pos.x = self.BALL_RADIUS
        self.ball_velocity.x *= -1
        
    elif ball_rect.right >= self.SCREEN_WIDTH:
        self.ball_pos.x = self.SCREEN_WIDTH - self.BALL_RADIUS
        self.ball_velocity.x *= -1
        
    if ball_rect.top <= 0:
        self.ball_pos.y = self.BALL_RADIUS
        self.ball_velocity.y *= -1
    
    # Perder vida
    if ball_rect.top >= self.SCREEN_HEIGHT:
        self.lives -= 1
        if self.lives > 0:
            
            self.reiniciar_bola()
        else:
            self.end_message = "GAME OVER"
        return

    # Colision con pala 
    if ball_rect.colliderect(self.paddle) and self.ball_velocity.y > 0:
        # Aunque salga recta, si el jugador la golpea con el lado cogerá ángulo 
        diff = (ball_rect.centerx - self.paddle.centerx) / (self.PADDLE_SIZE[0] / 2)
        
        nueva_direccion = Vector2(diff, -1).normalize() * self.BALL_SPEED
        self.ball_velocity = nueva_direccion
        
        self.ball_pos.y = self.paddle.top - self.BALL_RADIUS - 1

    # 4. Colision con bloques
    idx_colision = -1
    for i in range(len(self.blocks) - 1, -1, -1):
        if ball_rect.colliderect(self.blocks[i]):
            idx_colision = i
            break
    
    if idx_colision != -1:
        self.ball_velocity.y *= -1
        
        simbolo = self.block_symbols[idx_colision]
        if simbolo in self.BLOCK_POINTS:
            self.score += self.BLOCK_POINTS[simbolo]
        
        del self.blocks[idx_colision]
        del self.block_colors[idx_colision]
        del self.block_symbols[idx_colision]
        
        if not self.blocks:
            self.end_message = "VICTORIA!"

@arkanoid_method
def dibujar_escena(self) -> None:
    """Renderiza fondo, bloques, paleta, bola y HUD."""
   
    # Pinta el fondo 
    self.screen.fill(self.BACKGROUND_COLOR)
    
    # Pinta los bloques
    for i, rect in enumerate(self.blocks):
        color = self.block_colors[i]
        self.dibujar_rectangulo(rect, color)
        
    # Pinta la paleta
    self.dibujar_rectangulo(self.paddle, self.PADDLE_COLOR)
    
    # Pinta la bola
    # Convertimos la posición exacta (float) a píxeles (int) para dibujar
    centro_bola = (int(self.ball_pos.x), int(self.ball_pos.y))
    self.dibujar_circulo(centro_bola, self.BALL_RADIUS, self.BALL_COLOR)
    
    # Pinta la interfaz 
    self.dibujar_texto(f"Puntos: {self.score}", (20, 20))
    self.dibujar_texto(f"Vidas: {self.lives}", (self.SCREEN_WIDTH - 120, 20))
    
    # Mensaje de fin de juego
    if self.end_message:
        center_pos = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
        self.dibujar_texto(self.end_message, center_pos, grande=True)

@arkanoid_method
def run(self) -> None:
    """Ejecuta el bucle principal del juego."""
    self.inicializar_pygame()
    
    try:
        # Secuencia de inicio
        self.cargar_nivel()       
        self.preparar_entidades() 
        
        print("Intentando crear bloques...")
        self.crear_bloques()      
        
        # Bucle del juego
        self.running = True
        while self.running:
            self.clock.tick(self.FPS)
            
            # Gestión de cierre 
            for event in self.iterar_eventos():
                if event.type == self.EVENT_QUIT:
                    self.running = False
                elif event.type == self.EVENT_KEYDOWN:
                    if event.key == self.KEY_ESCAPE:
                        self.running = False
            
            
            self.procesar_input()
            self.actualizar_bola()
            
            # Dibujado 
            self.dibujar_escena()
            self.actualizar_pantalla()
            
    except Exception as e:
        print(f"\n[ERROR] Algo falló: {e}")
        
        import traceback
        traceback.print_exc()
    finally:
        self.finalizar_pygame()


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("level", type=str, nargs="?", default="niveles/demo.txt")
    args = parser.parse_args()
    game = ArkanoidGame(args.level)
    game.run()

if __name__ == "__main__":
    main()