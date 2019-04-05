import pygame
import sys
import random

ANCHO = 600
ALTO = 400
CASILLA = 10
BLANCO = (255,255,255)
NEGRO = (0,0,0)
ROJO = (255,0,0)
AZUL = (0,0,255)
VERDE = (0,255,0)
class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode([ANCHO,ALTO])
        pygame.display.set_caption("culebrita")
        self.score = 0
        self.jugando = True
        self.cantidad_comida = 0
        self.hay_cabeza=False
    def nuevo(self):
        self.comidas = pygame.sprite.Group()
        self.cabezas = pygame.sprite.Group()
        self.colas = pygame.sprite.Group()
    def dibujarCuadricula(self):
        for x in range (0,ANCHO,CASILLA):
            pygame.draw.line(self.pantalla,BLANCO,(x,0),(x,ANCHO))
        for x in range (0,ALTO,CASILLA):
            pygame.draw.line(self.pantalla,BLANCO,(0,x),(ANCHO,x))
    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jugando = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    for elemento in self.cabezas:
                        elemento.moverArriba()                    
                if event.key == pygame.K_DOWN:
                    for elemento in self.cabezas:
                        elemento.moverAbajo()
                if event.key == pygame.K_LEFT:
                    for elemento in self.cabezas:
                        elemento.moverIzquierda()
                if event.key == pygame.K_RIGHT:
                    for elemento in self.cabezas:
                        elemento.moverDerecha()
    def generarCabeza(self):
        cabeza = Cabeza(self)
        self.cabezas.add(cabeza)
        self.hay_cabeza = True
    def generarComida(self):
        
        comida = Comida(self,random.randint(0,(ANCHO/CASILLA)-1),random.randint(0,(ALTO/CASILLA)-1))
        #comida = Comida(self,0,0)
        self.comidas.add(comida)
        self.cantidad_comida=1
    def update(self):
        if self.hay_cabeza==False:
            self.generarCabeza()
        if self.cantidad_comida == 0:
            self.generarComida()
    def dibujar(self):
        
        self.pantalla.fill(NEGRO)
        self.dibujarCuadricula()
        self.cabezas.draw(self.pantalla)
        self.comidas.draw(self.pantalla)
        pygame.display.flip()
    def ejecutar(self):
        pass


class Comida(pygame.sprite.Sprite):
    def __init__(self,juego,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.juego = juego
        self.image = pygame.Surface([CASILLA,CASILLA])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = x*CASILLA
        self.rect.y = y*CASILLA

class Cola(pygame.sprite.Sprite):
    def __init__(self,juego,dir,xpre,ypre):
        pygame.sprite.Sprite.__init__(self)
        self.juego = juego
        self.image = pygame.Surface([CASILLA,CASILLA])
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()

class Cabeza(pygame.sprite.Sprite):
    def __init__(self,juego):
        pygame.sprite.Sprite.__init__(self)
        self.juego = juego
        self.image = pygame.Surface([CASILLA,CASILLA])
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO/2
        self.rect.y = ALTO/2
    def moverArriba(self):
        self.rect.y-=CASILLA
    def moverAbajo(self):
        self.rect.y+=CASILLA
    def moverDerecha(self):
        self.rect.x+=CASILLA
    def moverIzquierda(self):
        self.rect.x-=CASILLA
   
    
if __name__ == "__main__":
    juego = Juego()
    reloj = pygame.time.Clock()
    juego.nuevo()
    #comida = Comida(juego,0,0)
    #juego.comidas.add(comida)
    #juego.comidas.draw(juego.pantalla)
    while juego.jugando:
        #juego.nuevo()
        juego.update()
        #juego.comidas.draw(juego.pantalla)
        juego.dibujar()
        juego.eventos()
        reloj.tick(50)
    pygame.quit()
    sys.exit()
    


