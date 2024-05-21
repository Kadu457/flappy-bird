import pygame as pg
import os
import random
from menu import menu_inicial

ALTURA_TELA = 800
LARGURA_TELA = 500
IMG_BASE = pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'base.png')))
IMG_BG = pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bg.png')))
IMG_CANO = pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'pipe.png')))
IMG_BIRD = [
    pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bird1.png'))),
    pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bird2.png'))),
    pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bird3.png')))
]
pg.font.init()
FONTE_PONTOS = pg.font.SysFont('Flappy Bird', 50)

class Passaro:
    IMGS = IMG_BIRD
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 15
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.altura = self.y
        self.velocidade = 0
        self.tempo = 0
        self.contagem_img = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.altura = self.y
        self.tempo = 0

    def mover(self):
        # Calculo Deslocamento
        aceleracao = 1.5
        self.tempo += 1
        deslocamento = aceleracao * (self.tempo**2) + self.velocidade * self.tempo

        # Restrinção
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # Calculo Ângulo
        if deslocamento < 0 or self.y < (self.altura - 20):
            self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -60:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def mostrar(self, tela):
        # Animação Pássaro
        if self.contagem_img < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_img < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_img < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_img < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_img < self.TEMPO_ANIMACAO*5:
            self.imagem = self.IMGS[0]
            self.contagem_img = 0
        self.contagem_img += 1

        # Não bater asa caindo
        if self.angulo < -80:
            self.imagem = self.IMGS[1]
            self.contagem_img = self.TEMPO_ANIMACAO*2

        # Desenhar o pássaro
        imagem_rotacionada = pg.transform.rotate(self.imagem, self.angulo)
        pos_centro = imagem_rotacionada.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro)
        tela.blit(imagem_rotacionada, retangulo)

        # Colisão

    def get_mask(self):
        return pg.mask.from_surface(self.imagem)

class Cano:
    VELOCIDADE = 5
    DISTANCIA = 200

    def __init__(self, x):
        self.x = x
        self.CANO_TOPO = pg.transform.flip(IMG_CANO, False, True)
        self.CANO_BASE = IMG_CANO
        self.pos_base = 0
        self.pos_topo = 0
        self.definir_altura()
        self.altura = 0
        self.passou = False

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def colidir(self, passaro):
        bird_mask = passaro.get_mask()
        topo_mask = pg.mask.from_surface(self.CANO_TOPO)
        base_mask = pg.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        colisao_topo = bird_mask.overlap(topo_mask, distancia_topo)
        colisao_base = bird_mask.overlap(base_mask, distancia_base)

        if colisao_base or colisao_topo:
            return True
        else:
            return False

    def mover(self):
        self.x -= self.VELOCIDADE

    def mostrar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))


class Base:
    VELOCIDADE = 5
    IMG = IMG_BASE
    LARGURA = IMG.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def mostrar(self, tela):
        tela.blit(self.IMG, (self.x1, self.y))
        tela.blit(self.IMG, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMG_BG, (0,0))
    for passaro in passaros:
        passaro.mostrar(tela)
    for cano in canos:
        cano.mostrar(tela)
    chao.mostrar(tela)
    texto = FONTE_PONTOS.render(f"{pontos}", 1, (255,255,255))
    tela.blit(texto, (LARGURA_TELA / 2 - texto.get_width(), 100))
    pg.display.update()

def main():
    replay = True
    while replay:
        replay = False

        tela = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        play = menu_inicial(tela)

        passaros = [Passaro(230, 350)]
        canos = [Cano(730)]
        chao = Base(700)
        pontos = 0
        relogio = pg.time.Clock()

        while play:
            relogio.tick(30)

            # Interação com usuário
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    play = False
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        passaro.pular()
                    if event.key == pg.K_F5:
                        play = False
                        replay = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    passaro.pular()

            # Mover os objetos
            for passaro in passaros:
                passaro.mover()

            chao.mover()

            adicionar_cano = False
            canos_remover = []
            for cano in canos:
                for i, passaro in enumerate(passaros):
                    if cano.colidir(passaro):
                        passaros.pop(i)
                    if not cano.passou and passaro.x > cano.x:
                        cano.passou = True
                        adicionar_cano = True
                cano.mover()
                if cano.x + cano.CANO_TOPO.get_width() < 0:
                    canos_remover.append(cano)

            if adicionar_cano:
                pontos += 1
                canos.append(Cano(700))

            for cano in canos_remover:
                canos.remove(cano)

            passaro_remover = []
            for passaro in passaros:
                if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                    passaro_remover.append(passaro)
            for passaro in passaro_remover:
                passaros.remove(passaro)

            desenhar_tela(tela, passaros, canos, chao, pontos)

if __name__ == '__main__':
    main()