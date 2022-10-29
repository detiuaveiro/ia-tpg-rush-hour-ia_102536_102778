from math import dist

def get_path(node):
    """
    Get the path to the root node
    """
    if node[0] is None:
        return []
    return get_path(node[0]) + [node[3]]


def test_win(grid):
    """
    Check if the game is won
    """
    return grid[2][5] == 'A'


def get_grid(str, size):
    """
    Get the grid from a string
    """
    return [[*str[i*size[0]:i*size[0]+size[0]]] for i in range(size[1])]


def get_str(grid):
    """
    Get the string from the grid
    """
    return ''.join([''.join(i) for i in grid])


def print_grid(grid):
    """
    Print the grid
    """
    print()
    for i in grid:
        for j in i:
            print(j, end=' ')
        print()
    print()


def get_cars(grid, size):
    """
    Get the cars from grid
    """
    cars = {}
    for y in range(size[1]):
        for x in range(size[0]):
            if grid[y][x] != 'o' and grid[y][x] != 'x':
                if y-1 >= 0 and grid[y-1][x] == grid[y][x]:
                    if grid[y][x] not in cars:
                        cars[grid[y][x]] = [x, y-1, 'v', 2]     # car is vertical
                    else:
                        cars[grid[y][x]][3] += 1                # car length is increased
                elif x-1 >= 0 and grid[y][x-1] == grid[y][x]:
                    if grid[y][x] not in cars:
                        cars[grid[y][x]] = [x-1, y, 'h', 2]     # car is horizontal
                    else:
                        cars[grid[y][x]][3] += 1                # car length is increased
    cars_ = [[i, *cars[i]] for i in cars]
    cars_.sort(key=lambda x: x[0])
    return cars_


def move_car(car, direction, grid):
    """
    Move the car to a given direction
    """
    letter, x, y, _, length = car
    match direction:
        case 'a':                       # left
            grid[y][x-1] = letter
            grid[y][x+length-1] = 'o'
        case 'd':                       # right
            grid[y][x+length] = letter
            grid[y][x] = 'o'
        case 'w':                       # up
            grid[y-1][x] = letter
            grid[y+length-1][x] = 'o'
        case 's':                       # down
            grid[y+length][x] = letter
            grid[y][x] = 'o'


def get_new_nodes(parent, size):
    """
    Calculate new nodes
    """
    grid, cars, cost = parent[1], parent[2], parent[4]
    for idx, car in enumerate(cars):
        letter, x, y, orientation, length = car
        match orientation:
            case 'h':   # horizontal

                if x > 0 and grid[y][x-1] == 'o':                   # move left

                    new_grid = [[*i] for i in grid] # copy the grid
                    move_car(car, 'a', new_grid)
                    new_cars = (*cars[:idx] , (letter, x-1, y, orientation, length) , *cars[idx+1:]) # copy the cars with the change
                    yield (parent, new_grid, new_cars, (letter, 'a'), cost+1)

                if x+length < size[0] and grid[y][x+length] == 'o': # move right

                    new_grid = [[*i] for i in grid] # copy the grid
                    move_car(car, 'd', new_grid)
                    new_cars = (*cars[:idx] , (letter, x+1, y, orientation, length) , *cars[idx+1:]) # copy the cars with the change
                    yield (parent, new_grid, new_cars, (letter, 'd'), cost+1)

            case 'v':   # vertical

                if y > 0 and grid[y-1][x] == 'o':                   # move up

                    new_grid = [[*i] for i in grid] # copy the grid
                    move_car(car, 'w', new_grid)
                    new_cars = (*cars[:idx] , (letter, x, y-1, orientation, length) , *cars[idx+1:]) # copy the cars with the change
                    yield (parent, new_grid, new_cars, (letter, 'w'), cost+1)

                if y+length < size[1] and grid[y+length][x] == 'o': # move down

                    new_grid = [[*i] for i in grid] # copy the grid
                    move_car(car, 's', new_grid)
                    new_cars = (*cars[:idx] , (letter, x, y+1, orientation, length) , *cars[idx+1:]) # copy the cars with the change
                    yield (parent, new_grid, new_cars, (letter, 's'), cost+1)


def cost(cursor, selected, car, direction):

    letter, x, y, orientation, length = car

    if selected == letter:
        return 1

    x_,y_ = x,y
    distance = 99
    match orientation:
        case 'h':   # horizontal
            for i in range(length):
                dist = abs(x+i - cursor[0]) + abs(y - cursor[1])
                if dist < distance:
                    distance = dist
                    x_ += 1
        case 'v':   # vertical
            for i in range(length):
                dist = abs(x - cursor[0]) + abs(y+i - cursor[1])
                if dist < distance:
                    distance = dist
                    y_ += 1
    
    match direction:
        case 'a':   # left
            x_ -= 1
        case 'd':   # right
            x_ += 1
        case 'w':   # up
            y_ -= 1
        case 's':   # down
            y_ += 1

    cursor[0] = x_
    cursor[1] = y_
    
    return distance + 3

    
def cost2(cursor, selected, car):
    if selected == car[0]:
        return 1

    return abs(cursor[0] - car[1]) + abs(cursor[1] - car[2]) + 3

# if self.action is None:
        #     return 2

        # letter = self.action[0]
        # car, = [car for car in self.cars if car[0] == letter]

        # if letter == new_car[0]:
        #     return 1

        # return abs(car[1] - new_car[1]) + abs(car[2] - new_car[2]) + 3

    