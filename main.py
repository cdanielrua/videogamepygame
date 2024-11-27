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
title_font = pygame.font.Font(None, 64)

# Variables del jugador
ship_x, ship_y = WIDTH // 2, HEIGHT - 50
ship_speed = 7
ship_width, ship_height = 50, 20

# Lista de asteroides
asteroids = []
asteroid_speed = 5
spawn_timer = 30

# Puntuación
score = 0
difficulty_factor = 0.1  # Incremento de dificultad

def draw_ship(screen, x, y):
    """Dibuja la nave del jugador."""
    pygame.draw.rect(screen, WHITE, (x, y, ship_width, ship_height))

def draw_asteroids(screen, asteroid_list):
    """Dibuja los asteroides."""
    for asteroid in asteroid_list:
        pygame.draw.circle(screen, RED, (asteroid[0], asteroid[1]), 20)

def check_collision(asteroid_list, x, y):
    """Verifica si algún asteroide choca con la nave."""
    for asteroid in asteroid_list:
        if (x < asteroid[0] < x + ship_width) and (y < asteroid[1] < y + ship_height):
            return True
    return False

def show_start_screen():
    """Pantalla de inicio del juego."""
    screen.fill(BLACK)
    title_text = title_font.render("Defensor del Espacio", True, WHITE)
    prompt_text = font.render("Presiona ENTER para comenzar", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def main():
    global ship_x, score, asteroid_speed, spawn_timer  # Declarar variables globales

    clock = pygame.time.Clock()
    running = True
    frame_count = 0

    while running:
        screen.fill(BLACK)

        # Eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimiento de la nave
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ship_x > 0:
            ship_x -= ship_speed
        if keys[pygame.K_RIGHT] and ship_x < WIDTH - ship_width:
            ship_x += ship_speed

        # Generación de asteroides
        frame_count += 1
        if frame_count % spawn_timer == 0:
            asteroid_x = random.randint(0, WIDTH)
            asteroid_y = -20
            asteroids.append([asteroid_x, asteroid_y])

        # Movimiento de asteroides
        for asteroid in asteroids:
            asteroid[1] += asteroid_speed

        # Eliminar asteroides que salen de la pantalla
        asteroids[:] = [asteroid for asteroid in asteroids if asteroid[1] < HEIGHT]

        # Comprobar colisión
        if check_collision(asteroids, ship_x, ship_y):
            show_game_over_screen()
            return  # Salir del juego actual y volver al menú

        # Incrementar puntuación y dificultad
        score += 1
        if score % 100 == 0:  # Cada 100 puntos, aumenta la dificultad
            asteroid_speed += difficulty_factor
            spawn_timer = max(10, spawn_timer - 1)  # Reduce el tiempo entre asteroides

        # Dibujar elementos
        draw_ship(screen, ship_x, ship_y)
        draw_asteroids(screen, asteroids)

        # Mostrar puntuación
        score_text = font.render(f"Puntuación: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def show_game_over_screen():
    """Pantalla de Game Over."""
    screen.fill(BLACK)
    game_over_text = title_font.render("¡Juego Terminado!", True, WHITE)
    score_text = font.render(f"Puntuación final: {score}", True, WHITE)
    restart_text = font.render("Presiona ENTER para reiniciar", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
                main()  # Reiniciar el juego

if __name__ == "__main__":
    show_start_screen()
    main()
