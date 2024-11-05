# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
pygame.init()

# ----- Gera tela principal
WIDTH = 600
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Geometry Dash - Python Edition')
# ----- Inicia assets
background = pygame.image.load("assets\\img\\fundo.png").convert()
# ----- Inicia estruturas de dados
game = True

# ===== Loop principal =====
while game:
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Gera saídas
    window.fill((255, 255, 255))  # Preenche com a cor branca
    window.blit(background, (0, -80))
    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

