#!/usr/local/bin/python3

"""
Chris Johns (cjohns433@gmail.com), December 2024

Gobblet is a game for 2 players on a 4x4 grid.
Each player uses a set of pieces of one color, either black or white.
A player has 12 pieces, grouped into 3 sets of 4. The pieces in each set
are nested, like Russian dolls, and must be played in the order from
largest to smallest.

The game is an extension of traditional tic-tac-toe (noughts and crosses),
with the board being 4x4 instead of 3x3, and the pieces being of different sizes,
with the ability to move and cover or uncover already-played pieces.

Play consists of taking turns, with the objective being to get 4 pieces
of your color in a row, horizontally, vertically, or diagonally. The first
player to do so wins the game.

A turn consists of either:
 - Placing a piece not currently in play onto the board on an empty square, or
 - Placing a piece not currently in play onto the board over a smaller piece of either color, or
 - Picking up a piece of your own color from the board and placing it on an empty square, or
 - Picking up a piece of your own color from the board and placing it over a smaller piece of either color

The game ends when all squares are filled, or a line of 4 of one color exists.
If a line of 4 exists, the player using that color is the winner.
"""

"""
Outline of algorithm:

 - Initialize empty board and player piece sets
 - Until all squares are full or a line of 4 exists, alternate players:
   - Display current board with only outermost pieces shown
   - Display remaining player piece stacks
   - Request move, either piece size (1-4) to add, or piece (x/y) to move, and x/y of destination
   - Validate move
   - Update board and player's remaining pieces
   - A player wins if a line of 4 pieces of the players color exists
   - If true, output appropriate message and stop
"""

"""
How should the board be displayed in ASCII on a terminal window?

 - Use traditional X and O symbols
 - To show piece sizes, use a 2x2 grid of X or O to show sizes 1-4
 - Empty square has no pieces shown
 - Grid is delimited by + (corner), - (horizontal) and | (vertical), e.g.
 - Grid squares are identified by two letters - horizontal/vertical
 - Players' remaining pieces should be shown below the board with the largest
   piece in each of the 3 stacks, such as: P1: [4, 2, 1]

  +----+----+----+----+
  | XX | OO |    |    |
D | XX | OO |    |    |
  +----+----+----+----+
  |    |    |    |    |
C |    |    |    |    |
  +----+----+----+----+
  |    | OO | OO | XX |
B |    | O  |    | X  |
  +----+----+----+----+
  |    |    | X  | XX |
A |    |    |    |    |
  +----+----+----+----+
    A    B    C    D

P1: [4, 2, 1]
P2: [3, 3, 0]
"""

"""
How is a move validated?

 - Has a piece size in the range [1..4] been specified, and
   does the player have such a piece available as the largest in a stack, or
 - Has a source co-ordinate XY been specified, where X and Y are in the set [A..D], and
   does a piece of the player's color exist at that location
 - And: has a destination co-ordinate XY been specified, and is that
   square empty or does it contain a piece of either color with a size
   less than the piece being moved
"""

import random
import copy
from operator import itemgetter

