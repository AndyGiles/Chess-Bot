import pygame
import math
import random
import time
import copy

# assigns constants

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BROWN = (244, 164, 96)
DARK_BROWN = (139, 69, 19)
FOREST = (50, 205, 50)
RED = (212, 0, 0)
SKY = (123, 211, 247)
PLAYER_COLORS = (WHITE, BLACK)

HUMAN = -1
EMPTY = 0
CPU = 1
OUT_OF_BOUNDS = 2

# converts a given x or y coordinate to the x or y value of the cell it is in

def roundCell(coordinate_tuple):
    return (math.floor(coordinate_tuple[0] / 100), math.floor(coordinate_tuple[1] / 100))

class Pawn:
    def __init__(self, side):
        self.side = side
        self.moved = False
        self.icon = pygame.image.load("pawn.png")
        self.value = 1
    def generateMoves(self, board, coordinates):
        x, y = coordinates
        moves = []
        space = (x, y + self.side)
        if board.getSide(space) == EMPTY:
            moves.append(space)
            if self.moved == False:
                space = (x, y + (self.side * 2))
                if board.getSide(space) == EMPTY:
                    moves.append(space)
        for i in range(-1, 3, 2):
            space = (x + i, y + self.side)
            if board.getSide(space) == self.side * -1:
                moves.append(space)
        return moves


class Knight:
    def __init__(self, side):
        self.side = side
        self.moved = False
        self.icon = pygame.image.load("knight.png")
        self.value = 3
    def generateMoves(self, board, coordinates):
        x, y = coordinates
        moves = []
        for i in range(-1, 3, 2):
            for j in range(-2, 6, 4):
                if board.getSide((x + i, y + j)) in [self.side * -1, EMPTY]:
                    moves.append((x + i, y + j))
        for i in range(-2, 6, 4):
            for j in range(-1, 3, 2):
                if board.getSide((x + i, y + j)) in [self.side * -1, EMPTY]:
                    moves.append((x + i, y + j))
        return moves

class Rook:
    def __init__(self, side):
        self.side = side
        self.moved = False
        self.icon = pygame.image.load("rook.png")
        self.value = 4
    def generateMoves(self, board, coordinates):
        x, y = coordinates
        moves = []
        for i in range(4):
            for j in range(1, 8):
                space = [(x - j, y), (x + j, y), (x, y - j), (x, y + j)][i]
                side = board.getSide(space)
                if side in [OUT_OF_BOUNDS, self.side]:
                    break
                else:
                    moves.append(space)
                    if side == self.side * -1:
                        break
        return moves

class Bishop:
    def __init__(self, side):
        self.side = side
        self.moved = False
        self.icon = pygame.image.load("bishop.png")
        self.value = 3.5
    def generateMoves(self, board, coordinates):
        x, y = coordinates
        moves = []
        for i in range(4):
            for j in range(1, 8):
                space = [(x - j, y - j), (x - j, y + j), (x + j, y - j), (x + j, y + j)][i]
                side = board.getSide(space)
                if side in [OUT_OF_BOUNDS, self.side]:
                    break
                moves.append(space)
                if side == self.side * -1:
                    break
        return moves

class Queen:
    def __init__(self, side):
        self.side = side
        self.moved = False
        self.icon = pygame.image.load("queen.png")
        self.value = 9
    def generateMoves(self, board, coordinates):
        x, y = coordinates
        moves = []
        for i in range(2):
            for j in range(4):
                for k in range(1, 8):
                    space = [[(x - k, y), (x + k, y), (x, y - k), (x, y + k)], [(x - k, y - k), (x - k, y + k), (x + k, y - k), (x + k, y + k)]][i][j]
                    side = board.getSide(space)
                    if side in [OUT_OF_BOUNDS, self.side]:
                        break
                    moves.append(space)
                    if side == self.side * -1:
                        break
        return moves

