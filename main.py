import pygame
import sys
import time

# Inicializa o Pygame
pygame.init()
pygame.mixer.init()

# 📱 Configuração da tela
WIDTH, HEIGHT = 600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CandiCatch")

# 🎨 Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FIRE = (255, 69, 0)
GOLD = (255, 215, 0)
BLUE = (0, 102, 255)

# 🎮 Fonte personalizada
title_font = pygame.font.SysFont("comicsansms", 80, bold=True)
button_font = pygame.font.SysFont("comicsansms", 50, bold=True)
score_font = pygame.font.SysFont(None, 36)

# 🔊 Carregar sons
try:
    sound_hit = pygame.mixer.Sound("candicatch.wav")
    sound_hit.set_volume(1.0)
except pygame.error:
    sound_hit = None

try:
    sound_miss = pygame.mixer.Sound("errou.wav")
    sound_miss.set_volume(1.0)
except pygame.error:
    sound_miss = None

# 🏁 Tela inicial
def show_start_screen():
    screen.fill(WHITE)
    title_text = title_font.render("CandiCatch", True, GOLD)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    button_rect = pygame.Rect((WIDTH - 200) // 2, HEIGHT // 2, 200, 80)
    pygame.draw.rect(screen, BLUE, button_rect, border_radius=20)
    button_text = button_font.render("Jogar", True, WHITE)

    text_x = button_rect.x + (button_rect.width - button_text.get_width()) // 2
    text_y = button_rect.y + (button_rect.height - button_text.get_height()) // 2
    screen.blit(button_text, (text_x, text_y))

    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    pygame.mixer.music.load("candimusic.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    waiting = False

show_start_screen()

# 🎮 Carregar imagens
candiru = pygame.image.load("candiru.png")
candiru = pygame.transform.scale(candiru, (candiru.get_width() // 2, candiru.get_height() // 2))
candiru_rect = candiru.get_rect(center=(WIDTH // 2, HEIGHT - 50))

glande_original = pygame.image.load("glande.png")
glande = pygame.transform.scale(glande_original, (int(glande_original.get_width() * 1.2), int(glande_original.get_height() * 1.2)))
glande_rect = glande.get_rect(center=(WIDTH // 2, 120))  # 🔽 Glande mais para baixo

# ⚡ Configurações do jogo
gland_speed = 9
gland_direction = 1
initial_gland_speed = gland_speed

button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 100, 100, 50)

score = 0
multiplicador = 1
acertos_consecutivos = 0
candiru_lancado = False
candiru_speed = -20
max_streak = 0  

# ⏳ Contador de tempo
start_time = time.time()
time_limit = 90  

# 🔄 Funções do jogo
def draw_screen():
    screen.fill(WHITE)
    screen.blit(candiru, candiru_rect)
    screen.blit(glande, glande_rect)

    # 🟥 Botão "Catch"
    pygame.draw.rect(screen, RED, button_rect)
    button_text = score_font.render("Catch", True, WHITE)
    text_x = button_rect.x + (button_rect.width - button_text.get_width()) // 2
    text_y = button_rect.y + (button_rect.height - button_text.get_height()) // 2
    screen.blit(button_text, (text_x, text_y))

    # 📊 Alinhamento dos textos no topo da tela
    elapsed_time = int(time.time() - start_time)
    remaining_time = max(0, time_limit - elapsed_time)
    
    timer_text = score_font.render(f"Tempo: {remaining_time}s", True, BLACK)
    score_text = score_font.render(f"Pontos: {score}", True, BLACK)
    streak_text = score_font.render(f"Multiplicador: x{multiplicador}", True, FIRE)

    screen.blit(timer_text, (10, 10))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
    screen.blit(streak_text, (WIDTH - streak_text.get_width() - 10, 10))

    pygame.display.flip()

def reset_game(errou=False):
    global candiru_lancado, acertos_consecutivos, multiplicador, gland_speed

    candiru_rect.centerx = WIDTH // 2
    candiru_rect.bottom = HEIGHT - 50  
    candiru_lancado = False  

    if errou:  
        acertos_consecutivos = 0  
        multiplicador = 1  
        gland_speed = initial_gland_speed  
        
        if sound_miss:
            sound_miss.play()

def check_button_click():
    global candiru_lancado
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0] and not candiru_lancado:
            candiru_lancado = True  

def move_gland():
    global gland_direction
    glande_rect.x += gland_speed * gland_direction
    if glande_rect.left <= 0 or glande_rect.right >= WIDTH:
        gland_direction *= -1

def check_collision():
    global score, acertos_consecutivos, multiplicador, gland_speed, max_streak
    if candiru_rect.colliderect(glande_rect):
        score += 10 * multiplicador
        acertos_consecutivos += 1
        multiplicador += 1
        max_streak = max(max_streak, acertos_consecutivos)

        if acertos_consecutivos % 3 == 0:
            gland_speed += 1  

        if sound_hit:
            sound_hit.play()

        reset_game()

def show_game_over():
    screen.fill(WHITE)
    game_over_text = title_font.render("Fim de Jogo!", True, BLACK)
    score_text = button_font.render(f"Pontos: {score}", True, BLUE)
    streak_text = button_font.render(f"Streak Máximo: {max_streak}", True, FIRE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 350))
    screen.blit(streak_text, (WIDTH // 2 - streak_text.get_width() // 2, 450))

    pygame.display.flip()

    # 🔄 Espera indefinida até o jogador fechar a janela
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# 🎮 Loop principal
running = True
while running:
    elapsed_time = int(time.time() - start_time)
    if elapsed_time >= time_limit:
        show_game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    move_gland()
    check_button_click()

    if candiru_lancado:
        candiru_rect.y += candiru_speed  
        check_collision()  
        if candiru_rect.bottom < 0:
            reset_game(errou=True)

    draw_screen()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
