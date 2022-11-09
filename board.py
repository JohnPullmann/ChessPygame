import pygame


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
    mouse_on_square = [(),()] # [board_pos, board_pos_coords]

    last_turn = [(),()] # [start_board_pos, end_board_pos]

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
            selected_piece = self.board[mouse_board_pos[0]][mouse_board_pos[1]]
            if selected_piece != None:
                #print(selected_piece, self.player_on_turn)
                if selected_piece.color == self.player_on_turn.color:
                    selected_piece.selected = True
                    Board.holding_piece = selected_piece
                    Board.selected_piece = selected_piece
                    selected_piece.validate_moves(self)
                    #print(f"Valid moves {selected_piece.type}: {selected_piece.valid_moves}")
                else:
                    Board.selected_piece = None
                    Board.holding_piece = None
        else:
            Board.selected_piece = None
            Board.holding_piece = None



class Piece(Board):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        self.color = color # "white" or "black"
        self.board_pos = board_pos # (column, row)
        self.coords = board_pos_to_coords(self.board_pos) # (x, y)
        self.size = Board.size_of_board/8
        self.image = None # image loaded later
        self.image_original_size = None # image loaded later
        self.selected = selected
        self.rec = pygame.Rect(*self.coords, self.size, self.size)
        self.type = None
        self.valid_moves = [] # updates when spiece selected, [(col, row, attact)]

        if self.color == "white":
            Board.white_pieces.append(self)
        elif self.color == "black":
            Board.black_pieces.append(self)
        Board.all_pieces.append(self)


    def isSelected(self) -> bool:
        return self.selected

    def resize_window_reset_pos(self):
        self.coords = board_pos_to_coords(self.board_pos) # (x, y)
        self.size = Board.size_of_board/8
        self.rec.update(*self.coords, self.size, self.size)
    
    def move(self, dest_board_pos, game_board: Board) -> bool:
        if Board.player_on_turn.color != self.color:
            print(f"You tried to move piece of different color, \nYour color: {Board.player_on_turn.color}, Piece color: {self.color}")
            return False

        if (dest_board_pos[0], dest_board_pos[1], False) not in self.valid_moves:
            if (dest_board_pos[0], dest_board_pos[1], True) not in self.valid_moves:
                print(f"Not valid move!\nFROM: {self.board_pos}  TO: {dest_board_pos}\nValid moves: {self.valid_moves}\n")
                return False
            else:
                self.attack(dest_board_pos, game_board)
            

        print(f"MOVEMENT, {Board.player_on_turn.name}\nFROM: {self.board_pos}  TO: {dest_board_pos}")
        Board.last_turn = [self.board_pos, dest_board_pos]

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

        return True

    def attack(self, dest_board_pos, game_board: Board) -> bool:
        des_col, des_row = dest_board_pos 
        attacked_piece = game_board.board[des_col][des_row]
        game_board.board[des_col][des_row] = None
        white_pieces = []
        black_pieces = []
        Board.all_pieces.remove(attacked_piece)
        if attacked_piece.color == "white":
            Board.white_pieces.remove(attacked_piece)
        else:
            Board.black_pieces.remove(attacked_piece)
        print(f"{self} attacked {attacked_piece}")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.color}, {self.board_pos})"