class King:
    def __init__(self, side):
        self.side = side
        self.moved = False
        self.icon = pygame.image.load("king.png")
        self.value = 1000
    def generateMoves(self, board, coordinates):
        x, y = coordinates
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and board.getSide((x + i, y + j)) not in [self.side, OUT_OF_BOUNDS]:
                    moves.append((x + i, y + j))
        return moves

class Board:
    def __init__(self, grid, turn):
        self.grid = grid
        self.selected = None
        self.turn = turn
        self.highlight = []
    def draw(self, screen):
        # makes checkerboard pattern
        screen.fill(DARK_BROWN)
        for i in range(4):
            for j in range(4):
                for k in range(2):
                    pygame.draw.rect(screen, LIGHT_BROWN, (i * 200 + k * 100, j * 200 + k * 100, 100, 100))
        # shades in selected cell
        if self.selected != None:
            pygame.draw.rect(screen, SKY, (self.selected[0] * 100, self.selected[1] * 100, 100, 100))
            for cell in self.grid[self.selected[1]][self.selected[0]].generateMoves(self, self.selected):
                if self.getSide(cell) == EMPTY:
                    pygame.draw.rect(screen, FOREST, (cell[0] * 100, cell[1] * 100, 100, 100))
                else:
                    pygame.draw.rect(screen, RED, (cell[0] * 100, cell[1] * 100, 100, 100))
        for cell in self.highlight:
            side = self.getSide(cell)
            if side == self.turn:
                color = SKY
            elif side == self.turn * -1:
                color = RED
            else:
                color = FOREST
            pygame.draw.rect(screen, color, (cell[0] * 100, cell[1] * 100, 100, 100))
        # fills in pieces
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] != None:
                    screen.blit(self.grid[i][j].icon, (j * 100 + 18, i * 100 + 18))
                    # draws purple or orange square next to the pieces to indicate side
                    pygame.draw.rect(screen, PLAYER_COLORS[self.grid[i][j].side == 1], (j * 100 + 85, i * 100, 15, 15))

    # returns the value of the player who the piece belongs to
    def getSide(self, coordinates):
        x, y = coordinates
        if not (0 <= x <= 7 and 0 <= y <= 7):
            return OUT_OF_BOUNDS
        if self.grid[y][x] == None:
            return EMPTY
        return self.grid[y][x].side

    # changes the state of the board to reflect a move
    def move(self, origin, destination, change_state = True):
        self.grid[destination[1]][destination[0]] = self.grid[origin[1]][origin[0]]
        self.grid[origin[1]][origin[0]] = None
        if change_state:
            self.grid[destination[1]][destination[0]].moved = True

    # generates all moves for the board in the form (origin, destination), where origin and destination are tuples
    def generateMoves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.getSide((j, i)) == self.turn:
                    moves += [((j, i), x) for x in self.grid[i][j].generateMoves(self, (j, i))]
        return moves

    # returns a copy of the board where a certain move has taken place. this is used to calculate future moves
    def generateNewBoard(self, move):
        new_board = Board([list(row) for row in self.grid], -self.turn)
        new_board.move(move[0], move[1], False)
        return new_board

class Node:
    def __init__(self, board, move = None, value = 0):
        self.board = board
        self.value = value
        self.children = []
        self.move = move

    # this function generates all possible boards up to a certain number of moves away from the start
    # for every extra generation, the number of boards should increase by 20-60x
    def populate(self, generations, initial):
        global num_boards
        if generations > 0:
            total_moves = self.board.generateMoves()
            num_boards += len(total_moves)
            for move in total_moves:
                origin, destination = move
                if generations == initial:
                    self.board.highlight = [origin, destination]
                    self.board.draw(screen)
                    pygame.display.flip()
                    self.board.highlight = []
                side = self.board.getSide(destination)

                # this calculates the new value of the board based on how the move changes things
                # this was added to speed up the process significantly, as it took a lot of time
                # to compute the value of every board as it was generated
                value_change = 0
                if side != EMPTY:
                    value_change = -side * self.board.grid[destination[1]][destination[0]].value
                b = time.time()
                new_board = self.board.generateNewBoard(move)
                new_node = Node(new_board, move, self.value + value_change)
                new_node.populate(generations - 1, initial)
                self.children.append(new_node)

    # this function calculates the min-max algorithm to choose the best move to play
    def propagate(self):
        if self.children == []:
            return (self.value, self.move)
        propagations = [child.propagate() for child in self.children]
        if self.board.turn == HUMAN:
            min_propagation = min(propagations, key = lambda x:x[0])
            return (min_propagation[0], self.move)
        max_propagation = max(propagations, key = lambda x:x[0])
        return (max_propagation[0], self.move)

