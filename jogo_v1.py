# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
pygame.init()

# ----- Gera tela principal
WIDTH = 1030
HEIGHT = 405
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Geometry Dash - Python Edition')
# ----- Inicia assets
CUBO_WIDTH = 45
CUBO_HEIGHT = 45
background = pygame.image.load("assets\\img\\fundo.png").convert()
cubo_img = pygame.image.load('assets\img\cubo.png').convert_alpha()
cubo_img = pygame.transform.scale(cubo_img, (CUBO_WIDTH, CUBO_HEIGHT))

# ----- Inicia estruturas de dados

game = True
clock = pygame.time.Clock()
FPS = 30
class cubo(pygame.sprite.Sprite):
        def __init__(self,img):
            pygame.sprite.Sprite.__init__(self)
            self.image = img    
            self.rect = self.image.get_rect()
            self.rect.centerx = 30
            self.rect.bottom = 395
            self.speedx = 5
            self.jump_speed = -10  
            self.gravity = 0.5  
            self.vel_y = 5  
            self.on_ground = True  

        def update(self):
            self.rect.x += self.speedx

            if not self.on_ground:
                self.vel_y += self.gravity
                self.rect.y += self.vel_y

                
                if self.rect.bottom >= HEIGHT - 30:  
                    self.rect.bottom = HEIGHT - 30  
                    self.on_ground = True  
                    self.vel_y = 0  

        def jump(self):
       
            if self.on_ground:
                self.vel_y = self.jump_speed  
                self.on_ground = False

all_sprites = pygame.sprite.Group()
player = cubo(cubo_img)
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
    window.blit(background, (0, -180))
    all_sprites.draw(window)
    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador
    clock.tick(FPS)
# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

