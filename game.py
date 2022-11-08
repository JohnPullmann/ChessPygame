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

fullscreen = False
flags = pygame.RESIZABLE
if fullscreen:
    flags = pygame.FULLSCREEN
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT),flags)


board_color = "board2"


def draw() -> None:
    WINDOW.fill(BACKGROUND_COLOR)
    WINDOW.blit(Board.board_image, Board.position_of_board)
    WINDOW.blit(Board.identifiers_image, Board.position_of_identifiers)

    if Board.selected_piece != None:
        mouse_on_square_board_pos, mouse_on_square_board_coords = Board.mouse_on_square
        if mouse_on_square_board_pos != -1 and mouse_on_square_board_coords != -1:
            WINDOW.blit(Board.selected_square_image, mouse_on_square_board_coords)

    for p in Board.all_pieces:
        WINDOW.blit(p.image, p.coords)
    if Board.selected_piece != None:
        WINDOW.blit(Board.selected_piece.image, Board.selected_piece.coords)
    
    
    
    pygame.display.update()


def load_images() -> None:
    Board.board_image_original_size = pygame.image.load(os.path.join("images/PNG/", f"{board_color}.png"))
    Board.identifiers_image_original_size = pygame.image.load(os.path.join("images/PNG/", "identifiers.png"))

    Board.selected_square_image_original_size = pygame.image.load(os.path.join("images/PNG/", "selected_square.png"))

    for p in Board.all_pieces:
        #print(f"Loading: {p.color}_{p.type.lower()}.png")
        p.image_original_size = pygame.image.load(os.path.join("images/PNG/", f"{p.color}_{p.type.lower()}.png")) 

    transform_images() 


def transform_images() -> None:
    Board.board_image = pygame.transform.smoothscale(Board.board_image_original_size, (Board.size_of_board, Board.size_of_board))
    Board.identifiers_image = pygame.transform.smoothscale(Board.identifiers_image_original_size, (Board.size_of_identifiers, Board.size_of_identifiers))
 
    Board.selected_square_image = pygame.transform.smoothscale(Board.selected_square_image_original_size, (Board.size_of_board/8, Board.size_of_board/8))

    for p in Board.all_pieces:
        p.image = pygame.transform.smoothscale(p.image_original_size, (p.size, p.size))


def resize_window(board) -> None:
    board.resize_window_reset_pos()

    for p in Board.all_pieces:
        p.resize_window_reset_pos()

    transform_images() 


def select_piece(mouse_x: float, mouse_y: float, board: Board) -> None:

    mouse_board_pos = coords_to_board_pos((mouse_x, mouse_y))
    if mouse_board_pos != -1:
        selected_piece = board.board[mouse_board_pos[0]][mouse_board_pos[1]]
        print(selected_piece)
    else:
        selected_piece = None
    
    if selected_piece != None:
        selected_piece.selected = True
        Board.selected_piece = selected_piece
        #print(f"Coords: {(mouse_x, mouse_y)}\nBoard position: {mouse_board_pos}\nSelected piece: {selected_piece}")


def selected_piece_move_floating(mouse_x: float, mouse_y: float) -> None:
    if Board.selected_piece != None:
        x = mouse_x
        y = mouse_y
        x = x if x > Board.position_of_board[0] else Board.position_of_board[0]
        x = x if x < Board.position_of_board[0]+Board.size_of_board else Board.position_of_board[0]+Board.size_of_board
        y = y if y > Board.position_of_board[1] else Board.position_of_board[1]
        y = y if y < Board.position_of_board[1]+Board.size_of_board else Board.position_of_board[1]+Board.size_of_board
        
        sel_piece_size = Board.selected_piece.size
        Board.selected_piece.coords = (x-(sel_piece_size/2), y-(sel_piece_size/2))    


def selected_piece_drop(mouse_x: float, mouse_y: float, board: Board) -> None:
    if Board.selected_piece != None:
        sel_piece_board_pos = coords_to_board_pos((mouse_x, mouse_y))
        if sel_piece_board_pos != -1:
            sel_piece_pos = board_pos_to_coords(sel_piece_board_pos)
            
            if Board.selected_piece.move():
                print(f"Piece drop position: {sel_piece_board_pos}")
                board.board[Board.selected_piece.board_pos[0]][Board.selected_piece.board_pos[1]] = None
                board.board[sel_piece_board_pos[0]][sel_piece_board_pos[1]] = Board.selected_piece

                

                Board.selected_piece.coords = sel_piece_pos
                Board.selected_piece.board_pos = sel_piece_board_pos
                Board.selected_piece = None
            else:
                print(f"Piece drop to its old position")
                Board.selected_piece.coords = board_pos_to_coords(Board.selected_piece.board_pos)
                Board.selected_piece = None
        else:
            print(f"Piece drop to its old position")
            Board.selected_piece.coords = board_pos_to_coords(Board.selected_piece.board_pos)
            Board.selected_piece = None

def select_square(mouse_x: float, mouse_y: float) -> None:
    sel_board_pos = coords_to_board_pos((mouse_x, mouse_y))
    if sel_board_pos != -1:
        sel_board_coords = board_pos_to_coords(sel_board_pos)
        Board.mouse_on_square = [sel_board_pos, sel_board_coords]
    else:
        Board.mouse_on_square = [-1, -1]



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


            if event.type == pygame.MOUSEBUTTONDOWN:
                print("\nMouse down")
                mouse_x, mouse_y = pygame.mouse.get_pos()

                select_piece(mouse_x, mouse_y, board) 


            if event.type == pygame.MOUSEBUTTONUP:
                print("\nMouse up")
                mouse_x, mouse_y = pygame.mouse.get_pos()
            
                selected_piece_drop(mouse_x, mouse_y, board)
                
            
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                select_square(mouse_x, mouse_y)
                selected_piece_move_floating(mouse_x, mouse_y)

        draw()
    


if __name__ == "__main__":
    main()
    pygame.quit()