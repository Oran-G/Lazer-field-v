import time
import pygame
import os
class Player():
    def __init__(self, o, dx, dy, hitbox, mb=7, speed=10):
        self.o = o
        if o == False:
            self.x = 0
            self.y = 0
        else:
            self.x = dx - hitbox - 40
            self.y = dy - hitbox  -  40
        self.hb = hitbox
        self.speed = speed
        self.dx = dx
        self.dy = dy    
        self.bullets = list()
        self.s = True
        self.maxb = mb
    def move(self, d):
        self.rmb()
        self.x = max(20, min(self.x + (d * self.speed), self.dx - self.hb))
    def shoot(self, s):
        self.rmb()
        if s == 0:
            self.s = True
        elif self.s == True and len(self.bullets) <= self.maxb:
            self.bullets.append(Bullet(self.x, self.o, self.y, self.hb, dy = self.dy))    
            self.s = False
    def rmb(self):
        for bullet in self.bullets:
            if bullet.rm() == True:
                self.rmsb(bullet)
    def rmsb(self, bullet):
        self.bullets.remove(bullet)               



class Bullet():
    def __init__(self, x, o, y, hx, dy, speed=20, hy=60):
        self.x = x
        self.t = time.monotonic()
        self.o = o
        self.speed = speed
        self.y = y
        self.hx = hx
        self.hy = hy
        self.dy = dy + 40
    def rm(self):
        if time.monotonic() - self.t > .75 or self.y >= self.dy:
            return True
        else: 
            return False
    def update(self):
        if self.o == True:
            self.y-=self.speed
        else:
            self.y+=self.speed

ph1 = 0

class Lazer_field():
    def __init__(self, ph, dx=540, dy=385, w=5):
        self.dx = dx
        self.dy = dy
        self.reset()
        self.p1s = 0
        self.p2s = 0
        self.win = w
        self.done = False
        self.winner = None
        self.name = None
        self.ph = ph
        ph1 = ph  
        
    def new_game(self, ph, dx=540, dy=385, w=5):
        self.dx = dx
        self.dy = dy
        self.reset()
        self.p1s = 0
        self.p2s = 0
        self.win = w
        self.done = False
        self.winner = None
        self.name = None
        self.ph = ph
        print("hello")
        self.reset()
    def reset(self):
        self.p1 = Player(False, self.dx, dy=self.dy, hitbox=ph1)
        self.p2 = Player(True, self.dx, dy=self.dy, hitbox=ph1)   
    def collide(self):
        c1 = False

        self.p1.rmb()
        self.p2.rmb()
        for bullet in self.p1.bullets:
            if ((bullet.x > self.p2.x and bullet.x < self.p2.x + self.p2.hb) or (bullet.x + bullet.hx > self.p2.x and bullet.x + bullet.hx < self.p2.x + self.p2.hb)):
                if ((bullet.y < self.p2.y and bullet.y + bullet.hy > self.p2.y) or (bullet.y + bullet.hy > self.p2.y + self.p2.hb and bullet.y < self.p2.y + self.p2.hb)):
                    c1 = True
                    b1 = bullet
        c2 = False        
        for bullet in self.p2.bullets:
            if ((bullet.x > self.p1.x and bullet.x < self.p1.x + self.p1.hb) or (bullet.x + bullet.hx > self.p1.x and bullet.x + bullet.hx < self.p1.x + self.p1.hb)):
                if ((bullet.y < self.p1.y and bullet.y + bullet.hy > self.p1.y) or (bullet.y + bullet.hy > self.p1.y + self.p1.hb and bullet.y < self.p1.y + self.p1.hb)):
                    
                    c2 = True
                    b2 = bullet
        if c1 == True and c2 == True:
            if b2.t > b1.t:
                self.p1.rmsb(b1)
                self.reset()
                return self.won()
                
            elif b1.t > b2.t:
                self.p2.rmsb(b2) 
                self.reset()
                return self.won()
                
            else:
                self.p2.rmsb(b2)
                self.p1.rmsb(b1)
        elif c1 == True:
            self.p1s +=1
            self.reset()
            return self.won()
            
        elif c2 == True:
            self.p2s += 1
            self.reset()
            return self.won()
              
        return 0    
    def won(self):
        if self.p1s >=self.win:
            self.done = True
            self.winner = self.p1
            self.name = "Player 1"
            return 1
        elif self.p2s >= self.win:
            self.done = True
            self.winner = self.p1
            self.name = "Player 2"
            return -1    
        return 0    

    def __str__(self):
        s = f"P1: X {self.p1.x} p2: X {self.p2.x}\n"
        for i in range(self.dy):
            for j in range(self.dx):
                q = True
                if i == self.p1.y and j == self.p1.x:
                    s+="#"
                    q = False
                elif i == self.p2.y and j == self.p2.x:
                    s+="#"
                    q = False
                if q ==True:
                    for bullet in self.p1.bullets:
                        if bullet.x == j:
                            s+="X"
                            q = False
                            break
                if q == True:  
                    for bullet in self.p2.bullets:
                        if bullet.x == j:
                            s+="X"
                            q = False
                            break    
                if q == True:
                    s+="_"
            s+=f"\n"        

        return s
            




             



def load_image(file):
    """ loads an image, prepares it for play
    """
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    file = os.path.join(main_dir, "assets", file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert()