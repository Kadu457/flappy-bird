import pygame as pg
import os

LARGURA_TELA = 500
ALTURA_TELA = 800
IMG_BG = pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bg.png')))
IMG_LOGO = pg.transform.scale_by(pg.image.load(os.path.join('imgs', 'logo.png')), 0.85)
IMG_START = pg.transform.scale_by(pg.image.load(os.path.join('imgs', 'start_btn.png')), 0.8)
IMG_EXIT = pg.transform.scale_by(pg.image.load(os.path.join('imgs', 'exit_btn.png')), 0.8)
IMG_GAMEOVER = pg.transform.scale_by(pg.image.load(os.path.join('imgs', 'gameover.png')), 0.4)

tela = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA))

class Button:
    def __init__(self, img, y, x=0):
        self.imagem = img
        self.y = y
        if x == 0:
            self.x = LARGURA_TELA / 2 - img.get_width() / 2
        else:
            self.x = x

    def mostrar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

    def click(self, x, y):
        retangulo = self.imagem.get_rect(topleft=(self.x, self.y))
        if retangulo.collidepoint(x, y):
            return True
        else:
            return False

def menu_inicial(tela):

    start = Button(IMG_START, 350)
    exit = Button(IMG_EXIT, 500)

    play = True
    while play:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                play = False
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if exit.click(x, y):
                    play = False
                    pg.quit()
                    quit()
                elif start.click(x, y):
                    return True
        tela.blit(IMG_BG, (0,0))
        tela.blit(IMG_LOGO, (250 - IMG_LOGO.get_width() / 2, 100))
        start.mostrar(tela)
        exit.mostrar(tela)
        pg.display.update()

def menu_final(tela):
    x1 = (LARGURA_TELA - (IMG_START.get_width() + IMG_EXIT.get_width() + 40)) / 2
    x2 = x1 + IMG_START.get_width() + 40
    start = Button(IMG_START, 500, x1)
    exit = Button(IMG_EXIT, 500, x2)
    over = Button(IMG_GAMEOVER, 100)

    play = True
    while play:
        tela.blit(IMG_BG, (0,0))
        over.mostrar(tela)
        start.mostrar(tela)
        exit.mostrar(tela)
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                play = False
                pg.quit()
                quit()