class Pawn(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Pawn"

    def validate_moves(self, game_board) -> None:
        # add special move !
        board = game_board.board
        now_col, now_row = self.board_pos
        color_col_mult = 1
        self.valid_moves = []
        if self.color == "white":
            color_col_mult = -1        

        
        if board[now_col+(1*color_col_mult)][now_row] == None and 0 <= now_col+(1*color_col_mult) < 8: # one forward
            self.valid_moves.append((now_col+(1*color_col_mult), now_row, False))

        if board[now_col+(2*color_col_mult)][now_row] == None and 0 <= now_col+(2*color_col_mult) < 8: # first move two forward 
            if now_col == 1 or now_col == 6:
                self.valid_moves.append((now_col+(2*color_col_mult), now_row, False))

        for move_row_mod, move_col_mod in [(1,1), (-1,1)]: # one up diagonal, one left diagonal
            des_col = now_col+(move_col_mod*color_col_mult)
            des_row = now_row+move_row_mod
            if 0 <= des_col < 8 and 0 <= des_row < 8: 
                des_piece = board[des_col][des_row]
                if des_piece != None:
                    attack = True
                    if des_piece.color == self.color:
                        continue
                else:
                    attack = False
                if attack == True:
                    self.valid_moves.append((des_col, des_row, attack))

    #def move(self) -> bool:
    #    return True


class Knight(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Knight"
        self.moves = [(1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1), (-2,1), (-1,2)]

    def validate_moves(self, game_board) -> None:
        board = game_board.board
        now_col, now_row = self.board_pos
        color_col_mult = 1
        self.valid_moves = []
        if self.color == "white":
            color_col_mult = -1    

        for move_row_mod, move_col_mod in self.moves: 
            des_col = now_col+(move_col_mod*color_col_mult)
            des_row = now_row+move_row_mod
            if 0 <= des_col < 8 and 0 <= des_row < 8: 
                des_piece = board[des_col][des_row]
                if des_piece != None:
                    attack = True
                    if des_piece.color == self.color:
                        continue
                else:
                    attack = False

                self.valid_moves.append((des_col, des_row, attack))


class Bishop(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Bishop"
        self.moves = [[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)],
                      [(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)],
                      [(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)],
                      [(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)]]

    def validate_moves(self, game_board) -> None:
        board = game_board.board
        now_col, now_row = self.board_pos
        color_col_mult = 1
        self.valid_moves = []
        if self.color == "white":
            color_col_mult = -1    

        for set_of_moves in self.moves:
            for move_row_mod, move_col_mod in set_of_moves: 
                des_col = now_col+(move_col_mod*color_col_mult)
                des_row = now_row+move_row_mod
                if 0 <= des_col < 8 and 0 <= des_row < 8: 
                    des_piece = board[des_col][des_row]
                    if des_piece != None:
                        attack = True
                        if des_piece.color == self.color:
                            break
                        self.valid_moves.append((des_col, des_row, attack))
                        break
                    else:
                        attack = False

                    self.valid_moves.append((des_col, des_row, attack))
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
    
    def validate_moves(self, game_board) -> None:
        board = game_board.board
        now_col, now_row = self.board_pos
        color_col_mult = 1
        self.valid_moves = []
        if self.color == "white":
            color_col_mult = -1    

        for set_of_moves in self.moves:
            for move_row_mod, move_col_mod in set_of_moves: 
                des_col = now_col+(move_col_mod*color_col_mult)
                des_row = now_row+move_row_mod
                if 0 <= des_col < 8 and 0 <= des_row < 8: 
                    des_piece = board[des_col][des_row]
                    if des_piece != None:
                        attack = True
                        if des_piece.color == self.color:
                            break
                        self.valid_moves.append((des_col, des_row, attack))
                        break
                    else:
                        attack = False

                    self.valid_moves.append((des_col, des_row, attack))
                else:
                    break


class King(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "King"
        self.endangered = False
        self.moves = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,-1), (-1,1)]  

    def isEndangered(self) -> bool:
        return self.endangered

    def validate_moves(self, game_board) -> None:
        # Change valid moves to be only moves that will not put king in danger next turn !!!
        board = game_board.board
        now_col, now_row = self.board_pos
        color_col_mult = 1
        self.valid_moves = []
        if self.color == "white":
            color_col_mult = -1    

        for move_row_mod, move_col_mod in self.moves: 
            des_col = now_col+(move_col_mod*color_col_mult)
            des_row = now_row+move_row_mod
            if 0 <= des_col < 8 and 0 <= des_row < 8: 
                des_piece = board[des_col][des_row]
                print("a", des_piece, (move_row_mod, move_col_mod), (des_col, des_row))
                if des_piece != None:
                    print("b")
                    attack = True
                    if des_piece.color == self.color:
                        print("c")
                        continue
                else:
                    attack = False

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

    def validate_moves(self, game_board) -> None:
        board = game_board.board
        now_col, now_row = self.board_pos
        color_col_mult = 1
        self.valid_moves = []
        if self.color == "white":
            color_col_mult = -1    

        for set_of_moves in self.moves:
            for move_row_mod, move_col_mod in set_of_moves: 
                des_col = now_col+(move_col_mod*color_col_mult)
                des_row = now_row+move_row_mod
                if 0 <= des_col < 8 and 0 <= des_row < 8: 
                    des_piece = board[des_col][des_row]
                    if des_piece != None:
                        attack = True
                        if des_piece.color == self.color:
                            break
                        self.valid_moves.append((des_col, des_row, attack))
                        break
                    else:
                        attack = False

                    self.valid_moves.append((des_col, des_row, attack))
                else:
                    break



class Player(Board):
    def __init__(self, name: str, color: str, type: str):
        self.name = name
        self.color = color
        self.type = type