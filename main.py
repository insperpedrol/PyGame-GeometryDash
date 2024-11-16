# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import csv
import os   
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
Camera = 0
elements = pygame.sprite.Group()


#  gerando dicionairios
sprites = {}
sprites['background'] = pygame.image.load("assets\\img\\background.png").convert()
sprites['blue'] =  pygame.image.load("assets\\img\\blue.png").convert()
sprites['Player'] = pygame.image.load('assets\\img\\cubo.png').convert_alpha()
sprites['Spike'] = pygame.image.load('assets\\img\\spike.png').convert_alpha()
spike_resized = pygame.transform.scale(sprites['Spike'], (50, 50))
sprites['Spike'] = spike_resized
sprites['Player'] = pygame.transform.scale(sprites['Player'], (player_WIDTH, player_HEIGHT))


pygame.mixer.music.load('assets\\songs\\gdsong.wav')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

# --- Adicionando fundo
backcolorWIDTH = 720
backcolorHEIGHT = backcolorWIDTH
backcolor = pygame.Surface((backcolorWIDTH, backcolorHEIGHT))
backcolor.set_alpha(128)
backcolor.fill((53, 107, 232))

# --- Adicionando chao 
backcolorWIDTH2 = 720
backcolorHEIGHT2 = backcolorWIDTH2
backcolor2 = pygame.Surface((backcolorWIDTH2, backcolorHEIGHT2))
backcolor2.set_alpha(128)
backcolor2.fill((52, 128, 235))

# ----- Inicia estruturas de dados

game = True
clock = pygame.time.Clock()

# Parent class
class Draw(pygame.sprite.Sprite):

    def __init__(self, image, pos, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

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
            self.speedy += self.gravity
            self.rect.y += self.speedy
            if self.rect.bottom >= HEIGHT / 1.3:
                self.rect.bottom = HEIGHT / 1.3
                self.on_ground = True
                self.speedy = 0
        def volta_posicao(self):
            self.rect.centerx = WIDTH / 5.2
            self.rect.bottom = HEIGHT / 1.3
            self.speedy = 0
            self.on_ground = True

class Block(pygame.sprite.Sprite):
    def __init__(self, img):
        self.img = img

class Platform(pygame.sprite.Sprite):
    def __init__(self, img):
        self.img = img

class Spike(Draw):
    """spike"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)
        self.speedx = 10

    def update(self):
        self.rect.x -= self.speedx



class Fundo(pygame.sprite.Sprite):
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.speedx = 1
    
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right <= 0:
            self.rect.x = self.rect.width

class Floor(pygame.sprite.Sprite):
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT / 1.3
        self.speedx = 10
    
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right <= 0:
            self.rect.x = self.rect.width


def load_map(filename):
    with open(filename, newline='') as csvfile:
        map_data = []
        csv_reader = csv.reader(csvfile, delimiter=';')
        for row in csv_reader:
            map_data.append([(cell) for cell in row])
    return map_data


map_data = load_map("assets\\maps\\level_1.csv")
elements = pygame.sprite.Group()

def init_level(map):
    all_spikes = pygame.sprite.Group()
    x = 0
    y = 0
    for row in map:
        for col in row:
            if col == "Spike":
                all_spikes.add(Spike(sprites['Spike'], (x, y), elements))
            x += 50
        y += 50 
        x = 0
    return all_spikes



all_sprites = pygame.sprite.Group()

player = Player(sprites['Player'])

fundo1 = Fundo(sprites['blue'])
fundo2 = Fundo(sprites['blue'])
fundo2.rect.x += fundo2.rect.width

spikes = Fundo(sprites['Spike'])

all_sprites.add(fundo1)
all_sprites.add(fundo2)

floor1 = Floor(sprites['blue'])
floor2 = Floor(sprites['blue'])
floor2.rect.x += floor2.rect.width
all_sprites.add(floor1)
all_sprites.add(floor2)


all_sprites.add(player)

all_spikes = init_level(map_data)

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
    
    if pygame.sprite.spritecollide(player, all_spikes, False):
        player.volta_posicao() 
        all_spikes = init_level(map_data)
        pygame.mixer.music.play()
        


    # ----- Gera saídas
    window.fill((255, 255, 255))  # Preenche com a cor branca

    Camera = -fundo1.speedx
    all_sprites.draw(window)
    all_spikes.draw(window)
    elements.draw(window)

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador
    all_sprites.update()
    all_spikes.update()

    FPS = 120
    clock.tick(FPS)

# ===== Finalização =====
pygame.quit() 