import pygame
import os
from board import Board, Piece, Pawn, Knight, Bishop, Rook, Queen, King, Player
from board import board_pos_to_coords, coords_to_board_pos

pygame.init()
FPS = 60
BLACK = (0,0,0)
BACKGROUND_COLOR = (49,46,43)

SHOW_POSSIBLE_MOVES = False

# create window
WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("Chess")


icon = pygame.image.load(os.path.join("images/PNG/", "icon.png"))
pygame.display.set_icon(icon)

FULLSCREEN = False
flags = pygame.RESIZABLE
if FULLSCREEN:
    flags = pygame.FULLSCREEN
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT),flags)


board_color = "board2"

def draw() -> None:
    WINDOW.fill(BACKGROUND_COLOR)
    WINDOW.blit(Board.board_image, Board.position_of_board)
    WINDOW.blit(Board.identifiers_image, Board.position_of_identifiers)

    if Board.last_turn[0] != () and Board.last_turn[1] != ():
        start_turn_board_coords = board_pos_to_coords(Board.last_turn[0])
        end_turn_board_coords = board_pos_to_coords(Board.last_turn[1])

        WINDOW.blit(Board.selected_square_image, start_turn_board_coords)  
        WINDOW.blit(Board.selected_square_image, end_turn_board_coords)         

    if Board.selected_piece != None:
        selected_square_board_coords = board_pos_to_coords(Board.selected_piece.board_pos)
        WINDOW.blit(Board.selected_square_image, selected_square_board_coords)  

        for valid_move in Board.selected_piece.valid_moves:
            valid_move_coords = board_pos_to_coords((valid_move[0],valid_move[1]))
            if valid_move[2] == True:
                WINDOW.blit(Board.valid_move_attack_image, valid_move_coords)
            else:
                WINDOW.blit(Board.valid_move_image, valid_move_coords)

    if Board.holding_piece != None:
        mouse_on_square_board_pos, mouse_on_square_board_coords = Board.mouse_on_square
        if mouse_on_square_board_coords != -1:
            WINDOW.blit(Board.holding_over_square_image, mouse_on_square_board_coords)

    for p in Board.all_pieces:
        WINDOW.blit(p.image, p.coords)
    if Board.holding_piece != None:
        WINDOW.blit(Board.holding_piece.image, Board.holding_piece.coords)
    
    if Board.choosing_piece != None:
        if Board.choosing_piece.color == "white":
            WINDOW.blit(Board.choose_piece_white_image, Board.choosing_piece.coords)
        else:
            WINDOW.blit(Board.choose_piece_black_image, (Board.choosing_piece.coords[0], Board.choosing_piece.coords[1]-(Board.size_of_board/8*3)))

    pygame.display.update()


def load_images() -> None:
    Board.board_image_original_size = pygame.image.load(os.path.join("images/PNG/", f"{board_color}.png"))
    Board.identifiers_image_original_size = pygame.image.load(os.path.join("images/PNG/", "identifiers.png"))

    Board.selected_square_image_original_size = pygame.image.load(os.path.join("images/PNG/", "selected_square.png")) 
    Board.holding_over_square_image_original_size = pygame.image.load(os.path.join("images/PNG/", "holding_over_square.png"))
    Board.valid_move_image_original_size = pygame.image.load(os.path.join("images/PNG/", "valid_move.png"))
    Board.valid_move_attack_image_original_size = pygame.image.load(os.path.join("images/PNG/", "valid_move_attack.png")) 
    Board.choose_piece_white_image_original_size = pygame.image.load(os.path.join("images/PNG/", "choose_piece_white.png")) 
    Board.choose_piece_black_image_original_size = pygame.image.load(os.path.join("images/PNG/", "choose_piece_black.png")) 

    transform_images() 


def transform_images() -> None:
    Board.board_image = pygame.transform.smoothscale(Board.board_image_original_size, (Board.size_of_board, Board.size_of_board))
    Board.identifiers_image = pygame.transform.smoothscale(Board.identifiers_image_original_size, (Board.size_of_identifiers, Board.size_of_identifiers))
    
    Board.selected_square_image = pygame.transform.smoothscale(Board.selected_square_image_original_size, (Board.size_of_board/8, Board.size_of_board/8))
    Board.holding_over_square_image = pygame.transform.smoothscale(Board.holding_over_square_image_original_size, (Board.size_of_board/8, Board.size_of_board/8))

    Board.valid_move_image = pygame.transform.smoothscale(Board.valid_move_image_original_size, (Board.size_of_board/8, Board.size_of_board/8))
    Board.valid_move_attack_image = pygame.transform.smoothscale(Board.valid_move_attack_image_original_size, (Board.size_of_board/8, Board.size_of_board/8))

    Board.choose_piece_white_image = pygame.transform.smoothscale(Board.choose_piece_white_image_original_size, (Board.size_of_board/8, Board.size_of_board/8*5))
    Board.choose_piece_black_image = pygame.transform.smoothscale(Board.choose_piece_black_image_original_size, (Board.size_of_board/8, Board.size_of_board/8*5
    ))

    for piece in Board.all_pieces:
        piece.transform_image()



