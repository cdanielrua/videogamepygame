import pygame
import random

# Inicializar PyGame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Defensor del Espacio")

# Colores y fuentes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
font = pygame.font.Font(None, 36)

# Variables del jugador
ship_x, ship_y = WIDTH // 2, HEIGHT - 50
ship_speed = 5

# Lista de asteroides
asteroids = []

def draw_ship(screen, x, y):
    pygame.draw.rect(screen, WHITE, (x, y, 50, 20))

def draw_asteroid(screen, asteroid_list):
    for asteroid in asteroid_list:
        pygame.draw.circle(screen, RED, asteroid, 20)

def main():
    global ship_x  # Declarar ship_x como global para modificarla dentro de la función

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Movimiento de la nave
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ship_x > 0:
            ship_x -= ship_speed
        if keys[pygame.K_RIGHT] and ship_x < WIDTH - 50:
            ship_x += ship_speed
        
        draw_ship(screen, ship_x, ship_y)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
