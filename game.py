import pygame
import os
from game_board import Board, Piece, Pawn, Knight, Bishop, Rook, Queen, King, Player
from game_board import board_pos_to_coords, coords_to_board_pos


FPS = 60
BLACK = (0,0,0)
BACKGROUND_COLOR = (49,46,43)

SHOW_POSSIBLE_MOVES = False
BOARD_COLOR = "board2"
WIDTH, HEIGHT = 800, 600
FULLSCREEN = False

pygame.init()

pygame.display.set_caption("Chess")

icon = pygame.image.load(os.path.join("images/PNG/", "icon.png"))
pygame.display.set_icon(icon)

flags = pygame.RESIZABLE
if FULLSCREEN:
    flags = pygame.FULLSCREEN
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT),flags)


def main():
    

    def draw() -> None:
        WINDOW.fill(BACKGROUND_COLOR)
        WINDOW.blit(board.board_image, board.position_of_board)
        WINDOW.blit(board.identifiers_image, board.position_of_identifiers)

        if board.last_turn[0] != () and board.last_turn[1] != ():
            start_turn_board_coords = board_pos_to_coords(board, board.last_turn[0])
            end_turn_board_coords = board_pos_to_coords(board, board.last_turn[1])

            WINDOW.blit(board.selected_square_image, start_turn_board_coords)  
            WINDOW.blit(board.selected_square_image, end_turn_board_coords)         

        if board.selected_piece != None:
            selected_square_board_coords = board_pos_to_coords(board, board.selected_piece.board_pos)
            WINDOW.blit(board.selected_square_image, selected_square_board_coords)  

            for valid_move in board.selected_piece.valid_moves:
                valid_move_coords = board_pos_to_coords(board, (valid_move[0],valid_move[1]))
                if valid_move[2] == True:
                    WINDOW.blit(board.valid_move_attack_image, valid_move_coords)
                else:
                    WINDOW.blit(board.valid_move_image, valid_move_coords)

        if board.holding_piece != None:
            mouse_on_square_board_pos, mouse_on_square_board_coords = board.mouse_on_square
            if mouse_on_square_board_coords != -1:
                WINDOW.blit(board.holding_over_square_image, mouse_on_square_board_coords)


        for p in board.all_pieces:
            #print(p ,p.image, p.coords)
            WINDOW.blit(p.image, p.coords)

        if board.holding_piece != None:
            WINDOW.blit(board.holding_piece.image, board.holding_piece.coords)
        
        if board.choosing_piece != None:
            if board.choosing_piece.color == "white":
                WINDOW.blit(board.choose_piece_white_image, board.choosing_piece.coords)
            else:
                WINDOW.blit(board.choose_piece_black_image, (board.choosing_piece.coords[0], board.choosing_piece.coords[1]-(board.size_of_board/8*3)))

        pygame.display.update()


    def load_images() -> None:
        board.board_image_original_size = pygame.image.load(os.path.join("images/PNG/", f"{BOARD_COLOR}.png"))
        board.identifiers_image_original_size = pygame.image.load(os.path.join("images/PNG/", "identifiers.png"))

        board.selected_square_image_original_size = pygame.image.load(os.path.join("images/PNG/", "selected_square.png")) 
        board.holding_over_square_image_original_size = pygame.image.load(os.path.join("images/PNG/", "holding_over_square.png"))
        board.valid_move_image_original_size = pygame.image.load(os.path.join("images/PNG/", "valid_move.png"))
        board.valid_move_attack_image_original_size = pygame.image.load(os.path.join("images/PNG/", "valid_move_attack.png")) 
        board.choose_piece_white_image_original_size = pygame.image.load(os.path.join("images/PNG/", "choose_piece_white.png")) 
        board.choose_piece_black_image_original_size = pygame.image.load(os.path.join("images/PNG/", "choose_piece_black.png")) 

        transform_images() 


    def transform_images() -> None:
        board.board_image = pygame.transform.smoothscale(board.board_image_original_size, (board.size_of_board, board.size_of_board))
        board.identifiers_image = pygame.transform.smoothscale(board.identifiers_image_original_size, (board.size_of_identifiers, board.size_of_identifiers))
        
        board.selected_square_image = pygame.transform.smoothscale(board.selected_square_image_original_size, (board.size_of_board/8, board.size_of_board/8))
        board.holding_over_square_image = pygame.transform.smoothscale(board.holding_over_square_image_original_size, (board.size_of_board/8, board.size_of_board/8))

        board.valid_move_image = pygame.transform.smoothscale(board.valid_move_image_original_size, (board.size_of_board/8, board.size_of_board/8))
        board.valid_move_attack_image = pygame.transform.smoothscale(board.valid_move_attack_image_original_size, (board.size_of_board/8, board.size_of_board/8))

        board.choose_piece_white_image = pygame.transform.smoothscale(board.choose_piece_white_image_original_size, (board.size_of_board/8, board.size_of_board/8*5))
        board.choose_piece_black_image = pygame.transform.smoothscale(board.choose_piece_black_image_original_size, (board.size_of_board/8, board.size_of_board/8*5
        ))

        for piece in board.all_pieces:
            piece.transform_image()



    def resize_window() -> None:
        board.resize_window_reset_pos()

        for p in board.all_pieces:
            p.resize_window_reset_pos()

        transform_images() 


    def holding_piece_move(mouse_x: float, mouse_y: float) -> None:
        if board.holding_piece != None:
            x = mouse_x
            y = mouse_y
            x = x if x > board.position_of_board[0] else board.position_of_board[0]
            x = x if x < board.position_of_board[0]+board.size_of_board else board.position_of_board[0]+board.size_of_board
            y = y if y > board.position_of_board[1] else board.position_of_board[1]
            y = y if y < board.position_of_board[1]+board.size_of_board else board.position_of_board[1]+board.size_of_board
            holding_piece_size = board.holding_piece.size
            x -= holding_piece_size/2
            y -= holding_piece_size/2

            board.holding_piece.coords = (x, y)    


    def selected_piece_drop(mouse_x: float, mouse_y: float) -> None:
        if board.selected_piece != None:
            new_board_pos = coords_to_board_pos(board, (mouse_x, mouse_y))
            if new_board_pos != -1:
                new_piece_pos = board_pos_to_coords(board, new_board_pos)
                
                if board.selected_piece.move(new_board_pos):
                    pass
                else:
                    # return to old position
                    board.selected_piece.coords = board_pos_to_coords(board, board.selected_piece.board_pos)
                    board.holding_piece = None
            else:
                # return to old position
                board.selected_piece.coords = board_pos_to_coords(board, board.selected_piece.board_pos)
                board.holding_piece = None

    def choose_piece(mouse_x: float, mouse_y: float) -> None:

        if board.choosing_piece.color == "white":
            x, y = (mouse_x-board.choosing_piece.coords[0], mouse_y-(board.choosing_piece.coords[1]))
        else:
            x, y = (mouse_x-board.choosing_piece.coords[0], mouse_y-(board.choosing_piece.coords[1]-(board.size_of_board/8*3)))
            
        if (0 < x < board.size_of_board/8) and (0 < y < board.size_of_board/8*4):
            piece = y // (board.size_of_board/8)
            if piece == 0:
                board.choosing_piece.promote("Queen")
            elif piece == 1:
                board.choosing_piece.promote("Rook")
            elif piece == 2:
                board.choosing_piece.promote("Knight")
            elif piece == 3:
                board.choosing_piece.promote("Bishop")

            board.choosing_piece = None


    def mouse_on_square_select(mouse_x: float, mouse_y: float) -> None:
        new_board_pos = coords_to_board_pos(board, (mouse_x, mouse_y))
        if new_board_pos != -1:
            new_board_coords = board_pos_to_coords(board, new_board_pos)
            board.mouse_on_square = [new_board_pos, new_board_coords]
        else:
            board.mouse_on_square = [-1, -1]



    clock = pygame.time.Clock()
    running = True
    
    WIDTH, HEIGHT = pygame.display.get_window_size()
    #print(WIDTH, HEIGHT)
    #print(type(pygame.display.get_window_size()))
    board = Board(WIDTH, HEIGHT)

    board.position_of_board = (WIDTH*0.5-(HEIGHT*0.8*0.5), HEIGHT*0.1)
    board.size_of_board = HEIGHT*0.8

    board.position_of_identifiers = (WIDTH*0.5-(HEIGHT*0.89*0.5), HEIGHT*0.14)
    board.size_of_identifiers = HEIGHT*0.81

    
    board.validate_all_pieces()
    load_images()

    #print(f"\nWhite pieces: {Board.white_pieces}\n")
    #print(f"\nAll pieces: {Board.all_pieces}\n")
    
    #Main game loop
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.WINDOWRESIZED:
                resize_window()

            if not board.ended:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if board.choosing_piece == None:
                        board.select_piece(mouse_x, mouse_y)


                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if board.choosing_piece == None:
                        selected_piece_drop(mouse_x, mouse_y)
                    else:
                        choose_piece(mouse_x, mouse_y)


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
# - chessmate - ending of game
# - draw - ending of game
# - surrender - ending of game
# - reseting of game
# - chosing name and color
# - improve quality of code 
# - showing who is on turn
# - arrows for planning turns
# - Castling only if none of squares between king and rook are endangered
# - show destroyed pieces
# - show relative value of pieces
# - add draw Dead Position
# - add draw and resign by agreement
# - add draw Threefold Repetition
# - add 50-Move Rule

# - cant defend check by pieces error
# - Delete class objects after removing them
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

