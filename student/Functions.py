
# car = ( letter, x, y, orientation, length )

def print_board(board, size):
    """
    Print board
    """
    print()
    for i in range(size):
        for j in range(size):
            print(board[i * size + j], end=' ')
        print()
    print()


def get_cars(board, size):
    """
    Get cars from board
    """
    # letter : [x, y, orientation, length]
    cars = {}

    # loop through board
    for idx, letter in enumerate(board):
        
        # letter can be a car
        if letter != 'o' and letter != 'x':

            # car is horizontal
            if idx % size -1 >= 0 and board[idx-1] == letter:

                if letter not in cars:
                    # add new car
                    cars[letter] = [idx % size -1 , idx // size, 'h', 2]
                else:
                    # increase car length
                    cars[letter][3] += 1

            # car is vertical
            elif idx // size -1 >= 0 and board[idx-size] == letter:

                if letter not in cars:
                    # add new car
                    cars[letter] = [idx % size, idx // size -1, 'v', 2]
                else:
                    # increase car length
                    cars[letter][3] += 1

    # convert cars to list and sort by letter
    # [[letter, x, y, orientation, length], ...]
    cars_ = [[i, *cars[i]] for i in cars]
    cars_.sort(key=lambda x: x[0])
    return cars_


def move_car(board, car, direction, size):
    """
    Change the board with a car move
    """
    letter, x, y, _, length = car

    # left 
    if direction == 'a':  
        # change board  
        board[y * size + x - 1] = letter
        board[y * size + x + length - 1] = 'o'

    # right
    elif direction == 'd':  
        # change board
        board[y * size + x + length] = letter
        board[y * size + x] = 'o'

    # up
    elif direction == 'w': 
        # change board 
        board[(y - 1) * size + x] = letter
        board[(y + length - 1) * size + x] = 'o'

    # down
    elif direction == 's':  
        # change board
        board[(y + length) * size + x] = letter
        board[y * size + x] = 'o'


def test_win(node, pos):
    """
    Check if the board is solved
    """
    return node.cars[0][1] == pos


def get_path(node):
    """
    Get path from root to node
    """
    path = []
    while node.parent:
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path