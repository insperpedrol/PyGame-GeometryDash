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
pygame.display.set_caption('Cube Dash - Pygame Edition')
# ----- Inicia assets
player_WIDTH = 75
player_HEIGHT = 75
Camera = 0
elements = pygame.sprite.Group()
sprites = {}
sprites['background'] = pygame.image.load("assets\\img\\background.png").convert()
sprites['blue'] =  pygame.image.load("assets\\img\\blue.png").convert()
sprites['Player'] = pygame.image.load('assets\\img\\cubo.png').convert_alpha()

inicio =  pygame.image.load("assets\\img\\inicio2.png").convert()

fim = pygame.image.load("assets\\img\\fim.png").convert()

sprites['Spike'] = pygame.image.load('assets\\img\\spike.png').convert_alpha()
spike_novo = pygame.transform.scale(sprites['Spike'], (53, 53))

sprites['Moeda'] = pygame.image.load('assets\\img\\moeda.png').convert_alpha()
moeda = pygame.transform.scale(sprites['Moeda'], (60, 60))
sprites['Moeda'] = moeda

sprites['Spike'] = spike_novo
sprites['Player'] = pygame.transform.scale(sprites['Player'], (player_WIDTH, player_HEIGHT))

sprites['Bloco']  = pygame.image.load('assets\\img\\bloco.png').convert_alpha()
bloco_novo = pygame.transform.scale(sprites['Bloco'], (53, 53))
sprites['Bloco'] = bloco_novo


# --- Implementando musica

#som_morte = pygame.mixer.Sound('assets\\songs\\bomba.mp3')

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

# Classes
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

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)
        self.speedx = 9

    def update(self):
        self.rect.x -= self.speedx

class blocos(Draw):
    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)
        self.speedx =9
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
        self.speedx = 9
    
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right <= 0:
            self.rect.x = self.rect.width
class End(Draw):
    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)
        self.speedx =9
    def update(self):
        self.rect.x -= self.speedx

# le o mapa do jogo 
# lógica de leitura do mapa baseada no jogo desse repositorio https://github.com/y330/Pydash
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
    all_platforms = pygame.sprite.Group()
    all_ends = pygame.sprite.Group()
    x = 0
    y = 0
    for row in map:
        for col in row:
            if col == "Spike":
                all_spikes.add(Spike(sprites['Spike'], (x, y), elements))
            
            elif col == "Bloco":  
                all_platforms.add(blocos(sprites['Bloco'], (x, y), elements))
            
            elif col == "End":
                all_ends.add(End(sprites['Moeda'], (x, y), elements))
            
            x += 50
        y += 50 
        x = 0
    return all_spikes, all_platforms, all_ends



all_sprites = pygame.sprite.Group()
all_ends = pygame.sprite.Group()

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

all_spikes, all_platforms, all_ends = init_level(map_data)

# numero de mortes
tentativas = 0
BRANCO = (255, 255, 255)
fonte = pygame.font.Font(None, 38) 
texto = (f'Mortes: {tentativas}')
texto_ =  fonte.render(texto, True, BRANCO)
posicao = (8, 5)

# carrega musica 
pygame.mixer.music.load('assets\\songs\\gdsong.wav')
pygame.mixer.music.set_volume(0.3)


jogo = 'inicio'
# ===== Loop principal =====
while game:
    
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências  
        if event.type == pygame.MOUSEBUTTONDOWN:
                jogo = 'jogando'
                pygame.mixer.music.play()
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
    
    if pygame.sprite.spritecollide(player, all_spikes, False):
        player.volta_posicao()
        all_spikes.empty()
        all_platforms.empty()
        elements.empty()
        all_spikes, all_platforms, all_ends = init_level(map_data)
        pygame.mixer.music.stop()
        pygame.mixer.music.play()
        tentativas += 1
        texto = (f'Mortes: {tentativas}')
        texto_ =  fonte.render(texto, True, BRANCO) 
    
    if pygame.sprite.spritecollide(player, all_platforms, False):
        platform = pygame.sprite.spritecollideany(player, all_platforms)
        player.rect.bottom = platform.rect.top
        player.on_ground = True
    
    if pygame.sprite.spritecollide(player, all_ends, False):
            window.fill((255, 255, 255))  
            window.blit(fim, (0, 0))  
            pygame.display.update()
            pygame.mixer.music.stop()
            pygame.time.wait(3000) 
            game = False
    


    # ----- Gera saídas
    if jogo == 'inicio':

        window.fill((255, 255, 255))
        window.blit(inicio, (0,0))
        pygame.display.update()

    else: 

        window.fill((255, 255, 255))  # Preenche com a cor branca
        Camera = -fundo1.speedx
        all_sprites.draw(window)
        all_spikes.draw(window)
        all_platforms.draw(window)
        all_ends.draw(window)
        elements.draw(window)
        window.blit(texto_, posicao)

        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador
        all_sprites.update()
        all_spikes.update()
        all_platforms.update()
        all_ends.update()

    FPS = 120
    clock.tick(FPS)

# ===== Finalização =====
pygame.quit() 