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
    WINDOW.blit(Board.board_image, Board.position_of_board)
    WINDOW.blit(Board.identifiers_image, Board.position_of_identifiers)

    for p in Board.white_pieces:
        WINDOW.blit(p.image, p.position)
    for p in Board.black_pieces:
        WINDOW.blit(p.image, p.position)

    pygame.display.update()

def load_images():
    Board.board_image = pygame.image.load(os.path.join("images/PNG/", "board1.png"))
    Board.board_image = pygame.transform.scale(Board.board_image, (Board.size_of_board, Board.size_of_board))

    Board.identifiers_image = pygame.image.load(os.path.join("images/PNG/", "identifiers.png"))
    Board.identifiers_image = pygame.transform.scale(Board.identifiers_image, (Board.size_of_identifiers, Board.size_of_identifiers))

    for p in Board.white_pieces:
        #print(f"Loading: {p.color}_{p.type.lower()}.png")
        p.image = pygame.image.load(os.path.join("images/PNG/", f"{p.color}_{p.type.lower()}.png")) 
        p.image = pygame.transform.scale(p.image, (p.size, p.size))
    for p in Board.black_pieces:
        #print(f"Loading: {p.color}_{p.type.lower()}.png")
        p.image = pygame.image.load(os.path.join("images/PNG/", f"{p.color}_{p.type.lower()}.png")) 
        p.image = pygame.transform.scale(p.image, (p.size, p.size))


class Board():

    white_pieces = []
    black_pieces = []
    player1_name = "Player1" # name can be changed later
    player2_name = "Player2" # name can be changed later
    
    position_of_board: tuple = (0, 0)
    size_of_board: int = 0
    board_image = None # image loaded later

    identifiers_image = None # image loaded later
    position_of_identifiers: tuple = (0, 0)
    size_of_identifiers: int = 0

    def __init__(self):

        self.board = [[0 for _ in range(8)] for _ in range(8)]
        print(f"Board: {self.board}")

        self.board[0][0] = Rook("white", (0, 0))
        self.board[0][1] = Knight("white", (0, 1))
        self.board[0][2] = Bishop("white", (0, 2))
        self.board[0][3] = Queen("white", (0, 3))
        self.board[0][4] = King("white", (0, 4))
        self.board[0][5] = Bishop("white", (0, 5))
        self.board[0][6] = Knight("white", (0, 6))
        self.board[0][7] = Rook("white", (0, 7))

        self.board[1][0] = Pawn("white", (1, 0))
        self.board[1][1] = Pawn("white", (1, 1))
        self.board[1][2] = Pawn("white", (1, 2))
        self.board[1][3] = Pawn("white", (1, 3))
        self.board[1][4] = Pawn("white", (1, 4))
        self.board[1][5] = Pawn("white", (1, 5))
        self.board[1][6] = Pawn("white", (1, 6))
        self.board[1][7] = Pawn("white", (1, 7))


        self.board[6][0] = Pawn("black", (6, 0))
        self.board[6][1] = Pawn("black", (6, 1))
        self.board[6][2] = Pawn("black", (6, 2))
        self.board[6][3] = Pawn("black", (6, 3))
        self.board[6][4] = Pawn("black", (6, 4))
        self.board[6][5] = Pawn("black", (6, 5))
        self.board[6][6] = Pawn("black", (6, 6))
        self.board[6][7] = Pawn("black", (6, 7))

        self.board[7][0] = Rook("black", (7, 0))
        self.board[7][1] = Knight("black", (7, 1))
        self.board[7][2] = Bishop("black", (7, 2))
        self.board[7][3] = Queen("black", (7, 3))
        self.board[7][4] = King("black", (7, 4))
        self.board[7][5] = Bishop("black", (7, 5))
        self.board[7][6] = Knight("black", (7, 6))
        self.board[7][7] = Rook("black", (7, 7))

        #print(f"Board: {self.board}")


class Piece(Board):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        self.color = color # "white" or "black"
        self.board_pos = board_pos # (column, row)
        self.position = (Board.position_of_board[0]+Board.size_of_board/8*self.board_pos[1], Board.position_of_board[1]+Board.size_of_board/8*self.board_pos[0]) # (x, y)
        self.size = Board.size_of_board/8
        self.image = None # image loaded later
        self.selected = selected

        if self.color == "white":
            Board.white_pieces.append(self)
        elif self.color == "black":
            Board.black_pieces.append(self)

    def isSelected(self) -> bool:
        return self.selected

    def __repr__(self):
        return f"{self.__class__.__name__}({self.color}, {self.board_pos})"


class Pawn(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Pawn"
        self.image = None # image loaded later
        print(f"{self.color} Pawn{self.board_pos[1]} position: {self.position}")
        print(f"{self.color} Pawn{self.board_pos[1]} size: {self.size}\n")

    def move(self):
        pass


class Knight(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Knight"
        self.image = None # image loaded later

    def move(self):
        pass


class Bishop(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Bishop"
        self.image = None # image loaded later

    def move(self):
        pass


class Rook(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Rook"
        self.image = None # image loaded later

    def move(self):
        pass


class King(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "King"
        self.image = None # image loaded 
        self.endangered = False

    def isEndangered(self) -> bool:
        return self.endangered

    def move(self):
        pass


class Queen(Piece):
    def __init__(self, color: str, board_pos: tuple, selected: bool = False):
        super().__init__(color, board_pos, selected)
        self.type = "Queen"
        self.image = None # image loaded later
    
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

    Board()
    #print(Board.white_pieces)
    #print(Board.black_pieces)
    load_images()
    
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