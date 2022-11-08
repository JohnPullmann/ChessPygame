import pygame


def board_pos_to_coords(board_pos) -> tuple:
        return (Board.position_of_board[0]+Board.size_of_board/8*board_pos[1], Board.position_of_board[1]+Board.size_of_board/8*board_pos[0])


def coords_to_board_pos(coords) -> tuple:
        row = (coords[0]-Board.position_of_board[0])//(Board.size_of_board/8)
        col = (coords[1]-Board.position_of_board[1])//(Board.size_of_board/8)

        #row = row if row >= 0 else 0
        #row = row if row < 8 else 7
        #col = col if col >= 0 else 0
        #col = col if col < 8 else 7

        #return (int(col), int(row))

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

        Board.player1 = Player("Player1", "white") # player options can be changed later
        Board.player2 = Player("Player2", "black") # player options can be changed later 
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
    
    def move(self, dest_board_pos) -> bool:
        if self.board_pos != dest_board_pos:
            if Board.player_on_turn.color == self.color:
                print(f"MOVEMENT, {Board.player_on_turn.name}\nFROM: {self.board_pos}  TO: {dest_board_pos}\n")

                if Board.player_on_turn == Board.player1:
                    Board.player_on_turn = Board.player2
                elif Board.player_on_turn == Board.player2:
                    Board.player_on_turn = Board.player1
                else:
                    print("Problem!!!, Program didn't switch players!")
                print(f"Switched players, player on move: {Board.player_on_turn.name}")
                Board.last_turn = [self.board_pos, dest_board_pos]

                return True

            else:
                print(f"You tried to move piece of different color, \nYour color: {Board.player_on_turn.color}, Piece color: {self.color}")
        else:
            print(f"Same board pos, not moved \nFROM: {self.board_pos}  TO: {dest_board_pos}\n")
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.color}, {self.board_pos})"


class Pawn(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Pawn"
        #print(f"{self.color} Pawn{self.board_pos[1]} position: {self.coords}")
        #print(f"{self.color} Pawn{self.board_pos[1]} size: {self.size}\n")

    #def move(self) -> bool:
    #    return True


class Knight(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Knight"



class Bishop(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Bishop"



class Rook(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Rook"



class King(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "King"
        self.endangered = False

    def isEndangered(self) -> bool:
        return self.endangered



class Queen(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Queen"
    

class Player(Board):
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color