
# car = ( letter, x, y, orientation, length )
# y = idx // size
# x = idx % size
# idx = y * size + x


def print_grid(grid):
    """
    Print grid
    """
    for i in range(len(grid)):
        for j in range(len(grid)):
            print(grid[i][j], end=' ')
        print()


def get_grid(str_, size):
        """
        Get grid
        """
        # convert board to 2D
        return [[*str_[i:i+size]] for i in range(0, len(str_), size)]


def get_cars(grid):
    """
    Get cars from grid
    """
    size = len(grid)
    # letter : [ x, y, orientation, length ]
    cars = {}
    # loop through grid
    for y in range(size):
        for x in range(size):
            letter = grid[y][x]
            # letter can be a car
            if letter != 'o' and letter != 'x':
                # car is horizontal
                if x + 1 < size and grid[y][x + 1] == letter:
                    # check if car is already in cars
                    if letter not in cars:
                        # add new car
                        cars[letter] = [x, y, 'h', 2]
                    else:
                        # increase car length
                        cars[letter][3] += 1
                # car is vertical
                elif y + 1 < size and grid[y + 1][x] == letter:
                    # check if car is already in cars
                    if letter not in cars:
                        # add new car
                        cars[letter] = [x, y, 'v', 2]
                    else:
                        # increase car length
                        cars[letter][3] += 1

    # convert cars to list and sort by letter
    # [[letter, x, y, orientation, length], ...]
    cars_ = [[i, *cars[i]] for i in cars]
    cars_.sort(key=lambda x: x[0])
    return cars_


def test_win(car, pos):
    """
    Check if the board is solved
    """
    return car[1] == pos


def get_path(node):
    """
    Get path from root to node
    """
    path = []
    while node.parent:
        path.insert(0, node.action)
        node = node.parent
    return path


def move_car(grid, car, direction):
    """
    Move the car and change the grid
    """
    letter, x, y, _, length = car

    # left
    if direction == 'a':
        # change grid
        grid[y][x-1] = letter
        grid[y][x+length-1] = 'o'
        # move car
        car[1] -= 1
    # right
    elif direction == 'd':
        # change grid
        grid[y][x+length] = letter
        grid[y][x] = 'o'
        # move car
        car[1] += 1
    # up
    elif direction == 'w':
        # change grid
        grid[y-1][x] = letter
        grid[y+length-1][x] = 'o'
        # move car
        car[2] -= 1
    # down
    else:
        # change grid
        grid[y+length][x] = letter
        grid[y][x] = 'o'
        # move car
        car[2] += 1


def nearest_coords(cursor, car):
    """
    Get nearest coords to cursor
    """
    _, x, y, orientation, length = car

    # horizontal
    if orientation == 'h':
        # left
        if cursor[0] < x:
            return [x, y]
        # right
        elif cursor[0] > x + length - 1:
            return [x + length - 1, y]
        # middle
        else:
            return [cursor[0], y]
    # vertical
    else:
        # up
        if cursor[1] < y:
            return [x, y]
        # down
        elif cursor[1] > y + length - 1:
            return [x, y + length - 1]
        # middle
        else:
            return [x, cursor[1]]
