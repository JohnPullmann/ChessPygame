import pygame
from pprint import pprint
import os


def board_pos_to_coords(board_pos) -> tuple:
        return (Board.position_of_board[0]+Board.size_of_board/8*board_pos[1], Board.position_of_board[1]+Board.size_of_board/8*board_pos[0])


def coords_to_board_pos(coords) -> tuple:
        row = (coords[0]-Board.position_of_board[0])//(Board.size_of_board/8)
        col = (coords[1]-Board.position_of_board[1])//(Board.size_of_board/8)

        if 8 > col >= 0 and 8 > row >= 0:
            return (int(col), int(row))
        else:
            return -1 



class Board():

    white_pieces = []
    black_pieces = []
    all_pieces =[]
    holding_piece = None
    selected_piece = None
    white_king = None
    black_king = None

    player1 = None
    player2 = None
    player_on_turn = None

    position_of_board: tuple = (0, 0)
    size_of_board: int = 0
    board_image = None # image loaded 
    board_image_original_size = None # image loaded later

    position_of_identifiers: tuple = (0, 0)
    size_of_identifiers: int = 0
    identifiers_image = None # image loaded 
    identifiers_image_original_size = None # image loaded later

    selected_square_image = None  # image loaded later
    selected_square_image_original_size = None  # image loaded later
    holding_over_square_image = None  # image loaded later
    holding_over_square_image_original_size = None  # image loaded later
    valid_move_image = None  # image loaded later
    valid_move_image_original_size = None  # image loaded later
    valid_move_attack_image = None  # image loaded later
    valid_move_attack_image_original_size = None  # image loaded later
    choose_piece_white_image_original_size = None  # image loaded later
    choose_piece_black_image_original_size = None  # image loaded later
    choose_piece_white_image = None  # image loaded later
    choose_piece_black_image = None  # image loaded later
    mouse_on_square = [(),()] # [board_pos, board_pos_coords]

    last_turn = [(),()] # [start_board_pos, end_board_pos]
    danger_zone_black = [[False for _ in range(8)] for _ in range(8)]
    danger_zone_white = [[False for _ in range(8)] for _ in range(8)]

    choosing_piece = None

    def __init__(self):

        self.rec = pygame.Rect(*Board.position_of_board, Board.size_of_board, Board.size_of_board)

        self.board = [[None for _ in range(8)] for _ in range(8)]
        #print(f"Board: {self.board}")

        self.board[6][0] = Pawn("white", (6, 0))
        self.board[6][1] = Pawn("white", (6, 1))
        self.board[6][2] = Pawn("white", (6, 2))
        self.board[6][3] = Pawn("white", (6, 3))
        self.board[6][4] = Pawn("white", (6, 4))
        self.board[6][5] = Pawn("white", (6, 5))
        self.board[6][6] = Pawn("white", (6, 6))
        self.board[6][7] = Pawn("white", (6, 7))

        self.board[7][0] = Rook("white", (7, 0))
        self.board[7][1] = Knight("white", (7, 1))
        self.board[7][2] = Bishop("white", (7, 2))
        self.board[7][3] = Queen("white", (7, 3))
        self.board[7][4] = King("white", (7, 4))
        self.board[7][5] = Bishop("white", (7, 5))
        self.board[7][6] = Knight("white", (7, 6))
        self.board[7][7] = Rook("white", (7, 7))


        self.board[0][0] = Rook("black", (0, 0))
        self.board[0][1] = Knight("black", (0, 1))
        self.board[0][2] = Bishop("black", (0, 2))
        self.board[0][3] = Queen("black", (0, 3))
        self.board[0][4] = King("black", (0, 4))
        self.board[0][5] = Bishop("black", (0, 5))
        self.board[0][6] = Knight("black", (0, 6))
        self.board[0][7] = Rook("black", (0, 7))

        self.board[1][0] = Pawn("black", (1, 0))
        self.board[1][1] = Pawn("black", (1, 1))
        self.board[1][2] = Pawn("black", (1, 2))
        self.board[1][3] = Pawn("black", (1, 3))
        self.board[1][4] = Pawn("black", (1, 4))
        self.board[1][5] = Pawn("black", (1, 5))
        self.board[1][6] = Pawn("black", (1, 6))
        self.board[1][7] = Pawn("black", (1, 7))

        #print(f"Board: {self.board}")

        Board.player1 = Player("Player1", "white", "Player") # player options can be changed later
        Board.player2 = Player("Player2", "black", "Player") # player options can be changed later 
        if Board.player1.color == "white":
            Board.player_on_turn = Board.player1
        elif Board.player2.color == "white":
            Board.player_on_turn = Board.player2
        else:
            print("Problem! Neither player is white!")    


    def resize_window_reset_pos(self):
        WIDTH, HEIGHT = pygame.display.get_window_size()
        Board.position_of_board = (WIDTH*0.5-(HEIGHT*0.8*0.5), HEIGHT*0.1)
        Board.size_of_board = HEIGHT*0.8
        Board.position_of_identifiers = (WIDTH*0.5-(HEIGHT*0.89*0.5), HEIGHT*0.14)
        Board.size_of_identifiers = HEIGHT*0.81
        #print(WIDTH, HEIGHT)
        #print(type(pygame.display.get_window_size()))

        self.rec.update(*Board.position_of_board, Board.size_of_board, Board.size_of_board)

    def select_piece(self, mouse_x: float, mouse_y: float) -> None:
        mouse_board_pos = coords_to_board_pos((mouse_x, mouse_y))
        if mouse_board_pos != -1:
            if self.board[mouse_board_pos[0]][mouse_board_pos[1]] != None:
                #print(selected_piece, self.player_on_turn)
                if self.board[mouse_board_pos[0]][mouse_board_pos[1]].color == self.player_on_turn.color:
                    self.board[mouse_board_pos[0]][mouse_board_pos[1]].selected = True
                    Board.holding_piece = self.board[mouse_board_pos[0]][mouse_board_pos[1]]
                    Board.selected_piece = self.board[mouse_board_pos[0]][mouse_board_pos[1]]

                    #print(f"Valid moves {selected_piece.type}: {selected_piece.valid_moves}")
                else:
                    #print("ccccc",selected_piece.color == self.player_on_turn.color, selected_piece.color, self.player_on_turn.color, selected_piece)
                    #Board.selected_piece = None
                    Board.holding_piece = None
        else:
            Board.selected_piece = None
            Board.holding_piece = None

    def validate_all_pieces(self) -> None:
        Board.danger_zone_black = [[False for _ in range(8)] for _ in range(8)]
        Board.danger_zone_white = [[False for _ in range(8)] for _ in range(8)]

        for piece in Board.all_pieces:
            piece.validate_moves(self)
        
        Board.white_king.validate_moves(self)
        Board.black_king.validate_moves(self)

        for piece in Board.all_pieces:
            piece.validate_moves(self)

        # print("White danger zone: ")
        # pprint(Board.danger_zone_white)
        # print("Black danger zone: ")
        # pprint(Board.danger_zone_black)


