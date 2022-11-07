import pygame
import os
from board import Board, Piece, Pawn, Knight, Bishop, Rook, Queen, King
from board import board_pos_to_coords, coords_to_board_pos

pygame.init()
FPS = 60
BLACK = (0,0,0)
BACKGROUND_COLOR = (49,46,43)

# create window
WIDTH, HEIGHT = 1280, 720
pygame.display.set_caption("Chess")


icon = pygame.image.load(os.path.join("images/PNG/", "icon.png"))
pygame.display.set_icon(icon)

fullscreen = True
flags = pygame.RESIZABLE
if fullscreen:
    flags = pygame.FULLSCREEN
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT),flags)


board = "board2"


def draw() -> None:
    WINDOW.fill(BACKGROUND_COLOR)
    WINDOW.blit(Board.board_image, Board.position_of_board)
    WINDOW.blit(Board.identifiers_image, Board.position_of_identifiers)

    for p in Board.all_pieces:
        WINDOW.blit(p.image, p.coords)

    pygame.display.update()


def load_images() -> None:
    Board.board_image_original_size = pygame.image.load(os.path.join("images/PNG/", f"{board}.png"))
    Board.identifiers_image_original_size = pygame.image.load(os.path.join("images/PNG/", "identifiers.png"))

    for p in Board.all_pieces:
        #print(f"Loading: {p.color}_{p.type.lower()}.png")
        p.image_original_size = pygame.image.load(os.path.join("images/PNG/", f"{p.color}_{p.type.lower()}.png")) 

    transform_images() 


def transform_images() -> None:
    Board.board_image = pygame.transform.smoothscale(Board.board_image_original_size, (Board.size_of_board, Board.size_of_board))
    Board.identifiers_image = pygame.transform.smoothscale(Board.identifiers_image_original_size, (Board.size_of_identifiers, Board.size_of_identifiers))
 
    for p in Board.all_pieces:
        p.image = pygame.transform.smoothscale(p.image_original_size, (p.size, p.size))


def resize_window(board) -> None:
    board.resize_window_reset_pos()

    for p in Board.all_pieces:
        p.resize_window_reset_pos()

    transform_images() 


def main():
    clock = pygame.time.Clock()
    running = True


    
    WIDTH, HEIGHT = pygame.display.get_window_size()
    #print(WIDTH, HEIGHT)
    #print(type(pygame.display.get_window_size()))
    Board.position_of_board = (WIDTH*0.5-(HEIGHT*0.8*0.5), HEIGHT*0.1)
    Board.size_of_board = HEIGHT*0.8

    Board.position_of_identifiers = (WIDTH*0.5-(HEIGHT*0.89*0.5), HEIGHT*0.14)
    Board.size_of_identifiers = HEIGHT*0.81

    board = Board()
    load_images()

    #print(f"\nWhite pieces: {Board.white_pieces}\n")
    #print(f"\nAll pieces: {Board.all_pieces}\n")
    
    #Main game loop
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            #print(event)
            #print(event.type)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.WINDOWRESIZED:
                print("RESIZED")
                resize_window(board)

        draw()
    


if __name__ == "__main__":
    main()
    pygame.quit()