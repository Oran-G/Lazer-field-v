import pygame
import sys
import time
import random
from lazerfield import Lazer_field, load_image

HEIGHT = 8
WIDTH = 12
MINES = 8

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Create game
pygame.init()
size = width, height = 580, 425
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
BOARD_PADDING = 20
board_width = width - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

instructions = True
game = Lazer_field(cell_size)
game.new_game(cell_size)
stars = set()
for i in range(random.randint(50, 500)):
    stars.add((random.randint(0, width),  random.randint(0, height)))
print(game.p1.hb)   
p2b = False
lp2b = False
p1b = False
lp1b = False
show_hb = False
lshow_hb = False
while True:
    if game.done == False:
        screen.fill(BLACK)
        # Check if game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_q] == True:
            if lp2b == False:
                p2b = not(p2b)
                lp2b = True
        else:
            lp2b = False 

        if keystate[pygame.K_SLASH] == True:
            if lp1b == False:
                p1b = not(p1b)
                lp1b = True
        else:
            lp1b = False 
        game.p1.move(keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT])
        sh = keystate[pygame.K_UP] or keystate[pygame.K_DOWN]
        game.p1.shoot(sh, b=p1b) 
        game.p2.move(keystate[pygame.K_d] - keystate[pygame.K_a])
        sh = keystate[pygame.K_w] or keystate[pygame.K_s]
        
        if keystate[pygame.K_h] == True:
            if lshow_hb == False:
                show_hb = not(p1b)
                lshow_hb = True
        else:
            lshow_hb = False 
             
        game.p2.shoot(sh, b=p2b)
        
        for star in stars:
            pygame.draw.rect(screen, (255, 255,255), (star[0], star[1], 1, 1))
        # print(game)
        # print(game.collide())
        if keystate[pygame.K_m] == True:
            print(game)
        game.collide()
        game.p1.rmb()
        game.p2.rmb()
        line = smallFont.render(f"Player 1: {game.p1s}", True, WHITE)
        lineRect = line.get_rect()
        lineRect.center = (65, 30)
        screen.blit(line, lineRect)
        line = smallFont.render(f"Player 2: {game.p2s}", True, WHITE)
        lineRect = line.get_rect()
        lineRect.center = (width - 68, 30)
        screen.blit(line, lineRect)
        # pygame.draw.rect(screen, (0, 255, 0), (BOARD_PADDING + (cell_size * (game.p1.x)),25 + BOARD_PADDING + (cell_size * (game.p1.y)),cell_size,cell_size))

        
        screen.blit(pygame.transform.scale(load_image("X-wing.png"), 
            (cell_size, int((cell_size/4 )* 3))), (game.p2.x , game.p2.y + (cell_size/4) + 1))
        screen.blit(
            pygame.transform.rotozoom(load_image("tie-fighter.png"), 
                0, 
                cell_size/475), 
            (game.p1.x - 2,
                game.p1.y))
        if show_hb == True:        
            pygame.draw.rect(screen, (255, 0, 0), (game.p1.x, game.p1.y, game.p1.hb, game.p1.hb), width = 1)
            pygame.draw.rect(screen, (255, 0, 0), (game.p2.x, game.p2.y, game.p2.hb, game.p2.hb), width = 1)
        for bullet in game.p1.bullets:
            bullet.update()
            if show_hb == True:
                pygame.draw.rect(screen, (255, 0, 0), (bullet.x, bullet.y, bullet.hx, bullet.hy), width = 1)
            if bullet.b == False:
                pygame.draw.rect(screen, 
                    (0, 255, 0), 
                    (bullet.x + 1,bullet.y, 2,bullet.hy), border_bottom_left_radius=1, border_bottom_right_radius=1)
                pygame.draw.rect(screen, 
                    (0, 255, 0), 
                    (cell_size + 1 + bullet.x  - 4, bullet.y, 2,bullet.hy), border_bottom_left_radius=1, border_bottom_right_radius=1)
            else:
                pygame.draw.rect(screen, 
                    (0, 255, 0), 
                    (bullet.x + 1,bullet.y, 2,(bullet.hy/8)*2), border_bottom_left_radius=1, border_bottom_right_radius=1)
                pygame.draw.rect(screen, 
                    (0, 255, 0), 
                    (cell_size + 1 + bullet.x  - 4, bullet.y, 2,(bullet.hy/8)*2), border_bottom_left_radius=1, border_bottom_right_radius=1)

                pygame.draw.rect(screen, 
                    (0, 255, 0), 
                    (bullet.x + 1,bullet.y + ((bullet.hy/6)*4), 2,(bullet.hy/6)*2), border_bottom_left_radius=1, border_bottom_right_radius=1)
                pygame.draw.rect(screen, 
                    (0, 255, 0), 
                    (cell_size + 1 + bullet.x  - 4, bullet.y + ((bullet.hy/6)*4), 2,(bullet.hy/6)*2), border_bottom_left_radius=1, border_bottom_right_radius=1)

        for bullet in game.p2.bullets:
            # pygame.draw.rect(screen, (255, 0, 0), (BOARD_PADDING + (cell_size * (bullet.x)),25 + BOARD_PADDING, cell_size,(cell_size* (game.dy - 1)) - 1))
            bullet.update()
            if show_hb == True:
                pygame.draw.rect(screen, (255, 0, 0), (bullet.x, bullet.y, bullet.hx, bullet.hy), width = 1)
            if bullet.b == False:
                
                pygame.draw.rect(screen, 
                    (255, 0, 0), 
                    (bullet.x + 1,bullet.y, 2,bullet.hy), border_bottom_left_radius=1, border_bottom_right_radius=1)
                pygame.draw.rect(screen, 
                    (255, 0, 0), 
                    (bullet.x + cell_size - 3,bullet.y, 2,bullet.hy), border_bottom_left_radius=1, border_bottom_right_radius=1)
            else:
                pygame.draw.rect(screen, 
                    (255, 0, 0), 
                    (bullet.x + 1,bullet.y, 2,(bullet.hy/8)*2), border_bottom_left_radius=1, border_bottom_right_radius=1)
                pygame.draw.rect(screen, 
                    (255, 0, 0), 
                    (cell_size + 1 + bullet.x  - 4, bullet.y, 2,(bullet.hy/8)*2), border_bottom_left_radius=1, border_bottom_right_radius=1)

                pygame.draw.rect(screen, 
                    (255, 0, 0), 
                    (bullet.x + 1,bullet.y + ((bullet.hy/6)*4), 2,(bullet.hy/6)*2), border_bottom_left_radius=1, border_bottom_right_radius=1)
                pygame.draw.rect(screen, 
                    (255, 0, 0), 
                    (cell_size + 1 + bullet.x  - 4, bullet.y + ((bullet.hy/6)*4), 2,(bullet.hy/6)*2), border_bottom_left_radius=1, border_bottom_right_radius=1)




        
        pygame.display.flip()
    else:
        screen.fill(BLACK)
        line = largeFont.render(f"Winner is {game.name}!", True, WHITE)
        lineRect = line.get_rect()
        lineRect.center = (width/2, height/2)
        screen.blit(line, lineRect)

        line = mediumFont.render(f"Press enter to play again", True, WHITE)
        lineRect = line.get_rect()
        lineRect.center = (width/2, height/3 *2)
        screen.blit(line, lineRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RETURN] == 1:
            game.new_game()
            game.done = False
        pygame.display.flip()
        
        
    time.sleep(.025)




    

