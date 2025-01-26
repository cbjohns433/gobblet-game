<header>

# The Gobblet Game

Gobblet is a board game that was created and sold by Blue Orange games.
For details and additional links, see https://en.wikipedia.org/wiki/Gobblet.

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

</header>

## Running the code

The game code assumes that the Python 3 interpreter has been installed in
/usr/local/bin/python3. If your Python is in a different location, simply update
the first line of the file.

To run the game:

./gobblet.py

The game will then ask how many human player are to be playing (0-2), and for each
non-human player, the game implementation will make its own moves.

## Making a move

Before each move, the board is displayed, and the piece stacks of each player
are also shown. For example:

  +----+----+----+----+
  |    |    |    | OO |
D |    |    |    | OO |
  +----+----+----+----+
  |    | XX |    |    |
C |    | XX |    |    |
  +----+----+----+----+
  |    |    |    |    |
B |    |    |    |    |
  +----+----+----+----+
  |    |    | XX |    |
A |    |    | X  |    |
  +----+----+----+----+
    A    B    C    D

Player 1 (X) Stacks: [2, 4, 4]
Player 2 (O) Stacks: [3, 4, 4]

In this situation, player 2 (O) is the next to play, and can choose to place
a piece of size 3 or size 4 on the board, or move the piece at DD to another
board position, including covering the size 3 piece of player 1 at square CA.

Adding a piece from a stack of pieces requires specifying the size of piece
to be added (e.g. 3 or 4 in this case), and the destination square in XY
notation (e.g. BA, which would be the second square from the left on the
bottom row.

Moving an already-played piece requires the XY coordinates of the piece to
be moved (e.g. DD) and the XY coordinates of the destination square.
