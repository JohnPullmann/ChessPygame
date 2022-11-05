import pygame
import os


pygame.init()
FPS = 60
BLACK = (0,0,0)

# create window
WIDTH, HEIGHT = 1280, 720
pygame.display.set_caption("Chess")


icon = pygame.image.load(os.path.join("images/PNG/", "icon.png"))
pygame.display.set_icon(icon)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


def draw():
    WINDOW.fill(BLACK)
    pygame.display.update()
    

def main():
    clock = pygame.time.Clock()
    running = True
    
    #Main game loop
    while running:
          
        clock.tick(FPS)
        for event in pygame.event.get():
            #print(event)
            #print(event.type)
            if event.type == pygame.QUIT:
                running = False

        draw()
    


if __name__ == "__main__":
    main()
    pygame.quit()