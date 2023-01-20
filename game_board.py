import pygame
from pprint import pprint
import os


def board_pos_to_coords(gameBoard, board_pos) -> tuple:
    return (gameBoard.position_of_board[0]+gameBoard.size_of_board/8*board_pos[1], gameBoard.position_of_board[1]+gameBoard.size_of_board/8*board_pos[0])


def coords_to_board_pos(gameBoard, coords) -> tuple:
    row = (coords[0]-gameBoard.position_of_board[0])//(gameBoard.size_of_board/8)
    col = (coords[1]-gameBoard.position_of_board[1])//(gameBoard.size_of_board/8)

    if 8 > col >= 0 and 8 > row >= 0:
        return (int(col), int(row))
    else:
        return -1 



class Board():
    def __init__(self, WIDTH: int = 800, HEIGHT: int = 800):

        self.white_pieces = []
        self.black_pieces = []
        self.all_pieces =[]
        self.holding_piece = None
        self.selected_piece = None
        self.white_king = None
        self.black_king = None

        self.player1 = None
        self.player2 = None
        self.player_on_turn = None

        self.position_of_board: tuple = (WIDTH*0.5-(HEIGHT*0.8*0.5), HEIGHT*0.1)
        self.size_of_board: int = HEIGHT*0.8
        self.board_image = None # image loaded 
        self.board_image_original_size = None # image loaded later

        self.position_of_identifiers: tuple = (WIDTH*0.5-(HEIGHT*0.89*0.5), HEIGHT*0.14)
        self.size_of_identifiers: int = HEIGHT*0.81
        self.identifiers_image = None # image loaded 
        self.identifiers_image_original_size = None # image loaded later

        self.selected_square_image = None  # image loaded later
        self.selected_square_image_original_size = None  # image loaded later
        self.holding_over_square_image = None  # image loaded later
        self.holding_over_square_image_original_size = None  # image loaded later
        self.valid_move_image = None  # image loaded later
        self.valid_move_image_original_size = None  # image loaded later
        self.valid_move_attack_image = None  # image loaded later
        self.valid_move_attack_image_original_size = None  # image loaded later
        self.choose_piece_white_image_original_size = None  # image loaded later
        self.choose_piece_black_image_original_size = None  # image loaded later
        self.choose_piece_white_image = None  # image loaded later
        self.choose_piece_black_image = None  # image loaded later
        self.mouse_on_square = [(),()] # [board_pos, board_pos_coords]

        self.last_turn = [(),()] # [start_board_pos, end_board_pos]
        self.danger_zone_black = [[False for _ in range(8)] for _ in range(8)]
        self.danger_zone_white = [[False for _ in range(8)] for _ in range(8)]

        self.choosing_piece = None

        



        self.rec = pygame.Rect(*self.position_of_board, self.size_of_board, self.size_of_board)

        self.board = [[None for _ in range(8)] for _ in range(8)]
        #print(f"Board: {self.board}")

        self.board[7][4] = King("white", (7, 4), self)
        self.board[0][4] = King("black", (0, 4), self)


        self.board[6][0] = Pawn("white", (6, 0), self)
        self.board[6][1] = Pawn("white", (6, 1), self)
        self.board[6][2] = Pawn("white", (6, 2), self)
        self.board[6][3] = Pawn("white", (6, 3), self)
        self.board[6][4] = Pawn("white", (6, 4), self)
        self.board[6][5] = Pawn("white", (6, 5), self)
        self.board[6][6] = Pawn("white", (6, 6), self)
        self.board[6][7] = Pawn("white", (6, 7), self)

        self.board[7][0] = Rook("white", (7, 0), self)
        self.board[7][1] = Knight("white", (7, 1), self)
        self.board[7][2] = Bishop("white", (7, 2), self)
        self.board[7][3] = Queen("white", (7, 3), self)
        self.board[7][5] = Bishop("white", (7, 5), self)
        self.board[7][6] = Knight("white", (7, 6), self)
        self.board[7][7] = Rook("white", (7, 7), self)


        self.board[0][0] = Rook("black", (0, 0), self)
        self.board[0][1] = Knight("black", (0, 1), self)
        self.board[0][2] = Bishop("black", (0, 2), self)
        self.board[0][3] = Queen("black", (0, 3), self)
        self.board[0][5] = Bishop("black", (0, 5), self)
        self.board[0][6] = Knight("black", (0, 6), self)
        self.board[0][7] = Rook("black", (0, 7), self)

        self.board[1][0] = Pawn("black", (1, 0), self)
        self.board[1][1] = Pawn("black", (1, 1), self)
        self.board[1][2] = Pawn("black", (1, 2), self)
        self.board[1][3] = Pawn("black", (1, 3), self)
        self.board[1][4] = Pawn("black", (1, 4), self)
        self.board[1][5] = Pawn("black", (1, 5), self)
        self.board[1][6] = Pawn("black", (1, 6), self)
        self.board[1][7] = Pawn("black", (1, 7), self)

        #print(f"Board: {self.board}")

        self.player1 = Player("Player1", "white", "Player") # player options can be changed later
        self.player2 = Player("Player2", "black", "Player") # player options can be changed later 
        if self.player1.color == "white":
            self.player_on_turn = self.player1
        elif self.player2.color == "white":
            self.player_on_turn = self.player2
        else:
            print("Problem! Neither player is white!")    


    def resize_window_reset_pos(self):
        WIDTH, HEIGHT = pygame.display.get_window_size()
        self.position_of_board = (WIDTH*0.5-(HEIGHT*0.8*0.5), HEIGHT*0.1)
        self.size_of_board = HEIGHT*0.8
        self.position_of_identifiers = (WIDTH*0.5-(HEIGHT*0.89*0.5), HEIGHT*0.14)
        self.size_of_identifiers = HEIGHT*0.81
        #print(WIDTH, HEIGHT)
        #print(type(pygame.display.get_window_size()))

        self.rec.update(*self.position_of_board, self.size_of_board, self.size_of_board)

    def select_piece(self, mouse_x: float, mouse_y: float) -> None:
        mouse_board_pos = coords_to_board_pos(self, (mouse_x, mouse_y))
        if mouse_board_pos != -1:
            mouse_on_piece = self.board[mouse_board_pos[0]][mouse_board_pos[1]]
            if mouse_on_piece != None:
                #print(selected_piece, self.player_on_turn)
                if mouse_on_piece.color == self.player_on_turn.color:
                    mouse_on_piece.selected = True
                    self.holding_piece = mouse_on_piece
                    self.selected_piece = mouse_on_piece

                    #print(f"Valid moves {selected_piece.type}: {selected_piece.valid_moves}")
                else:
                    #print("ccccc",selected_piece.color == self.player_on_turn.color, selected_piece.color, self.player_on_turn.color, selected_piece)
                    #Board.selected_piece = None
                    print(f"You tried to move piece of different color, \nYour color: {self.player_on_turn.color}, Piece color: {mouse_on_piece.color}\n")
                    self.holding_piece = None
        else:
            self.selected_piece = None
            self.holding_piece = None

    def validate_all_pieces(self, potent_pos_validation = False) -> None:
        self.danger_zone_black = [[False for _ in range(8)] for _ in range(8)]
        self.danger_zone_white = [[False for _ in range(8)] for _ in range(8)]

        for piece in self.all_pieces:
            piece.validate_moves(potent_pos_validation)
      
        
        self.white_king.validate_moves(potent_pos_validation)
        self.black_king.validate_moves(potent_pos_validation)

        for piece in self.all_pieces:
            piece.validate_moves(potent_pos_validation)


        # print("White danger zone: ")
        # pprint(Board.danger_zone_white)
        # print("Black danger zone: ")
        # pprint(Board.danger_zone_black)


