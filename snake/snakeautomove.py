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
        self.ocupada = True
    def nuevo(self):
        self.comidas = pygame.sprite.Group()
        self.cabezas = pygame.sprite.Group()
        self.colas = pygame.sprite.Group()
    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jugando = False
    def posCola(self):
        for i in range(len(self.snake)-1,0,-1):
            self.snake[i].rect.x = self.snake[i-1].rect.x
            self.snake[i].rect.y = self.snake[i-1].rect.y
    def generarCabeza(self):
        cabeza = Cabeza(self)
        self.snake.append(cabeza)
        self.cabezas.add(cabeza)
        self.hay_cabeza = True
    def generarComida(self):
        while self.ocupada:
            x = random.randint(0,(ANCHO/CASILLA)-1)
            y = random.randint(0,(ALTO/CASILLA)-1)
            for item in self.snake:
                if (x == item.rect.x) and (y == item.rect.y):
                    self.ocupada = True
                    continue
            self.ocupada = False
        comida = Comida(self,random.randint(0,(ANCHO/CASILLA)-1),random.randint(0,(ALTO/CASILLA)-1))
        self.ocupada = True
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
    def __init__(self,juego):
        pygame.sprite.Sprite.__init__(self)
        self.juego = juego
        self.image = pygame.Surface([CASILLA,CASILLA])
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
    def update(self):
        pass

class Cabeza(pygame.sprite.Sprite):
    def __init__(self,juego):
        pygame.sprite.Sprite.__init__(self)
        self.juego = juego
        self.image = pygame.Surface([CASILLA,CASILLA])
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO/2
        self.rect.y = ALTO/2
        self.vel_x = CASILLA
        self.vel_y = CASILLA
        self.dir = 6
        self.x = self.rect.x
        self.y = self.rect.y
        self.direcciones = [2,8,6,4]
    def colisionCuerpo(self):
        for item in self.juego.colas:
            if pygame.sprite.collide_rect(self,item):
                print "colision cuerpo"
                pygame.quit()
                sys.exit()
    def colisionComida(self):
        for item in self.juego.comidas:
            if pygame.sprite.collide_rect(self,item):
                item.kill()
                del item
                self.juego.cantidad_comida = 0
                cola = Cola(self.juego)
                self.juego.snake.append(cola)
                self.juego.colas.add(cola)
    def mover(self):
        change = False
        while not change:
            nextdir = self.direcciones[random.randint(0,3)]
            if (nextdir == 6 and self.dir == 4) or (nextdir == 4 and self.dir == 6) or (nextdir == 2 and self.dir== 8) or (nextdir == 8 and self.dir == 2):
                pass
            else:
                self.dir = nextdir
                change = True          
    def update(self):
        self.colisionComida()
        self.juego.posCola()
        self.mover()
        if ((self.dir == 6)and(self.rect.x<(ANCHO-CASILLA)) and (self.dir!=4)):
            self.rect.x += self.vel_x
        elif ((self.dir == 4)and(self.rect.x>0)and (self.dir!=6)):
            self.rect.x -= self.vel_x
        elif ((self.dir == 8)and(self.rect.y<ALTO-CASILLA)and (self.dir!=2)):
            self.rect.y += self.vel_y
        elif ((self.dir == 2)and(self.rect.y>0)and (self.dir!=8)):
            self.rect.y -= self.vel_y
        self.colisionCuerpo()
        if self.dir == 2:
            self.y-=CASILLA
            if self.y<0:
                print "colision arriba"
                pygame.quit()
                sys.exit()
        elif self.dir == 8:
            self.y+=CASILLA
            if self.y>=ALTO:
                print "colision abajo"
                pygame.quit()
                sys.exit()
        elif self.dir == 6:
            self.x+=CASILLA
            if self.x>=ANCHO:
                print "colision derecha"
                pygame.quit()
                sys.exit()
        elif self.dir == 4:
            self.x-=CASILLA
            if self.x<0:
                print "colision izquierda"
                pygame.quit()
                sys.exit()
   
    
if __name__ == "__main__":
    juego = Juego()
    reloj = pygame.time.Clock()
    juego.nuevo()
    while juego.jugando:
        juego.update()
        juego.dibujar()
        juego.eventos()
        reloj.tick(20)
    pygame.quit()
    sys.exit()
    