class Piece():
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        self.color = color # "white" or "black"
        self.board_pos = board_pos # (column, row)
        self.coords = board_pos_to_coords(self.board_pos) # (x, y)
        self.size = Board.size_of_board/8
        self.selected = selected
        self.rec = pygame.Rect(*self.coords, self.size, self.size)
        self.type = None
        self.valid_moves = [] # updates when spiece selected, [(col, row, attact)]
        self.image = None # image loaded later
        self.image_original_size = None # image loaded later

        if self.color == "white":
            Board.white_pieces.append(self)
        elif self.color == "black":
            Board.black_pieces.append(self)
        Board.all_pieces.append(self)

    def load_image(self):
        self.image_original_size = pygame.image.load(os.path.join("images/PNG/", f"{self.color}_{self.type.lower()}.png")) 
        self.image = pygame.transform.smoothscale(self.image_original_size, (self.size, self.size))

    def isSelected(self) -> bool:
        return self.selected

    def resize_window_reset_pos(self):
        self.coords = board_pos_to_coords(self.board_pos) # (x, y)
        self.size = Board.size_of_board/8
        self.rec.update(*self.coords, self.size, self.size)
    
    def move(self, dest_board_pos, game_board: Board) -> bool:
        color_col_mult = 1
        if self.color == "white":
            color_col_mult = -1

        if Board.player_on_turn.color != self.color:
            print(f"You tried to move piece of different color, \nYour color: {Board.player_on_turn.color}, Piece color: {self.color}")
            return False

        attacking = False
        if (dest_board_pos[0], dest_board_pos[1], False) not in self.valid_moves:
            if (dest_board_pos[0], dest_board_pos[1], True) not in self.valid_moves:
                print(f"Not valid move!\nFROM: {self.board_pos}  TO: {dest_board_pos}\nValid moves: {self.valid_moves}")
                return False
            else:
                attacking = True
                

        # ---------------------- Special moves
        if self.type == "Pawn" and attacking == False: # en passant move, left and right
            if dest_board_pos[1] != self.board_pos[1]: #  - test if not normal forward move
                self.attack((dest_board_pos[0]-color_col_mult, dest_board_pos[1]), game_board) 
                attacking = False
            
        other_side = 0 if self.color == "white" else 7
        if self.type == "Pawn" and dest_board_pos[0] == other_side:
            #change pawn to piece of choice
            Board.choosing_piece = self

        elif self.type == "King":
            self.endangered = False
            self.enemy_piece_attacking = None
            if dest_board_pos[1] - self.board_pos[1] == -2: # castling left
                print(f"MOVEMENT, {Board.player_on_turn.name}\nCastling left")
                rook = game_board.board[self.board_pos[0]][self.board_pos[1]-4]
                rook.moved = True
                game_board.board[self.board_pos[0]][self.board_pos[1]-4] = None
                game_board.board[self.board_pos[0]][self.board_pos[1]-1] = rook
                rook.coords = board_pos_to_coords((self.board_pos[0], self.board_pos[1]-1))
                rook.board_pos = (self.board_pos[0], self.board_pos[1]-1)
                #move rook one to right +, of dest
            if dest_board_pos[1] - self.board_pos[1] == 2: # castling right
                print(f"MOVEMENT, {Board.player_on_turn.name}\nCastling right")
                rook = game_board.board[self.board_pos[0]][self.board_pos[1]+3]
                rook.moved = True
                game_board.board[self.board_pos[0]][self.board_pos[1]+3] = None
                game_board.board[self.board_pos[0]][self.board_pos[1]+1] = rook
                rook.coords = board_pos_to_coords((self.board_pos[0], self.board_pos[1]+1))
                rook.board_pos = (self.board_pos[0], self.board_pos[1]+1)

                #move rook one to left -, of dest
        if attacking == True:
            self.attack(dest_board_pos, game_board)
        # ----------------------

        print(f"MOVEMENT, {Board.player_on_turn.name}\nFROM: {self.board_pos}  TO: {dest_board_pos}")
        Board.last_turn = [self.board_pos, dest_board_pos]
        if self.type in ["King","Rook", "Pawn"]:
            self.moved = True


        # Switch player on turn
        if Board.player_on_turn == Board.player1:
            Board.player_on_turn = Board.player2
        elif Board.player_on_turn == Board.player2:
            Board.player_on_turn = Board.player1
        else:
            print("Problem!!!, Program didn't switch players!")
        print(f"Switched players, player on move: {Board.player_on_turn.name}\n")


        game_board.board[Board.selected_piece.board_pos[0]][Board.selected_piece.board_pos[1]] = None
        game_board.board[dest_board_pos[0]][dest_board_pos[1]] = Board.selected_piece

        Board.selected_piece.coords = board_pos_to_coords(dest_board_pos)
        Board.selected_piece.board_pos = dest_board_pos
        Board.holding_piece = None
        Board.selected_piece = None

        Board.validate_all_pieces(game_board)

        return True

    def attack(self, dest_board_pos, game_board: Board) -> bool:
        des_col, des_row = dest_board_pos 
        attacked_piece = game_board.board[des_col][des_row]
        game_board.board[des_col][des_row] = None
        Board.all_pieces.remove(attacked_piece)
        if attacked_piece.color == "white":
            Board.white_pieces.remove(attacked_piece)
        else:
            Board.black_pieces.remove(attacked_piece)
        print(f"{self} attacked {attacked_piece}")

    def add_if_saves_king(self, des_col, des_row, p_attacking_king, your_king, attack, game_board) -> bool:
        game_board.board[des_col][des_row] = self
        p_attacking_king.validate_moves(game_board)

        if (your_king.board_pos[0], your_king.board_pos[1], True) not in p_attacking_king.valid_moves:
            self.valid_moves.append((des_col, des_row, attack))
            game_board.board[des_col][des_row] = None
            p_attacking_king.validate_moves(game_board)
            return True
        game_board.board[des_col][des_row] = None
        p_attacking_king.validate_moves(game_board)
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.color}, {self.board_pos})"