class Piece():
    def __init__(self, color: str, board_pos: tuple, gameBoard: Board , selected: bool = False):
        self.board = gameBoard
        self.color = color # "white" or "black"
        self.board_pos = board_pos # (column, row)
        self.coords = board_pos_to_coords(self.board, self.board_pos) # (x, y)
        self.size = self.board.size_of_board/8
        self.selected = selected
        self.rec = pygame.Rect(*self.coords, self.size, self.size)
        self.type = None
        self.valid_moves = [] # updates when spiece selected, [(col, row, attact)]
        self.image = None # image loaded later
        self.image_original_size = None # image loaded later

        if self.color == "white":
            self.your_king = self.board.white_king
        else:
            self.your_king = self.board.black_king
            
        if self.color == "white":
            self.board.white_pieces.append(self)
        elif self.color == "black":
            self.board.black_pieces.append(self)
        self.board.all_pieces.append(self)

    def load_image(self):
        self.image_original_size = pygame.image.load(os.path.join("images/PNG/", f"{self.color}_{self.type.lower()}.png")) 
        self.transform_image()

    def transform_image(self):    
        self.image = pygame.transform.smoothscale(self.image_original_size, (self.size, self.size))

    def isSelected(self) -> bool:
        return self.selected

    def resize_window_reset_pos(self):
        self.coords = board_pos_to_coords(self.board, self.board_pos) # (x, y)
        self.size = self.board.size_of_board/8
        self.rec.update(*self.coords, self.size, self.size)
    
    def move(self, dest_board_pos) -> bool:
        color_col_mult = 1
        if self.color == "white":
            color_col_mult = -1

        #if Board.player_on_turn.color != self.color:
        #    print(f"You tried to move piece of different color, \nYour color: {Board.player_on_turn.color}, Piece color: {self.color}")
        #    return False

        attacking = False
        if (dest_board_pos[0], dest_board_pos[1], False) not in self.valid_moves:
            if (dest_board_pos[0], dest_board_pos[1], True) not in self.valid_moves:
                if self.board_pos != dest_board_pos:
                    print(f"Not valid move!\nFROM: {self.board_pos}  TO: {dest_board_pos}\nValid moves: {self.valid_moves}\n")
                    print(self.board.board)
                    #print(f"Piece droped to it's old position\n")
                return False
            else:
                attacking = True
                

        # ---------------------- Special moves
        if self.type == "Pawn" and attacking == False: # en passant move, left and right
            if dest_board_pos[1] != self.board_pos[1]: #  - test if not normal forward move
                self.attack((dest_board_pos[0]-color_col_mult, dest_board_pos[1])) 
                attacking = False
            
        other_side = 0 if self.color == "white" else 7
        if self.type == "Pawn" and dest_board_pos[0] == other_side:
            #change pawn to piece of choice
            self.board.choosing_piece = self

        elif self.type == "King":
            self.endangered = False
            self.enemy_piece_attacking = None
            if dest_board_pos[1] - self.board_pos[1] == -2: # castling left
                print(f"MOVEMENT, {self.board.player_on_turn.name}\nCastling left")
                rook = self.board.board[self.board_pos[0]][self.board_pos[1]-4]
                rook.moved = True
                self.board.board[self.board_pos[0]][self.board_pos[1]-4] = None
                self.board.board[self.board_pos[0]][self.board_pos[1]-1] = rook
                rook.coords = board_pos_to_coords(self.board, (self.board_pos[0], self.board_pos[1]-1))
                rook.board_pos = (self.board_pos[0], self.board_pos[1]-1)
                #move rook one to right +, of dest
            if dest_board_pos[1] - self.board_pos[1] == 2: # castling right
                print(f"MOVEMENT, {self.board.player_on_turn.name}\nCastling right")
                rook = self.board.board[self.board_pos[0]][self.board_pos[1]+3]
                rook.moved = True
                self.board.board[self.board_pos[0]][self.board_pos[1]+3] = None
                self.board.board[self.board_pos[0]][self.board_pos[1]+1] = rook
                rook.coords = board_pos_to_coords(self.board, (self.board_pos[0], self.board_pos[1]+1))
                rook.board_pos = (self.board_pos[0], self.board_pos[1]+1)

                #move rook one to left -, of dest
        if attacking == True:
            self.attack(dest_board_pos)
        # ----------------------

        print(f"MOVEMENT, {self.board.player_on_turn.name}\nFROM: {self.board_pos}  TO: {dest_board_pos}")
        self.board.last_turn = [self.board_pos, dest_board_pos]
        if self.type in ["King","Rook", "Pawn"]:
            self.moved = True


        # Switch player on turn
        if self.board.player_on_turn == self.board.player1:
            self.board.player_on_turn = self.board.player2
        elif self.board.player_on_turn == self.board.player2:
            self.board.player_on_turn = self.board.player1
        else:
            print("Problem!!!, Program didn't switch players!")
        print(f"Switched players, player on move: {self.board.player_on_turn.name}\n")


        self.board.board[self.board.selected_piece.board_pos[0]][self.board.selected_piece.board_pos[1]] = None
        self.board.board[dest_board_pos[0]][dest_board_pos[1]] = self.board.selected_piece

        self.board.selected_piece.coords = board_pos_to_coords(self.board, dest_board_pos)
        self.board.selected_piece.board_pos = dest_board_pos
        self.board.holding_piece = None
        self.board.selected_piece = None

        self.board.validate_all_pieces()

        return True

    def attack(self, dest_board_pos) -> bool:
        des_col, des_row = dest_board_pos 
        attacked_piece = self.board.board[des_col][des_row]
        self.board.board[des_col][des_row] = None
        self.board.all_pieces.remove(attacked_piece)
        if attacked_piece.color == "white":
            self.board.white_pieces.remove(attacked_piece)
        else:
            self.board.black_pieces.remove(attacked_piece)
        print(f"{self} attacked {attacked_piece}")

    def will_save_his_king(self, des_col, des_row, p_attacking_king, potent_pos_validation) -> bool:
        if potent_pos_validation == False:
            king_state_w, king_state_b = self.board.black_king.endangered, self.board.white_king.endangered
            original_dest_piece = self.board.board[des_col][des_row]
            self.board.board[des_col][des_row] = self
            p_attacking_king.validate_moves(potent_pos_validation = True)
            self.board.black_king.endangered, self.board.white_king.endangered = king_state_b, king_state_w

            self.board.board[des_col][des_row] = original_dest_piece
            if (self.your_king.board_pos[0], self.your_king.board_pos[1], True) not in p_attacking_king.valid_moves:
                p_attacking_king.validate_moves()
                return True
            else:
                p_attacking_king.validate_moves()
                return False

    def will_endanger_his_king(self):
        king_state_w, king_state_b = self.board.black_king.endangered, self.board.white_king.endangered
        self.board.board[self.board_pos[0]][self.board_pos[1]] = None
        for piece in self.board.all_pieces:
            piece.validate_moves(potent_pos_validation = True)
        self.board.board[self.board_pos[0]][self.board_pos[1]] = self

        if self.your_king.endangered == False:
            self.board.black_king.endangered, self.board.white_king.endangered = king_state_b, king_state_w
            return False
        else:
            self.board.black_king.endangered, self.board.white_king.endangered = king_state_b, king_state_w
            #print("--------------------------------------------------------endangered king ", self)
            return True

    def valid_moves_append(self, des_col, des_row, attack, potent_pos_validation):
        if potent_pos_validation == False:
            if isinstance(self, King):
                self.valid_moves.append((des_col, des_row, attack))
            elif not self.will_endanger_his_king():
                self.valid_moves.append((des_col, des_row, attack))


    def __repr__(self):
        return f"{self.__class__.__name__}({self.color}, {self.board_pos})"


