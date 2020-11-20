import pygame
import sys
import time

from lazerfield import Lazer_field

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
game = Lazer_field(dx=12)


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
game = Lazer_field()
while True:
    if game.done == False:
        screen.fill(BLACK)
        # Check if game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keystate = pygame.key.get_pressed()
        game.p1.move(keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT])
        sh = keystate[pygame.K_UP] or keystate[pygame.K_DOWN]
        game.p1.shoot(sh)
        game.p2.move(keystate[pygame.K_d] - keystate[pygame.K_a])
        sh = keystate[pygame.K_w] or keystate[pygame.K_s]
        game.p2.shoot(sh)
        
        
        # print(game)
        # print(game.collide())
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
        for bullet in game.p1.bullets:
            pygame.draw.rect(screen, (0, 255, 0), (BOARD_PADDING + (cell_size * (bullet.x)),25 + BOARD_PADDING + cell_size + 1, cell_size,(cell_size* (game.dy - 1)) - 1))
        for bullet in game.p2.bullets:
            pygame.draw.rect(screen, (255, 0, 0), (BOARD_PADDING + (cell_size * (bullet.x)),25 + BOARD_PADDING, cell_size,(cell_size* (game.dy - 1)) - 1))
        pygame.draw.rect(screen, (0, 255, 0), (BOARD_PADDING + (cell_size * (game.p1.x)),25 + BOARD_PADDING + (cell_size * (game.p1.y)),cell_size,cell_size))
        pygame.draw.rect(screen, (255, 0, 0), (BOARD_PADDING + (cell_size * game.p2.x),25 + BOARD_PADDING + (cell_size * game.p2.y),cell_size,cell_size))
        
        
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
        
        
    time.sleep(.05)




    


def load_image(file):
    """ loads an image, prepares it for play
    """
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert()