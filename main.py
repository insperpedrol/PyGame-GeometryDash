# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
pygame.init()

# ----- Gera tela principal
WIDTH = 720
HEIGHT = 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Geometry Dash - Python Edition')
# ----- Inicia assets
player_WIDTH = 75
player_HEIGHT = 75

sprites = {}
sprites['background'] = pygame.image.load("assets\\img\\background.png").convert()
sprites['Player'] = pygame.image.load('assets\img\cubo.png').convert_alpha()

sprites['Player'] = pygame.transform.scale(sprites['Player'], (player_WIDTH, player_HEIGHT))


backcolorWIDTH = 720
backcolorHEIGHT = backcolorWIDTH
backcolor = pygame.Surface((backcolorWIDTH, backcolorHEIGHT))
backcolor.set_alpha(128)
backcolor.fill((53, 107, 232))

backcolorWIDTH2 = 720
backcolorHEIGHT2 = backcolorWIDTH2
backcolor2 = pygame.Surface((backcolorWIDTH2, backcolorHEIGHT2))
backcolor2.set_alpha(128)
backcolor2.fill((52, 128, 235))

# ----- Inicia estruturas de dados

game = True
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
        def __init__(self,img):
            pygame.sprite.Sprite.__init__(self)
            self.image = img

            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH / 5.2
            self.rect.bottom = HEIGHT / 1.3

            self.gravity = 0.3
            self.jump_speed = -9
            self.speedy = 2.5
            self.on_ground = True

        def jump(self):
            if self.on_ground:
                self.speedy = self.jump_speed
                self.on_ground = False

        def update(self):
            if not self.on_ground:
                self.speedy += self.gravity
                self.rect.y += self.speedy
                if self.rect.bottom >= HEIGHT / 1.3:
                    self.rect.bottom = HEIGHT / 1.3
                    self.on_ground = True
                    self.speedy = 0

class Block(pygame.sprite.Sprite):
    def __init__(self, img):
        self.img = img

class Platform(pygame.sprite.Sprite):
    def __init__(self, img):
        self.img = img

class Spike(pygame.sprite.Sprite):
    def __init__(self, img):
        self.img = img

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

    # Coloca o background
    window.blit(sprites['background'], (0, 0))
    window.blit(backcolor, (0, 0))

    # Coloca o chao
    window.blit(sprites['background'], (0, HEIGHT / 1.3))
    window.blit(backcolor2, (0, HEIGHT / 1.3))
    all_sprites.draw(window)

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador
    all_sprites.update()

    FPS = 120
    clock.tick(FPS)

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