class Pawn(Piece):
    def __init__(self, color: str, board_pos: tuple, gameBoard: Board , selected: bool = False):
        super().__init__(color, board_pos, gameBoard, selected)
        self.type = "Pawn"
        self.moved = False
        self.load_image()

    def promote(self, piece):
        if piece == "Queen":
            self.board.board[self.board_pos[0]][self.board_pos[1]] = Queen(self.color, self.board_pos)
            print(f"\n{self.board.player_on_turn.name} chose Queen\n")
        if piece == "Rook":
            self.board.board[self.board_pos[0]][self.board_pos[1]] = Rook(self.color, self.board_pos)
            print(f"\n{self.board.player_on_turn.name} chose Rook\n")
        if piece == "Knight":
            self.board.board[self.board_pos[0]][self.board_pos[1]] = Knight(self.color, self.board_pos)
            print(f"\n{self.board.player_on_turn.name} chose Knight\n")
        if piece == "Bishop":
            self.board.board[self.board_pos[0]][self.board_pos[1]] = Bishop(self.color, self.board_pos)
            print(f"\n{self.board.player_on_turn.name} chose Bishop\n")
            
        self.board.all_pieces.remove(self)
        if self.color == "white":
            self.board.white_pieces.remove(self)
        else:
            self.board.black_pieces.remove(self)

        self.board.holding_piece = None
        self.board.selected_piece = None
        self.board.validate_all_pieces()


    def validate_moves(self, potent_pos_validation = False) -> None:
        # add special move !
        now_col, now_row = self.board_pos
        color_col_mult = 1
        if potent_pos_validation == False:
            self.valid_moves = []
        if self.color == "white":
            color_col_mult = -1    
        p_attacking_king = self.your_king.enemy_piece_attacking
           
        if  0 <= now_col+(1*color_col_mult) < 8: # one forward
            if self.board.board[now_col+(1*color_col_mult)][now_row] == None:   
                if self.your_king.endangered == False:
                    #if not self.will_endanger_his_king():
                    self.valid_moves_append(now_col+(1*color_col_mult), now_row, False, potent_pos_validation)
                else:
                    if self.will_save_his_king(now_col+(1*color_col_mult), now_row, p_attacking_king, potent_pos_validation):
                        self.valid_moves_append(now_col+(1*color_col_mult), now_row, False, potent_pos_validation)

        if 0 <= now_col+(2*color_col_mult) < 8: # first move two forward
            if self.board.board[now_col+(2*color_col_mult)][now_row] == None and self.board.board[now_col+(1*color_col_mult)][now_row] == None: 
                if self.moved == False:
                    if self.your_king.endangered == False:
                        self.valid_moves_append(now_col+(2*color_col_mult), now_row, False, potent_pos_validation)
                    else:
                        if self.will_save_his_king(now_col+(2*color_col_mult), now_row, p_attacking_king, potent_pos_validation):
                            self.valid_moves_append(now_col+(2*color_col_mult), now_row, False, potent_pos_validation)

        for direction in [1,-1]: # en passant move, left and right
            if 0 <= now_col+(1*color_col_mult) < 8 and 0 <= now_row+(direction) < 8 : 
                attacked_pawn = self.board.board[now_col][now_row+(direction)]
                if self.board.board[now_col+(1*color_col_mult)][now_row+(direction)] == None and isinstance(attacked_pawn, Pawn):
                    if self.board.last_turn[0] == (now_col+(2*color_col_mult), now_row+(direction)) and self.board.last_turn[1] == (now_col, now_row+(direction)):
                        if self.your_king.endangered == False:
                            self.valid_moves_append(now_col+(1*color_col_mult), now_row+(direction), False, potent_pos_validation)
                        else:
                            if self.will_save_his_king(now_col+(1*color_col_mult), now_row+(direction), p_attacking_king, potent_pos_validation):
                                self.valid_moves_append(now_col+(1*color_col_mult), now_row+(direction), False, potent_pos_validation)

        for move_row_mod, move_col_mod in [(1,1), (-1,1)]: # one up diagonal, one left diagonal
            des_col = now_col+(move_col_mod*color_col_mult)
            des_row = now_row+move_row_mod
            if 0 <= des_col < 8 and 0 <= des_row < 8: 
                if potent_pos_validation == False:
                    if self.color == "white":
                        self.board.danger_zone_black[des_col][des_row] = True
                    else:
                        self.board.danger_zone_white[des_col][des_row] = True

                des_piece = self.board.board[des_col][des_row]
                if des_piece != None:
                    if des_piece.color == self.color:
                        continue
                    else:
                        attack = True
                        if isinstance(des_piece, King):
                            des_piece.endangered = True
                            des_piece.enemy_piece_attacking = self
                        if self.your_king.endangered == True:
                            if des_col == p_attacking_king.board_pos[0] and des_row == p_attacking_king.board_pos[1]:
                                self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                                continue
                else:
                    attack = False

                if attack == True:
                    if self.your_king.endangered == False:
                        self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                    else:
                        if self.will_save_his_king(des_col, des_row, p_attacking_king, potent_pos_validation):
                            self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)

    #def move(self) -> bool:
    #    return True


class Knight(Piece):
    def __init__(self, color: str, board_pos: tuple, gameBoard: Board , selected: bool = False):
        super().__init__(color, board_pos, gameBoard, selected)
        self.type = "Knight"
        self.moves = [(1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1), (-2,1), (-1,2)]
        self.load_image()

    def validate_moves(self, potent_pos_validation = False) -> None:
        now_col, now_row = self.board_pos
        color_col_mult = 1
        if potent_pos_validation == False:
            self.valid_moves = []
        if self.color == "white":
            color_col_mult = -1     
        p_attacking_king = self.your_king.enemy_piece_attacking


        for move_row_mod, move_col_mod in self.moves: 
            des_col = now_col+(move_col_mod*color_col_mult)
            des_row = now_row+move_row_mod
            if 0 <= des_col < 8 and 0 <= des_row < 8: 
                if potent_pos_validation == False:
                    if self.color == "white":
                        self.board.danger_zone_black[des_col][des_row] = True
                    else:
                        self.board.danger_zone_white[des_col][des_row] = True

                des_piece = self.board.board[des_col][des_row]
                if des_piece != None:
                    if des_piece.color == self.color:
                        continue
                    else:
                        attack = True
                        if isinstance(des_piece, King):
                            des_piece.endangered = True
                            des_piece.enemy_piece_attacking = self
                        if self.your_king.endangered == True:
                            if des_col == p_attacking_king.board_pos[0] and des_row == p_attacking_king.board_pos[1]:
                                self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                                continue
                else:
                    attack = False
                
                if self.your_king.endangered == False:
                    self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                else:
                    if self.will_save_his_king(des_col, des_row, p_attacking_king, potent_pos_validation):
                        self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)


class Bishop(Piece):
    def __init__(self, color: str, board_pos: tuple, gameBoard: Board , selected: bool = False):
        super().__init__(color, board_pos, gameBoard, selected)
        self.type = "Bishop"
        self.moves = [[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)],
                      [(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)],
                      [(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)],
                      [(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)]]
        self.load_image()

    def validate_moves(self, potent_pos_validation = False) -> None:
        now_col, now_row = self.board_pos
        color_col_mult = 1
        if potent_pos_validation == False:
            self.valid_moves = []
        if self.color == "white":
            color_col_mult = -1     
        p_attacking_king = self.your_king.enemy_piece_attacking


        for set_of_moves in self.moves:
            for move_row_mod, move_col_mod in set_of_moves: 
                des_col = now_col+(move_col_mod*color_col_mult)
                des_row = now_row+move_row_mod
                if 0 <= des_col < 8 and 0 <= des_row < 8: 
                    if potent_pos_validation == False:
                        if self.color == "white":
                            self.board.danger_zone_black[des_col][des_row] = True
                        else:
                            self.board.danger_zone_white[des_col][des_row] = True

                    des_piece = self.board.board[des_col][des_row]
                    if des_piece != None:
                        if des_piece.color == self.color:
                            break
                        else:
                            attack = True
                            if isinstance(des_piece, King):
                                des_piece.endangered = True
                                des_piece.enemy_piece_attacking = self
                            if self.your_king.endangered == True:
                                if des_col == p_attacking_king.board_pos[0] and des_row == p_attacking_king.board_pos[1]:
                                    self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                            else:
                                self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                        break
                    else:
                        attack = False
                    
                    if self.your_king.endangered == False:
                        self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                    else:
                        if self.will_save_his_king(des_col, des_row, p_attacking_king, potent_pos_validation):
                            self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                else:
                    break


class Rook(Piece):
    def __init__(self, color: str, board_pos: tuple, gameBoard: Board , selected: bool = False):
        super().__init__(color, board_pos, gameBoard, selected)
        self.type = "Rook"
        self.moves = [[(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7)],
                      [(0,-1), (0,-2), (0,-3), (0,-4), (0,-5), (0,-6), (0,-7)],
                      [(1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0)],
                      [(-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0)]]
        self.moved = False
        self.load_image()

    def validate_moves(self, potent_pos_validation = False) -> None:
        now_col, now_row = self.board_pos
        color_col_mult = 1
        if potent_pos_validation == False:
            self.valid_moves = []
        if self.color == "white":
            color_col_mult = -1     
        p_attacking_king = self.your_king.enemy_piece_attacking


        for set_of_moves in self.moves:
            for move_row_mod, move_col_mod in set_of_moves: 
                des_col = now_col+(move_col_mod*color_col_mult)
                des_row = now_row+move_row_mod
                if 0 <= des_col < 8 and 0 <= des_row < 8: 
                    if potent_pos_validation == False:
                        if self.color == "white":
                            self.board.danger_zone_black[des_col][des_row] = True
                        else:
                            self.board.danger_zone_white[des_col][des_row] = True

                    des_piece = self.board.board[des_col][des_row]
                    if des_piece != None:
                        if des_piece.color == self.color:
                            break
                        else:
                            attack = True
                            if isinstance(des_piece, King):
                                des_piece.endangered = True
                                des_piece.enemy_piece_attacking = self
                            if self.your_king.endangered == True:
                                if des_col == p_attacking_king.board_pos[0] and des_row == p_attacking_king.board_pos[1]:
                                    self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                            else:
                                self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                        break
                    else:
                        attack = False
                    
                    if self.your_king.endangered == False:
                        self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                    else:
                        if self.will_save_his_king(des_col, des_row, p_attacking_king, potent_pos_validation):
                            self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                else:
                    break