def resize_window(board) -> None:
    board.resize_window_reset_pos()

    for p in Board.all_pieces:
        p.resize_window_reset_pos()

    transform_images() 


def holding_piece_move(mouse_x: float, mouse_y: float) -> None:
    if Board.holding_piece != None:
        x = mouse_x
        y = mouse_y
        x = x if x > Board.position_of_board[0] else Board.position_of_board[0]
        x = x if x < Board.position_of_board[0]+Board.size_of_board else Board.position_of_board[0]+Board.size_of_board
        y = y if y > Board.position_of_board[1] else Board.position_of_board[1]
        y = y if y < Board.position_of_board[1]+Board.size_of_board else Board.position_of_board[1]+Board.size_of_board
        holding_piece_size = Board.holding_piece.size
        x -= holding_piece_size/2
        y -= holding_piece_size/2

        Board.holding_piece.coords = (x, y)    


def selected_piece_drop(mouse_x: float, mouse_y: float, board: Board) -> None:
    if Board.selected_piece != None:
        new_board_pos = coords_to_board_pos((mouse_x, mouse_y))
        if new_board_pos != -1:
            new_piece_pos = board_pos_to_coords(new_board_pos)
            
            if Board.selected_piece.move(new_board_pos, board):
                pass
            else:
                Board.selected_piece.coords = board_pos_to_coords(Board.selected_piece.board_pos)
                Board.holding_piece = None
        else:
            Board.selected_piece.coords = board_pos_to_coords(Board.selected_piece.board_pos)
            Board.holding_piece = None

def choose_piece(mouse_x: float, mouse_y: float, board: Board) -> None:

    if Board.choosing_piece.color == "white":
        x, y = (mouse_x-Board.choosing_piece.coords[0], mouse_y-(Board.choosing_piece.coords[1]))
    else:
        x, y = (mouse_x-Board.choosing_piece.coords[0], mouse_y-(Board.choosing_piece.coords[1]-(Board.size_of_board/8*3)))
        
    if (0 < x < Board.size_of_board/8) and (0 < y < Board.size_of_board/8*4):
        piece = y // (Board.size_of_board/8)
        if piece == 0:
            Board.choosing_piece.promote("Queen", board)
        elif piece == 1:
            Board.choosing_piece.promote("Rook", board)
        elif piece == 2:
            Board.choosing_piece.promote("Knight", board)
        elif piece == 3:
            Board.choosing_piece.promote("Bishop", board)

        Board.choosing_piece = None


def mouse_on_square_select(mouse_x: float, mouse_y: float) -> None:
    new_board_pos = coords_to_board_pos((mouse_x, mouse_y))
    if new_board_pos != -1:
        new_board_coords = board_pos_to_coords(new_board_pos)
        Board.mouse_on_square = [new_board_pos, new_board_coords]
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
    Board.validate_all_pieces(board)
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
                #print("RESIZED")

                resize_window(board)


            if event.type == pygame.MOUSEBUTTONDOWN:
                #print("\nMouse down")
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if board.choosing_piece == None:
                    board.select_piece(mouse_x, mouse_y)
                    #select_piece(mouse_x, mouse_y, board) 


            if event.type == pygame.MOUSEBUTTONUP:
                #print("\nMouse up")
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if board.choosing_piece == None:
                    selected_piece_drop(mouse_x, mouse_y, board)
                else:
                    choose_piece(mouse_x, mouse_y, board)

                
            
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if board.choosing_piece == None:
                    mouse_on_square_select(mouse_x, mouse_y)
                    holding_piece_move(mouse_x, mouse_y)

        draw()
    


if __name__ == "__main__":
    main()
    pygame.quit()


##TODO##
# Implement:
# - change piece type when pawn moves to end of board #219
# - piece cant make move that will endanger king
# - chessmate - ending of game
# - draw - ending of game
# - surrender - ending of game
# - reseting of game
# - chosing name and color
# - improve quality of code 
# - showing who is on turn
# - arrows for planning turns

# - Delete class objects after removing them
# - sometimes pawns cant be touched
# - error maximum recursion p_attacking king validate moves -> add if saves king -> p_attacking king validate moves 

# player vs player
# - on one device
# -- switching showing of board 
# - localy on two devices
# -- surrender when someone quits

#/ player vs computer

# sandbox mode

# Menu
# - local play PvP
# - fullscreen and scale window switching 
# - changing styles

# implement info around board 
# - name, entering a name
#/ - score

# On website watching matches

# moving board.py to some dictionary 

# improving readme