pygame.init()
pygame.display.set_caption("Chess AI")
screen = pygame.display.set_mode((800, 800))

# assigns pieces to the chessboard

starting_grid = [
    [Rook(CPU),   Knight(CPU),   Bishop(CPU),   Queen(CPU),   King(CPU),   Bishop(CPU),   Knight(CPU),   Rook(CPU)],
    [Pawn(CPU),   Pawn(CPU),     Pawn(CPU),     Pawn(CPU),    Pawn(CPU),   Pawn(CPU),     Pawn(CPU),     Pawn(CPU)],
    [None,        None,          None,          None,         None,        None,          None,          None],
    [None,        None,          None,          None,         None,        None,          None,          None],
    [None,        None,          None,          None,         None,        None,          None,          None],
    [None,        None,          None,          None,         None,        None,          None,          None],
    [Pawn(HUMAN), Pawn(HUMAN),   Pawn(HUMAN),   Pawn(HUMAN),  Pawn(HUMAN), Pawn(HUMAN),   Pawn(HUMAN),   Pawn(HUMAN)],
    [Rook(HUMAN), Knight(HUMAN), Bishop(HUMAN), Queen(HUMAN), King(HUMAN), Bishop(HUMAN), Knight(HUMAN), Rook(HUMAN)]
]

board = Board(starting_grid, HUMAN)

board.draw(screen)
pygame.display.flip()

running = True

while running:
    if board.turn == HUMAN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                cell = roundCell(pygame.mouse.get_pos())
                if board.getSide(cell) == HUMAN and cell != board.selected:
                    board.selected = cell
                elif board.selected != None:
                    if cell in board.grid[board.selected[1]][board.selected[0]].generateMoves(board, board.selected):
                        board.move(board.selected, cell)
                        board.turn *= -1 # changes sides
                    board.selected = None
    else:
        start = time.time()
        num_boards = 0
        node = Node(board)
        difficulty = 3 # changing this number changes the depth at which the bot can look ahead (+1 makes it take longer by a factor of 20, 4 is a good value in the middle)
        node.populate(difficulty, difficulty)
        # creates a list of all the next moves it can take, sorted by their effectiveness
        best_moves = sorted([child.propagate() for child in node.children], reverse = True, key = lambda x:x[0])
        # if multiple moves are tied for best, it chooses a random one
        best_value = best_moves[0][0]
        top_moves = [move for move in best_moves if move[0] == best_value]
        random.shuffle(top_moves)
        best_move = top_moves[0][1]

        # moves the board accordingly and passes control back to the player
        print("Moved {} to {} in {} seconds. ({} possibilities analyzed)".format(best_move[0], best_move[1], round(time.time() - start, 2), num_boards))
        board.move(best_move[0], best_move[1])
        board.turn *= -1
    board.draw(screen)
    pygame.display.flip()
    black_king = False
    white_king = False
    for row in board.grid:
        for piece in row:
            if isinstance(piece, King):
                if piece.side == 1:
                    black_king = True
                else:
                    white_king = True
    if not black_king:
        print("White wins!")
        running = False
    if not white_king:
        print("Black wins!")
        running = False