class King(Piece):
    def __init__(self, color: str, board_pos: tuple, gameBoard: Board , selected: bool = False):
        super().__init__(color, board_pos, gameBoard, selected)
        self.type = "King"
        self.endangered = False
        self.enemy_piece_attacking = None
        self.moves = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,-1), (-1,1)]  
        self.moved = False
        if self.color == "white":
            self.board.white_king = self
        else:    
            self.board.black_king = self
        self.load_image()

    def isEndangered(self) -> bool:
        return self.endangered

    def validate_moves(self, potent_pos_validation = False) -> None:
        # Change valid moves to be only moves that will not put king in danger next turn !!!
        now_col, now_row = self.board_pos
        color_col_mult = 1
        if potent_pos_validation == False:
            self.valid_moves = []
        if self.color == "white":
            color_col_mult = -1     


        if self.color == "white":
            danger_zone = self.board.danger_zone_white
        else:
            danger_zone = self.board.danger_zone_black

        if self.moved == False: #castling
            row = self.board.board[now_col]
            danger_row = danger_zone[now_col]
            if row[now_row-1] == row[now_row-2] == row[now_row-3] == None and isinstance(row[now_row-4], Rook):
                if danger_row[now_row-1] == danger_row[now_row-2] == danger_row[now_row-3] == False and row[now_row-4].moved == False:
                    self.valid_moves_append(now_col, now_row-2, False, potent_pos_validation)
            elif row[now_row+1] == row[now_row+2] == None and isinstance(row[now_row+3], Rook):
                if danger_row[now_row+1] == danger_row[now_row+2] == False and row[now_row+3].moved == False:
                    self.valid_moves_append(now_col, now_row+2, False, potent_pos_validation)

        for move_row_mod, move_col_mod in self.moves: 
            des_col = now_col+(move_col_mod*color_col_mult)
            des_row = now_row+move_row_mod
            if 0 <= des_col < 8 and 0 <= des_row < 8: 
                if potent_pos_validation == False:
                    if self.color == "white":
                        self.board.danger_zone_black[des_col][des_row] = True
                    else:
                        self.board.danger_zone_white[des_col][des_row] = True

                des_piece = self.board.board[des_col][des_row]
                if des_piece != None:
                    attack = True
                    if des_piece.color == self.color:
                        continue
                else:
                    attack = False
                #print((des_col, des_row))
                #print(danger_zone[des_col][des_row])
                if danger_zone[des_col][des_row] == False:
                    self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)


class Queen(Piece):
    def __init__(self, color: str, board_pos: tuple, gameBoard: Board , selected: bool = False):
        super().__init__(color, board_pos, gameBoard, selected)
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

    def validate_moves(self, potent_pos_validation = False) -> None:
        now_col, now_row = self.board_pos
        color_col_mult = 1
        if potent_pos_validation == False:
            self.valid_moves = []
        if self.color == "white":
            color_col_mult = -1     
        p_attacking_king = self.your_king.enemy_piece_attacking


        for set_of_moves in self.moves:
            for move_row_mod, move_col_mod in set_of_moves: 
                des_col = now_col+(move_col_mod*color_col_mult)
                des_row = now_row+move_row_mod
                if 0 <= des_col < 8 and 0 <= des_row < 8: 
                    if potent_pos_validation == False:
                        if self.color == "white":
                            self.board.danger_zone_black[des_col][des_row] = True
                        else:
                            self.board.danger_zone_white[des_col][des_row] = True

                    des_piece = self.board.board[des_col][des_row]
                    if des_piece != None:
                        if des_piece.color == self.color:
                            break
                        else:
                            attack = True
                            if isinstance(des_piece, King):
                                des_piece.endangered = True
                                des_piece.enemy_piece_attacking = self
                            if self.your_king.endangered == True:
                                if des_col == p_attacking_king.board_pos[0] and des_row == p_attacking_king.board_pos[1]:
                                    self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                            else:
                                self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                        break
                    else:
                        attack = False
                    
                    if self.your_king.endangered == False:
                        self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                    else:
                        if self.will_save_his_king(des_col, des_row, p_attacking_king, potent_pos_validation):
                            self.valid_moves_append(des_col, des_row, attack, potent_pos_validation)
                else:
                    break



class Player(Board):
    def __init__(self, name: str, color: str, type: str):
        self.name = name
        self.color = color
        self.type = type