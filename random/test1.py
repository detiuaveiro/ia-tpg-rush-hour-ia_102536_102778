from math import dist

def print_grid(grid):
    print()
    for i in grid:
        for j in i:
            print(j, end=' ')
        print()
    print()

def move_car(car, direction, grid):
    """
    Move the car to a given direction
    """
    match direction:
        case 0: # left
            grid[car[2]][car[1]-1] = car[0]
            grid[car[2]][car[1]+car[4]-1] = 'o'
            car[1] -= 1
        case 1: # right
            grid[car[2]][car[1]+car[4]] = car[0]
            grid[car[2]][car[1]] = 'o'
            car[1] += 1
        case 2: # up
            grid[car[2]-1][car[1]] = car[0]
            grid[car[2]+car[4]-1][car[1]] = 'o'
            car[2] -= 1
        case 3: # down
            grid[car[2]+car[4]][car[1]] = car[0]
            grid[car[2]][car[1]] = 'o'
            car[2] += 1

grid= [['o', 'o', 'B', 'o', 'o', 'o'], ['o', 'o', 'B', 'o', 'o', 'C'], ['A', 'A', 'B', 'o', 'o', 'C'], ['o', 'o', 'o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o', 'o', 'o']]

size=[6,6]

cursor = [3,3]

selected = ''

cars= [['A', 0, 2, 1, 2], ['B', 2, 0, 0, 3], ['C', 5, 1, 0, 2]]

solution= [(1, 3), (1, 3), (1, 3), (0, 1), (0, 1), (0, 1), (2, 2), (0, 1)]

keys= ('A', 'D', 'W', 'S')

moves= [ "Left", "Right", "Up", "Down"]


def get_action(cursor, selected, car, step, coords):
    """
    Get the action to move the car
    """

    keys = ('a', 'd', 'w', 's')

    if selected == car[0]:
        return keys[step[1]], True
    if selected != '':
        return ' ', False
    
    if cursor[0] > coords[0]:
        return 'a', False
    if cursor[0] < coords[0]:
        return 'd', False
    if cursor[1] > coords[1]:
        return 'w', False
    if cursor[1] < coords[1]:
        return 's', False

    return ' ', False


def actions(grid, cars, cursor, selected, solution):

    selected = selected
    all_actions = []
    for step in solution:
        car = cars[step[0]]
        dists =[]
        for square in range(car[4]):
            if car[3]:
                dists.append(dist([car[1]+square, car[2]], cursor))
            else:
                dists.append(dist([car[1], car[2]+square], cursor))
        dist_min = min(dists)
        square = dists.index(dist_min)
        coords = [car[1]+square, car[2]] if car[3] else [car[1], car[2]+square]

        print_grid(grid)
        print(f"Cursor: {cursor}")
        print(f"Selected: {selected}")
        print(f"Target car: {car[0]} at {coords}")

        actions = []
        done = False
        while not done:
            key, done = get_action(cursor, selected, car, step, coords)
            actions.append(key)
            selected = simulate(grid, car, cursor, selected, key)
        print(f"Actions: {actions}")
        all_actions+=actions
    return all_actions
        


def simulate(grid, car, cursor, selected, key):
    """
    Simulate the move of a car
    """
    if selected == car[0]:
        if key == 'a':
            move_car(car, 0, grid)
            cursor[0] -= 1
        if key == 'd':
            move_car(car, 1, grid)
            cursor[0] += 1
        if key == 'w':
            move_car(car, 2, grid)
            cursor[1] -= 1
        if key == 's':
            move_car(car, 3, grid)
            cursor[1] += 1
        return selected
    
    if key == 'a':
        cursor[0] -= 1
    if key == 'd':
        cursor[0] += 1
    if key == 'w':
        cursor[1] -= 1
    if key == 's':
        cursor[1] += 1
    if key == ' ':
        if selected == '':
            selected = car[0]
        else:
            selected = ''
    return selected

print(actions(grid, cars, cursor, selected, solution))

