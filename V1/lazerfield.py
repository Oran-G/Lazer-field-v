import time
class Player():
    def __init__(self, o, dx, dy, mb=2):
        self.o = o
        if o == False:
            self.x = 0
            self.y = 0
        else:
            self.x = dx-1
            self.y = dy-1
        self.dx = dx
        self.dy = dy    
        self.bullets = list()
        self.m = True
        self.s = True
        self.maxb = mb
    def move(self, d):
        self.rmb()
        if d == 0:
            self.m = True
        elif self.m == True:
            self.x = max(0, min(self.x + d, self.dx - 1))
            self.m = False
    def shoot(self, s):
        self.rmb()
        if s == 0:
            self.s = True
        elif self.s == True and len(self.bullets) <= self.maxb:
            self.bullets.append(Bullet(self.x, self.o))    
            self.s = False
    def rmb(self):
        for bullet in self.bullets:
            if bullet.rm() == True:
                self.rmsb(bullet)
    def rmsb(self, bullet):
        self.bullets.remove(bullet)               



class Bullet():
    def __init__(self, x, o):
        self.x = x
        self.t = time.monotonic()
        self.o = o
    def rm(self):
        return True if time.monotonic() - self.t > .75 else False

class Lazer_field():
    def __init__(self, dx=12, dy=8, w=5):
        self.dx = dx
        self.dy = dy
        self.reset()
        self.p1s = 0
        self.p2s = 0
        self.win = w
        self.done = False
        self.winner = None
        self.name = None
        self.reset()
    def new_game(self, dx=12, dy=8, w=5):
        self.dx = dx
        self.dy = dy
        self.reset()
        self.p1s = 0
        self.p2s = 0
        self.win = w
        self.done = False
        self.winner = None
        self.name = None
        self.reset()
    def reset(self):
        self.p1 = Player(False, self.dx, self.dy)
        self.p2 = Player(True, self.dx, self.dy)   
    def collide(self):
        c1 = False

        self.p1.rmb()
        self.p2.rmb()
        for bullet in self.p1.bullets:
            if bullet.x == self.p2.x:
                c1 = True
                b1 = bullet
        c2 = False        
        for bullet in self.p2.bullets:
            if bullet.x == self.p1.x:
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
            




             


