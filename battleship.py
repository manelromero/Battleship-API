from random import randint


def add_ship(ship_length):
    success = False
    while not success:
        # Horizontal or vertical?
        horizontal = True if randint(0, 1) == 0 else False
        # Start cell
        row = randint(0, 9) if horizontal else randint(0, 5)
        column = randint(0, 5) if horizontal else randint(0, 9)
        # Check free space for the ship
        free_space = True
        for length in xrange(-1, ship_length + 1):
            for width in xrange(-1, 2):
                if horizontal:
                    try:
                        value = board[row + width][column + length]
                        if value == 1:
                            free_space = False
                    except IndexError:
                        pass
                else:
                    try:
                        value = board[row + length][column + width]
                        if value == 1:
                            free_space = False
                    except IndexError:
                        pass
        # If there is free space, place the ship
        if free_space:
            board[row][column] = 1
            for l in xrange(1, ship_length):
                if horizontal:
                    board[row][column + l] = 1
                else:
                    board[row + l][column] = 1
            # success is now True so while loop stops
            success = True


# Generate the empty board
board = []
for row in xrange(0, 10):
    board.append([0] * 10)

# Add battleships
add_ship(5)
add_ship(4)
add_ship(3)
add_ship(2)
add_ship(2)
add_ship(1)
add_ship(1)
print board