class Gobblet:

    def __init__(self):
        # Board is a square array, each element of which is an array of 4 pieces, where
        # each piece has a size 1-4 and color (1 or 2). Board starts out empty.
        #self.board = [ [ [0, 1, 2, 1] for _ in range(4)] for _ in range(4)]
        #self.board = [ [ [0, 0, 0, 0], [0, 0, 0, 1], [0, 2, 2, 2], [1, 2, 1, 2] ],
        #              [ [0, 0, 0, 0], [0, 0, 0, 2], [0, 1, 0, 0], [1, 0, 0, 0] ],
        #              [ [0, 1, 2, 1], [1, 2, 1, 2], [0, 0, 0, 0], [2, 2, 1, 0] ],
        #              [ [1, 2, 1, 1], [0, 0, 0, 1], [0, 2, 0, 0], [1, 0, 0, 0] ] ]
        self.board = [ [ [0, 0, 0, 0] for _ in range(4)] for _ in range(4)]
        self.player_stacks = [ [ 4, 4, 4 ], [ 4, 4, 4 ] ]
        self.player_chars = [ "X", "O" ]
        self.computer_players = [ False, False ]
        self.empty_piece = "  "
        self.empty_row = "  |    |    |    |    |"
        self.row_labels = "DCBA"
        self.num_moves = 0
        self.huge_score = 1000000
        self.big_score = 10000

    def show_board(self):
        row1 = self.empty_row
        row2 = self.empty_row
        self.print_horiz_line()
        row_num = 0
        for row in reversed(self.board):
            col_num = 0
            for column in row:
                # column will be a list like [ 0, 2, 1, 2 ] where the first element
                # is the outermost piece of size 4, next of size 3, then size 2, and
                # finally size 1. A zero means no piece of that size exists in that square.
                square_is_empty = True
                for size in range(4):
                    if column[size] == 0:
                        continue
                    piece_row1 = self.gen_row1(size, column[size])
                    piece_row2 = self.gen_row2(size, column[size])
                    # Replace 2 chars of row1 and row2 with chars reflecting what's visible
                    start_index = 4 + 5 * col_num
                    row1 = row1[0:start_index] + piece_row1 + row1[start_index+2:]
                    row2 = row2[0:start_index] + piece_row2 + row2[start_index+2:]
                    square_is_empty = False
                    break
                if square_is_empty:
                    start_index = 4 + 5 * col_num
                    row1 = row1[0:start_index] + self.empty_piece + row1[start_index+2:]
                    row2 = row2[0:start_index] + self.empty_piece + row2[start_index+2:]
                col_num += 1
            # Add row label
            row2 = self.row_labels[row_num:row_num+1] + row2[1:]
            print(row1)
            print(row2)
            self.print_horiz_line()
            row_num += 1
        self.print_horiz_labels()
        print()
        for player in range(2):
            print(f"Player {player + 1} ({self.player_chars[player]}) Stacks: {self.player_stacks[player]}")
        print()

    def gen_row1(self, size, player):
        char = self.player_chars[player - 1]
        match size:
            case 0: # biggest piece
                return char + char
            case 1:
                return char + char
            case 2:
                return char + char
            case 3: # smallest piece
                return char + " "

    def gen_row2(self, size, player):
        char = self.player_chars[player - 1]
        match size:
            case 0: # biggest piece
                return char + char
            case 1:
                return char + " "
            case 2:
                return "  "
            case 3: # smallest piece
                return "  "

    def print_horiz_line(self):
        print("  +----+----+----+----+")

    def print_horiz_labels(self):
        print("    A    B    C    D")

    def get_outermost(self, square):
        for size in range(4):
            if square[size]:
                return square[size]

        return None

    def map_player(self, player):
        if player == 1:
            return -1
        else:
            return 1

    def is_a_winner(self, player):
        # Look for a row, column, or diagonal of one color
        # and if found, the player has won. Note that we look first for the
        # other player than the one who just had a turn, since uncovering a
        # piece resulting in the opponent having a line of 4 will lose the game
        # for the player whose turn it was.

        # Map current player 1 to value -1, player 2 to value 1
        player_val = self.map_player(player)

        # Look for rows first
        for row in range(4):
            row_total = 0
            for column in range(4):
                piece = self.get_outermost(self.board[row][column])
                if piece:
                    # Map player 1 to value -1, player 2 to value 1
                    row_total += self.map_player(piece)
            # Check other player first
            if row_total == -4 * player_val:
                return 3 - player
            elif row_total == 4 * player_val:
                return player

        # Look for columns next
        for column in range(4):
            column_total = 0
            for row in range(4):
                piece = self.get_outermost(self.board[row][column])
                if piece:
                    # Map player 1 to value -1, player 2 to value 1
                    column_total += self.map_player(piece)
            # Check other player first
            if column_total == -4 * player_val:
                return 3 - player
            elif column_total == 4 * player_val:
                return player

        # Finally, look for diagonals
        diag_total1 = 0
        diag_total2 = 0
        for diag in range(4):
            piece = self.get_outermost(self.board[diag][diag])
            if piece:
                diag_total1 += self.map_player(piece)
            piece = self.get_outermost(self.board[3 - diag][diag])
            if piece:
                diag_total2 += self.map_player(piece)

        # Check other player first
        if diag_total1 == -4 * player_val or diag_total2 == -4 * player_val:
            return 3 - player
        elif diag_total1 == 4 * player_val or diag_total2 == 4 * player_val:
            return player

        return False

    def game_over(self, player):
        winner = self.is_a_winner(player)
        if winner:
            print(f"Player {winner} has won in {self.num_moves} moves!")
            return True
        return False

    def check_from(self, player, move):
        # A move must be a single digit specifying the size of a piece in
        # the player's stacks to add to the board, or a two character x/y
        # co-ordinate of a piece of the player's color to move.

        if len(move) == 1:
            size = int(move)
            if size < 1 or size > 4:
                print("Invalid move: size must be 1-4")
                return None
            # Make sure player has an outermost piece of that size
            if size not in self.player_stacks[player - 1]:
                print(f"Invalid move: player {player} has no usable piece of size {size}")
                return None
            return size
        elif len(move) == 2:
            if move[0] not in self.row_labels or move[1] not in self.row_labels:
                print("Invalid move: characters must be A-D")
                return None
            # Make sure there is a piece of the player's color at the grid location
            x = ord(move[0]) - ord("A")
            y = ord(move[1]) - ord("A")
            for i in range(4):
                size = self.board[x][y][i]
                if size == 0:
                    continue
                if player != size:
                    print("Invalid move: player does not have a piece at that location")
                    return None
                else:
                    return 4 - i
            print("Invalid move: player does not have a piece at that location")
            return None

        else:
            print("Invalid move: expected size 1-4 or 2-character grid co-ordinate")
            return None

    def check_to(self, player, size, dest):
        if len(dest) != 2:
            print("Invalid move: expected 2 characters")
            return False
        if dest[0] not in self.row_labels or dest[1] not in self.row_labels:
            print("Invalid move: destination characters must be A-D")
            return False

        # Check that piece of size 'size' can be placed at 'dest',
        # which means that no piece of equal or larger size exists there.
        dx = ord(dest[0]) - ord("A")
        dy = ord(dest[1]) - ord("A")
        for i in range(size, 5):
            if self.board[dx][dy][4 - i]:
                print("Invalid move: destination contains a piece of the same size or larger")
                return False

        return True

    def get_legal_destinations(self, player, size):
        # Look at each board square and determine if it contains nothing,
        # or as its largest piece, a piece smaller than 'size'. If so, it's a legal
        # destination square for the move being considered.

        sizeidx = 4 - size
        destinations = []

        for rowidx, row in enumerate(self.board):
            rowname = chr(ord("A") + rowidx)
            for colidx, column in enumerate(row):
                colname = chr(ord("A") + colidx)
                square_allowed = True
                for slot in range(0, sizeidx + 1):
                    #print(f"XXX: size {size} rowname {rowname} colname {colname} slot {slot} column[slot] {column[slot]}")
                    if column[slot] != 0:
                        square_allowed = False
                        break
                if square_allowed:
                    dest = rowname + colname
                    #print(f"Adding {dest} to allowed destinations")
                    destinations.append(dest)

        return destinations

    def get_legal_moves(self, player):
        # Generate all legal moves based on the current board and stack states
        # for the given player, by first looking at adding pieces to the board,
        # and then by moving the player's pieces that are already on the board.
        # A 'move' consists of a size/dest pair for a new piece, or a src/dest
        # pair for an already-played piece.
        moves = []

        for size in self.player_stacks[player - 1]:
            if size == 0:
                continue
            destinations = self.get_legal_destinations(player, size)
            if not destinations:
                continue
            for dest in destinations:
                move = [str(size), dest, 0]
                moves.append(move)

        for rowidx, row in enumerate(self.board):
            rowname = chr(ord("A") + rowidx)
            for colidx, column in enumerate(row):
                colname = chr(ord("A") + colidx)
                for slot in range(4):
                    #print(f"glm: player {player} rowname {rowname} colname {colname} slot {slot} column[slot] {column[slot]}")
                    if column[slot] == 0:
                        continue
                    if column[slot] != player:
                        break
                    size = 4 - slot
                    destinations = self.get_legal_destinations(player, size)
                    if not destinations:
                        continue
                    for dest in destinations:
                        dx = ord(dest[0]) - ord("A")
                        dy = ord(dest[1]) - ord("A")
                        # Skip no-op moves where the destination is the source
                        if dx == colidx and dy == rowidx:
                            continue
                        move = [rowname + colname, dest, 0]
                        moves.append(move)

        #print(f"glm: {moves}")
        return moves

    def evaluate_board(self, player, board):
        # Look for a row, column, or diagonal of one color,
        # and maintain a max score in the order:
        #   opponent: 4 in a line - huge negative score
        #   player:   4 in a line - huge positive score
        #   opponent: 3 in a line and other empty - big negative score
        #   player:   3 in a line and other empty - big positive score
        #   anything else: random positive score up to half of 'big'
        #
        # Note that we look first for the
        # other player than the one who just had a turn, since uncovering a
        # piece resulting in the opponent having a line of 4 will lose the game
        # for the player whose turn it was.

        # Map current player 1 to value -1, player 2 to value 1
        player_val = self.map_player(player)
        current_score = 0

        # Look for rows first
        for row in range(4):
            row_total = 0
            row_empty_total = 0
            for column in range(4):
                piece = self.get_outermost(board[row][column])
                if piece:
                    # Map player 1 to value -1, player 2 to value 1
                    row_total += self.map_player(piece)
                else:
                    # Count empty squares in this row
                    row_empty_total += 1
            # Check other player first
            if row_total == -4 * player_val:
                return -self.huge_score
            elif row_total == 4 * player_val:
                return self.huge_score
            elif row_total == -3 * player_val and row_empty_total == 1:
                current_score = -self.big_score
            elif row_total == 3 * player_val and row_empty_total == 1:
                current_score = self.big_score

        # Look for columns next
        for column in range(4):
            column_total = 0
            column_empty_total = 0
            for row in range(4):
                piece = self.get_outermost(board[row][column])
                if piece:
                    # Map player 1 to value -1, player 2 to value 1
                    column_total += self.map_player(piece)
                else:
                    # Count empty squares in this column
                    column_empty_total += 1
            # Check other player first
            if column_total == -4 * player_val:
                return -self.huge_score
            elif column_total == 4 * player_val:
                return self.huge_score
            elif column_total == -3 * player_val and column_empty_total == 1:
                current_score = -self.big_score
            elif column_total == 3 * player_val and column_empty_total == 1:
                current_score = self.big_score

        # Finally, look for diagonals
        diag_total1 = 0
        diag_empty_total1 = 0
        diag_total2 = 0
        diag_empty_total2 = 0
        for diag in range(4):
            piece = self.get_outermost(board[diag][diag])
            if piece:
                diag_total1 += self.map_player(piece)
            else:
                diag_empty_total1 += 1
            piece = self.get_outermost(board[3 - diag][diag])
            if piece:
                diag_total2 += self.map_player(piece)
            else:
                diag_empty_total2 += 1

        # Check other player first
        if diag_total1 == -4 * player_val or diag_total2 == -4 * player_val:
            return -self.huge_score
        elif diag_total1 == 4 * player_val or diag_total2 == 4 * player_val:
            return self.huge_score
        elif diag_total1 == -3 * player_val and diag_empty_total1 == 1:
            current_score = -self.huge_score
        elif diag_total2 == -3 * player_val and diag_empty_total2 == 1:
            current_score = -self.huge_score
        elif diag_total1 == 3 * player_val and diag_empty_total1 == 1:
            current_score = self.huge_score
        elif diag_total2 == 3 * player_val and diag_empty_total2 == 1:
            current_score = self.huge_score

        if current_score:
            return current_score
        else:
            return random.randrange(self.big_score)

    def choose_best(self, player, moves):
        for m in moves:
            move = m[0]
            dest = m[1]
            tmp_board = copy.deepcopy(self.board)
            tmp_stacks = copy.deepcopy(self.player_stacks)
            tmp_board = self.do_move(tmp_board, tmp_stacks, player, move, dest)
            m[2] = self.evaluate_board(player, tmp_board)
        moves = sorted(moves, key=itemgetter(2), reverse=True)
        #print(f"cb: {moves}")

        return moves[0]

    def generate_move(self, player):
        moves = self.get_legal_moves(player)
        move = self.choose_best(player, moves)
        move[0] = move[0][::-1]
        move[1] = move[1][::-1]
        print(f"Computer player {player} move is: {move}")
        move[0] = move[0][::-1]
        move[1] = move[1][::-1]
        return move[0], move[1]

    def get_move(self, player):
        while True:
            move = input("Enter piece size (1-4) to add or location (XY) to move: ")
            move = move[::-1]
            size = self.check_from(player, move)
            if not size:
                continue
            dest = input("Enter destination location (XY): ")
            dest = dest[::-1]
            if self.check_to(player, size, dest):
                return move, dest
            print()

    def do_move(self, board, stacks, player, move, dest):
        dx = ord(dest[0]) - ord("A")
        dy = ord(dest[1]) - ord("A")

        if len(move) == 1:
            # Remove piece of size 'move' from player stack and place on first
            # empty piece stack position in board location 'dest'
            move = int(move)
            found = -1
            for stack in range(3):
                if stacks[player - 1][stack] == move:
                    found = stack
                    break
            if found == -1:
                print("Error: player has no usable piece of that size")
            else:
                if board[dx][dy][4 - move] != 0:
                    print("Error: destination already has a piece of that size")
                    return False

                # Sizes are 4, 3, 2, 1, so decrement size in stack we took from
                stacks[player - 1][stack] -= 1
                # Now add player's piece to destination
                board[dx][dy][4 - move] = player
                return board
        else:
            # Remove piece from board stack in location 'move' and place on first
            # empty piece stack position in board location 'dest'
            x = ord(move[0]) - ord("A")
            y = ord(move[1]) - ord("A")
            for size in range(4):
                if board[x][y][size] == 0:
                    continue
                board[x][y][size] = 0
                board[dx][dy][size] = player
                break

        return board

    def get_computer_players(self):
        while True:
            num_humans = input("How many human players? (0-2) ")
            if len(num_humans) != 1:
                continue
            nh = ord(num_humans[0]) - ord("0")
            if nh >= 0 and nh <= 2:
                break
        match nh:
            case 0:
                self.computer_players = [ True, True ]
            case 1:
                self.computer_players = [ False, True ]
            case 2:
                self.computer_players = [ False, False ]

    def play(self):
        self.get_computer_players()
        player = 1
        self.show_board()
        while True:
            self.num_moves += 1
            print(f"Player {player} ({self.player_chars[player - 1]}) to move")
            if self.computer_players[player - 1]:
                move, dest = self.generate_move(player)
            else:
                move, dest = self.get_move(player)
            if not self.do_move(self.board, self.player_stacks, player, move, dest):
                print()
                continue
            self.show_board()
            if self.game_over(player):
                break
            player = 3 - player

gobblet = Gobblet()
gobblet.play()
