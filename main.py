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
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 64)

# Variables del jugador
ship_width, ship_height = 50, 20
ship_speed = 7
ship_x, ship_y = WIDTH // 2, HEIGHT - 50

# Lista de asteroides
asteroids = []
asteroid_speed = 5
spawn_timer = 30

# Puntuación y vidas
score = 0
difficulty_factor = 0.1
lives = 3

# Cargar imágenes
ship_image = pygame.image.load("imagenes/ship.png")
ship_image = pygame.transform.scale(ship_image, (70, 70))

asteroid_image = pygame.image.load("imagenes/asteroid.png")
asteroid_image = pygame.transform.scale(asteroid_image, (60, 60))

background_image = pygame.image.load("imagenes/background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

start_screen_image = pygame.image.load("imagenes/start_screen.jpg")
start_screen_image = pygame.transform.scale(start_screen_image, (WIDTH, HEIGHT))

game_over_image = pygame.image.load("imagenes/game_over.jpg")
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))

def draw_ship(screen, x, y):
    """Dibuja la nave del jugador usando una imagen."""
    screen.blit(ship_image, (x, y))

def draw_asteroids(screen, asteroid_list):
    """Dibuja los asteroides usando imágenes."""
    for asteroid in asteroid_list:
        screen.blit(asteroid_image, (asteroid[0] - 20, asteroid[1] - 20))

def check_collision(asteroid_list, x, y):
    """Verifica si algún asteroide choca con la nave."""
    for asteroid in asteroid_list:
        if (x < asteroid[0] < x + ship_width) and (y < asteroid[1] < y + ship_height):
            asteroid_list.remove(asteroid)
            return True
    return False

def show_start_screen():
    """Pantalla de inicio del juego con imagen personalizada."""
    screen.blit(start_screen_image, (0, 0))
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

def show_game_over_screen():
    """Pantalla de Game Over con imagen personalizada."""
    screen.blit(game_over_image, (0, 0))
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
                reset_game()

def reset_game():
    """Reinicia las variables del juego."""
    global ship_x, score, asteroid_speed, spawn_timer, lives, asteroids
    ship_x = WIDTH // 2
    score = 0
    asteroid_speed = 5
    spawn_timer = 30
    lives = 3
    asteroids = []
    main()

def main():
    global ship_x, score, asteroid_speed, spawn_timer, lives

    clock = pygame.time.Clock()
    running = True
    frame_count = 0

    while running:
        screen.blit(background_image, (0, 0))

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
            lives -= 1
            if lives == 0:
                show_game_over_screen()
                return

        # Incrementar puntuación y dificultad
        score += 1
        if score % 100 == 0:
            asteroid_speed += difficulty_factor
            spawn_timer = max(10, spawn_timer - 1)

        # Dibujar elementos
        draw_ship(screen, ship_x, ship_y)
        draw_asteroids(screen, asteroids)

        # Mostrar puntuación y vidas
        score_text = font.render(f"Puntuación: {score}", True, WHITE)
        lives_text = font.render(f"Vidas: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    show_start_screen()
    main()
