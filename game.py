import pygame
import os


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


def board_pos_to_coords(board_pos) -> tuple:
        return (Board.position_of_board[0]+Board.size_of_board/8*board_pos[1], Board.position_of_board[1]+Board.size_of_board/8*board_pos[0])


def coords_to_board_pos(coords) -> tuple:
        row = (coords[0]-Board.position_of_board[0])//(Board.size_of_board/8)
        col = (coords[1]-Board.position_of_board[1])//(Board.size_of_board/8)
        if 8 > col >= 0 and 8 > row >= 0:
            return (col, row)
        else:
            return -1


class Board():

    white_pieces = []
    black_pieces = []
    all_pieces =[]
    player1_name = "Player1" # name can be changed later
    player2_name = "Player2" # name can be changed later
    
    position_of_board: tuple = (0, 0)
    size_of_board: int = 0
    board_image = None # image loaded 
    board_image_original_size = None # image loaded later

    position_of_identifiers: tuple = (0, 0)
    size_of_identifiers: int = 0
    identifiers_image = None # image loaded 
    identifiers_image_original_size = None # image loaded later


    def __init__(self):

        self.rec = pygame.Rect(*Board.position_of_board, Board.size_of_board, Board.size_of_board)

        self.board = [[0 for _ in range(8)] for _ in range(8)]
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

    def resize_window_reset_pos(self):
        WIDTH, HEIGHT = pygame.display.get_window_size()
        Board.position_of_board = (WIDTH*0.5-(HEIGHT*0.8*0.5), HEIGHT*0.1)
        Board.size_of_board = HEIGHT*0.8
        Board.position_of_identifiers = (WIDTH*0.5-(HEIGHT*0.89*0.5), HEIGHT*0.14)
        Board.size_of_identifiers = HEIGHT*0.81
        #print(WIDTH, HEIGHT)
        #print(type(pygame.display.get_window_size()))

        self.rec.update(*Board.position_of_board, Board.size_of_board, Board.size_of_board)


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

    def __repr__(self):
        return f"{self.__class__.__name__}({self.color}, {self.board_pos})"


class Pawn(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Pawn"
        #print(f"{self.color} Pawn{self.board_pos[1]} position: {self.coords}")
        #print(f"{self.color} Pawn{self.board_pos[1]} size: {self.size}\n")

    def move(self):
        pass


class Knight(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Knight"

    def move(self):
        pass


class Bishop(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Bishop"

    def move(self):
        pass


class Rook(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Rook"

    def move(self):
        pass


class King(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "King"
        self.endangered = False

    def isEndangered(self) -> bool:
        return self.endangered

    def move(self):
        pass


class Queen(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Queen"
    
    def move(self):
        pass





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