class Pawn(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Pawn"
        self.moved = False
        self.load_image()

    def promote(self, piece, game_board):
        if piece == "Queen":
            game_board.board[self.board_pos[0]][self.board_pos[1]] = Queen(self.color, self.board_pos)
            print(f"\n{Board.player_on_turn.name} chose Queen\n")
        if piece == "Rook":
            game_board.board[self.board_pos[0]][self.board_pos[1]] = Rook(self.color, self.board_pos)
            print(f"\n{Board.player_on_turn.name} chose Rook\n")
        if piece == "Knight":
            game_board.board[self.board_pos[0]][self.board_pos[1]] = Knight(self.color, self.board_pos)
            print(f"\n{Board.player_on_turn.name} chose Knight\n")
        if piece == "Bishop":
            game_board.board[self.board_pos[0]][self.board_pos[1]] = Bishop(self.color, self.board_pos)
            print(f"\n{Board.player_on_turn.name} chose Bishop\n")

        game_board.all_pieces.remove(self)
        if self.color == "white":
            game_board.white_pieces.remove(self)
        else:
            game_board.black_pieces.remove(self)

    def validate_moves(self, game_board) -> None:
        # add special move !
        board = game_board.board
        now_col, now_row = self.board_pos
        color_col_mult = 1
        self.valid_moves = []
        your_king = Board.black_king
        if self.color == "white":
            color_col_mult = -1     
            your_king = Board.white_king
        p_attacking_king = your_king.enemy_piece_attacking
           


        if  0 <= now_col+(1*color_col_mult) < 8: # one forward
            if board[now_col+(1*color_col_mult)][now_row] == None:   
                if your_king.endangered == False:
                    self.valid_moves.append((now_col+(1*color_col_mult), now_row, False))
                else:
                    self.add_if_saves_king(now_col+(1*color_col_mult), now_row, p_attacking_king, your_king, False, game_board)

        if 0 <= now_col+(2*color_col_mult) < 8: # first move two forward
            if board[now_col+(2*color_col_mult)][now_row] == None and board[now_col+(1*color_col_mult)][now_row] == None: 
                if self.moved == False:
                    if your_king.endangered == False:
                        self.valid_moves.append((now_col+(2*color_col_mult), now_row, False))
                    else:
                        self.add_if_saves_king(now_col+(2*color_col_mult), now_row, p_attacking_king, your_king, False, game_board)

        for direction in [1,-1]: # en passant move, left and right
            if 0 <= now_col+(1*color_col_mult) < 8 and 0 <= now_row+(direction) < 8 : 
                attacked_pawn = board[now_col][now_row+(direction)]
                if board[now_col+(1*color_col_mult)][now_row+(direction)] == None and isinstance(attacked_pawn, Pawn):
                    if Board.last_turn[0] == (now_col+(2*color_col_mult), now_row+(direction)) and Board.last_turn[1] == (now_col, now_row+(direction)):
                        self.valid_moves.append((now_col+(1*color_col_mult), now_row+(direction), False))

        for move_row_mod, move_col_mod in [(1,1), (-1,1)]: # one up diagonal, one left diagonal
            des_col = now_col+(move_col_mod*color_col_mult)
            des_row = now_row+move_row_mod
            if 0 <= des_col < 8 and 0 <= des_row < 8: 
                if self.color == "white":
                    Board.danger_zone_black[des_col][des_row] = True
                else:
                    Board.danger_zone_white[des_col][des_row] = True

                des_piece = board[des_col][des_row]
                if des_piece != None:
                    if des_piece.color == self.color:
                        continue
                    else:
                        attack = True
                        if isinstance(des_piece, King):
                            des_piece.endangered = True
                            des_piece.enemy_piece_attacking = self
                        if your_king.endangered == True:
                            if des_col == p_attacking_king.board_pos[0] and des_row == p_attacking_king.board_pos[1]:
                                self.valid_moves.append((des_col, des_row, attack))
                                continue
                else:
                    attack = False

                if attack == True:
                    if your_king.endangered == False:
                        self.valid_moves.append((des_col, des_row, attack))
                    else:
                        self.add_if_saves_king(des_col, des_row, p_attacking_king, your_king, attack, game_board)

    #def move(self) -> bool:
    #    return True


class Knight(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Knight"
        self.moves = [(1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1), (-2,1), (-1,2)]
        self.load_image()

    def validate_moves(self, game_board) -> None:
        board = game_board.board
        now_col, now_row = self.board_pos
        color_col_mult = 1
        self.valid_moves = []
        your_king = Board.black_king
        if self.color == "white":
            color_col_mult = -1     
            your_king = Board.white_king
        p_attacking_king = your_king.enemy_piece_attacking


        for move_row_mod, move_col_mod in self.moves: 
            des_col = now_col+(move_col_mod*color_col_mult)
            des_row = now_row+move_row_mod
            if 0 <= des_col < 8 and 0 <= des_row < 8: 
                
                if self.color == "white":
                    Board.danger_zone_black[des_col][des_row] = True
                else:
                    Board.danger_zone_white[des_col][des_row] = True

                des_piece = board[des_col][des_row]
                if des_piece != None:
                    if des_piece.color == self.color:
                        continue
                    else:
                        attack = True
                        if isinstance(des_piece, King):
                            des_piece.endangered = True
                            des_piece.enemy_piece_attacking = self
                        if your_king.endangered == True:
                            if des_col == p_attacking_king.board_pos[0] and des_row == p_attacking_king.board_pos[1]:
                                self.valid_moves.append((des_col, des_row, attack))
                                continue
                else:
                    attack = False
                
                if your_king.endangered == False:
                    self.valid_moves.append((des_col, des_row, attack))
                else:
                    self.add_if_saves_king(des_col, des_row, p_attacking_king, your_king, attack, game_board)


class Bishop(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Bishop"
        self.moves = [[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)],
                      [(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)],
                      [(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)],
                      [(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)]]
        self.load_image()

    def validate_moves(self, game_board) -> None:
        board = game_board.board
        now_col, now_row = self.board_pos
        color_col_mult = 1
        self.valid_moves = []
        your_king = Board.black_king
        if self.color == "white":
            color_col_mult = -1     
            your_king = Board.white_king
        p_attacking_king = your_king.enemy_piece_attacking


        for set_of_moves in self.moves:
            for move_row_mod, move_col_mod in set_of_moves: 
                des_col = now_col+(move_col_mod*color_col_mult)
                des_row = now_row+move_row_mod
                if 0 <= des_col < 8 and 0 <= des_row < 8: 
                    
                    if self.color == "white":
                        Board.danger_zone_black[des_col][des_row] = True
                    else:
                        Board.danger_zone_white[des_col][des_row] = True

                    des_piece = board[des_col][des_row]
                    if des_piece != None:
                        if des_piece.color == self.color:
                            break
                        else:
                            attack = True
                            if isinstance(des_piece, King):
                                des_piece.endangered = True
                                des_piece.enemy_piece_attacking = self
                            if your_king.endangered == True:
                                if des_col == p_attacking_king.board_pos[0] and des_row == p_attacking_king.board_pos[1]:
                                    self.valid_moves.append((des_col, des_row, attack))
                            else:
                                self.valid_moves.append((des_col, des_row, attack))
                        break
                    else:
                        attack = False
                    
                    if your_king.endangered == False:
                        self.valid_moves.append((des_col, des_row, attack))
                    else:
                        self.add_if_saves_king(des_col, des_row, p_attacking_king, your_king, attack, game_board)
                else:
                    break


class Rook(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Rook"
        self.moves = [[(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7)],
                      [(0,-1), (0,-2), (0,-3), (0,-4), (0,-5), (0,-6), (0,-7)],
                      [(1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0)],
                      [(-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0)]]
        self.moved = False
        self.load_image()

    def validate_moves(self, game_board) -> None:
        board = game_board.board
        now_col, now_row = self.board_pos
        color_col_mult = 1
        self.valid_moves = []
        your_king = Board.black_king
        if self.color == "white":
            color_col_mult = -1     
            your_king = Board.white_king
        p_attacking_king = your_king.enemy_piece_attacking


        for set_of_moves in self.moves:
            for move_row_mod, move_col_mod in set_of_moves: 
                des_col = now_col+(move_col_mod*color_col_mult)
                des_row = now_row+move_row_mod
                if 0 <= des_col < 8 and 0 <= des_row < 8: 
                        
                    if self.color == "white":
                        Board.danger_zone_black[des_col][des_row] = True
                    else:
                        Board.danger_zone_white[des_col][des_row] = True

                    des_piece = board[des_col][des_row]
                    if des_piece != None:
                        if des_piece.color == self.color:
                            break
                        else:
                            attack = True
                            if isinstance(des_piece, King):
                                des_piece.endangered = True
                                des_piece.enemy_piece_attacking = self
                            if your_king.endangered == True:
                                if des_col == p_attacking_king.board_pos[0] and des_row == p_attacking_king.board_pos[1]:
                                    self.valid_moves.append((des_col, des_row, attack))
                            else:
                                self.valid_moves.append((des_col, des_row, attack))
                        break
                    else:
                        attack = False
                    
                    if your_king.endangered == False:
                        self.valid_moves.append((des_col, des_row, attack))
                    else:
                        self.add_if_saves_king(des_col, des_row, p_attacking_king, your_king, attack, game_board)
                else:
                    break


class King(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "King"
        self.endangered = False
        self.enemy_piece_attacking = None
        self.moves = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,-1), (-1,1)]  
        self.moved = False
        if self.color == "white":
            Board.white_king = self
        else:    
            Board.black_king = self
        self.load_image()

    def isEndangered(self) -> bool:
        return self.endangered

    def validate_moves(self, game_board) -> None:
        # Change valid moves to be only moves that will not put king in danger next turn !!!
        board = game_board.board
        now_col, now_row = self.board_pos
        color_col_mult = 1
        self.valid_moves = []
        your_king = Board.black_king
        if self.color == "white":
            color_col_mult = -1     
            your_king = Board.white_king
        p_attacking_king = your_king.enemy_piece_attacking


        if self.color == "white":
            danger_zone = Board.danger_zone_white
        else:
            danger_zone = Board.danger_zone_black

        if self.moved == False: #castling
            row = board[now_col]
            danger_row = danger_zone[now_col]
            if row[now_row-1] == row[now_row-2] == row[now_row-3] == None and isinstance(row[now_row-4], Rook):
                if danger_row[now_row-1] == danger_row[now_row-2] == danger_row[now_row-3] == False and row[now_row-4].moved == False:
                    self.valid_moves.append((now_col, now_row-2, False))
            elif row[now_row+1] == row[now_row+2] == None and isinstance(row[now_row+3], Rook):
                if danger_row[now_row+1] == danger_row[now_row+2] == False and row[now_row+3].moved == False:
                    self.valid_moves.append((now_col, now_row+2, False))

        for move_row_mod, move_col_mod in self.moves: 
            des_col = now_col+(move_col_mod*color_col_mult)
            des_row = now_row+move_row_mod
            if 0 <= des_col < 8 and 0 <= des_row < 8: 
                
                if self.color == "white":
                    Board.danger_zone_black[des_col][des_row] = True
                else:
                    Board.danger_zone_white[des_col][des_row] = True

                des_piece = board[des_col][des_row]
                if des_piece != None:
                    attack = True
                    if des_piece.color == self.color:
                        continue
                else:
                    attack = False
                #print((des_col, des_row))
                #print(danger_zone[des_col][des_row])
                if danger_zone[des_col][des_row] == False:
                    self.valid_moves.append((des_col, des_row, attack))


class Queen(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Queen"
        self.moves = [[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)],
                      [(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)],
                      [(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)],
                      [(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)],
                      [(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7)],
                      [(0,-1), (0,-2), (0,-3), (0,-4), (0,-5), (0,-6), (0,-7)],
                      [(1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0)],
                      [(-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0)]]
        self.load_image()

    def validate_moves(self, game_board) -> None:
        board = game_board.board
        now_col, now_row = self.board_pos
        color_col_mult = 1
        self.valid_moves = []
        your_king = Board.black_king
        if self.color == "white":
            color_col_mult = -1     
            your_king = Board.white_king
        p_attacking_king = your_king.enemy_piece_attacking


        for set_of_moves in self.moves:
            for move_row_mod, move_col_mod in set_of_moves: 
                des_col = now_col+(move_col_mod*color_col_mult)
                des_row = now_row+move_row_mod
                if 0 <= des_col < 8 and 0 <= des_row < 8: 
                        
                    if self.color == "white":
                        Board.danger_zone_black[des_col][des_row] = True
                    else:
                        Board.danger_zone_white[des_col][des_row] = True

                    des_piece = board[des_col][des_row]
                    if des_piece != None:
                        if des_piece.color == self.color:
                            break
                        else:
                            attack = True
                            if isinstance(des_piece, King):
                                des_piece.endangered = True
                                des_piece.enemy_piece_attacking = self
                            if your_king.endangered == True:
                                if des_col == p_attacking_king.board_pos[0] and des_row == p_attacking_king.board_pos[1]:
                                    self.valid_moves.append((des_col, des_row, attack))
                            else:
                                self.valid_moves.append((des_col, des_row, attack))
                        break
                    else:
                        attack = False
                    
                    if your_king.endangered == False:
                        self.valid_moves.append((des_col, des_row, attack))
                    else:
                        self.add_if_saves_king(des_col, des_row, p_attacking_king, your_king, attack, game_board)
                else:
                    break



class Player(Board):
    def __init__(self, name: str, color: str, type: str):
        self.name = name
        self.color = color
        self.type = type