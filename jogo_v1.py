# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
pygame.init()

# ----- Gera tela principal
WIDTH = 1080
HEIGHT = 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Geometry Dash - Python Edition')
# ----- Inicia assets
CUBO_WIDTH = 45
CUBO_HEIGHT = 45

sprites = {}
sprites['background'] = pygame.image.load("assets\\img\\fundo.png").convert()
sprites['Player'] = pygame.image.load('assets\img\cubo.png').convert_alpha()

sprites['Player'] = pygame.transform.scale(sprites['Player'], (CUBO_WIDTH, CUBO_HEIGHT))

# ----- Inicia estruturas de dados

game = True
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
        def __init__(self,img):
            pygame.sprite.Sprite.__init__(self)
            self.image = img

            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH / 3
            self.rect.bottom = HEIGHT / 1.3

            self.speedx = 1.5
            self.gravity = 0.25
            self.jump_speed = -7
            self.speedy = 2.5
            self.on_ground = True

        def jump(self):
            if self.on_ground:
                self.speedy = self.jump_speed
                self.on_ground = False

        def update(self):
            self.rect.x += self.speedx

            if not self.on_ground:
                self.speedy += self.gravity
                self.rect.y += self.speedy
                if self.rect.bottom >= HEIGHT / 1.3:
                    self.rect.bottom = HEIGHT / 1.3
                    self.on_ground = True
                    self.speedy = 0

all_sprites = pygame.sprite.Group()
player = Player(sprites['Player'])
all_sprites.add(player)

# ===== Loop principal =====
while game:

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências  
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # ----- Gera saídas
    window.fill((255, 255, 255))  # Preenche com a cor branca
    window.blit(sprites['background'], (0, -180))
    all_sprites.draw(window)

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador
    all_sprites.update()

    FPS = 120
    clock.tick(FPS)

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

