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
        self.snake = []
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
                        if elemento.dir != 8:
                            elemento.moverArriba()                    
                if event.key == pygame.K_DOWN:
                    for elemento in self.cabezas:
                        if elemento.dir != 2:
                            elemento.moverAbajo()
                if event.key == pygame.K_LEFT:
                    for elemento in self.cabezas:
                        if elemento.dir != 6:
                            elemento.moverIzquierda()
                if event.key == pygame.K_RIGHT:
                    for elemento in self.cabezas:
                        if elemento.dir != 4:
                            elemento.moverDerecha()
    def generarCabeza(self):
        cabeza = Cabeza(self)
        self.snake.append(cabeza)
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
        self.cabezas.update()
        self.colas.update()
    def dibujar(self):
        
        self.pantalla.fill(NEGRO)
        self.dibujarCuadricula()
        self.cabezas.draw(self.pantalla)
        self.comidas.draw(self.pantalla)
        self.colas.draw(self.pantalla)
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
    def __init__(self,juego,xpre,ypre,anterior):
        pygame.sprite.Sprite.__init__(self)
        self.juego = juego
        self.image = pygame.Surface([CASILLA,CASILLA])
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = xpre
        self.rect.y = ypre
        self.anterior = anterior
        self.prepos = []
    def update(self):
        self.prepos = [self.rect.x,self.rect.y]
        self.rect.x = self.anterior.prepos[0]
        self.rect.y = self.anterior.prepos[1]

class Cabeza(pygame.sprite.Sprite):
    def __init__(self,juego):
        pygame.sprite.Sprite.__init__(self)
        self.juego = juego
        self.image = pygame.Surface([CASILLA,CASILLA])
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO/2
        self.rect.y = ALTO/2
        self.vel_x = 0
        self.vel_y = 0
        self.dir = -1
        self.x = self.rect.x
        self.y = self.rect.y
        self.prepos = []

    def moverArriba(self):
        if self.dir == 8:
            self.dir = 2
        elif self.dir!=2:
            self.vel_y+=CASILLA
            self.vel_x = 0
            self.dir = 2
    def moverAbajo(self):
        if self.dir == 2:
            self.dir = 8
        elif self.dir!=8:
            self.vel_y+=CASILLA
            self.vel_x = 0
            self.dir = 8
    def moverDerecha(self):
        if self.dir == 4:
            self.dir = 6
        elif self.dir!=6:
            self.vel_x+=CASILLA
            self.vel_y = 0
            self.dir = 6
    def moverIzquierda(self):
        if self.dir == 6:
            self.dir = 4
        elif self.dir!= 4:
            self.vel_x+=CASILLA
            self.vel_y = 0
            self.dir = 4
    def colisionComida(self):
        for item in self.juego.comidas:
            if pygame.sprite.collide_rect(self,item):
                print "colision comida"
                item.kill()
                del item
                self.juego.cantidad_comida = 0
                cola = Cola(self.juego,self.juego.snake[-1].prepos[0],self.juego.snake[-1].prepos[1],self.juego.snake[-1])
                self.juego.colas.add(cola)
                self.juego.snake.append(cola)
    def update(self):
        self.colisionComida()
        if ((self.dir == 6)and(self.rect.x<(ANCHO-CASILLA))):
            self.prepos = [self.rect.x,self.rect.y]
            self.rect.x += self.vel_x
        if ((self.dir == 4)and(self.rect.x>0)):
            self.prepos = [self.rect.x,self.rect.y]
            self.rect.x -= self.vel_x
        if ((self.dir == 8)and(self.rect.y<ALTO-CASILLA)):
            self.prepos = [self.rect.x,self.rect.y]
            self.rect.y += self.vel_y
        if ((self.dir == 2)and(self.rect.y>0)):
            self.prepos = [self.rect.x,self.rect.y]
            self.rect.y -= self.vel_y
        #self.colisionComida()
        if self.dir == 2:
            self.y-=CASILLA
            if self.y<0:
                print "colision arriba"
                pygame.quit()
                sys.exit()
        if self.dir == 8:
            self.y+=CASILLA
            if self.y>=ALTO:
                print "colision abajo"
                pygame.quit()
                sys.exit()
        if self.dir == 6:
            self.x+=CASILLA
            if self.x>=ANCHO:
                print "colision derecha"
                pygame.quit()
                sys.exit()
        if self.dir == 4:
            self.x-=CASILLA
            if self.x<0:
                print "colision izquierda"
                pygame.quit()
                sys.exit()
   
    
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
        reloj.tick(5)
    pygame.quit()
    sys.exit()
    


