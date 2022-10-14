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


move_cursor = lambda x, y: [cursor[0]+x, cursor[1]+y]

all_actions=[]
for step in solution:
    actions=[]
    print_grid(grid)

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
    print(f"Position: {cursor}")
    print(f"Selected: {selected}")
    print(f"Target: {car[0]} to {moves[step[1]]}")
    print(f"Nearest square: {coords}\n")

    while coords != cursor:

        if selected != '' and selected != car[0]:
            actions.append(' ')

        elif coords[0] < cursor[0]:
            actions.append('A')
        elif coords[0] > cursor[0]:
            actions.append('D')
        elif coords[1] < cursor[1]:
            actions.append('W')
        elif coords[1] > cursor[1]:
            actions.append('S')

        match actions[-1]:
            case 'A':
                cursor = move_cursor(-1, 0)
            case 'D':
                cursor = move_cursor(1, 0)
            case 'W':
                cursor = move_cursor(0, -1)
            case 'S':
                cursor = move_cursor(0, 1)
            case ' ':
                selected = ''

    if selected == '':
        selected = car[0]
        actions.append(' ')

    
    selected = car[0]

    match step[1]:
        case 0:
            actions.append('A')
        case 1:
            actions.append('D')
        case 2:
            actions.append('W')
        case 3:
            actions.append('S')

    match actions[-1]:
            case 'A':
                cursor = move_cursor(-1, 0)
            case 'D':
                cursor = move_cursor(1, 0)
            case 'W':
                cursor = move_cursor(0, -1)
            case 'S':
                cursor = move_cursor(0, 1)

    print(f"ACTIONS: {actions}")

    move_car(car, step[1], grid)

    all_actions += actions
print(all_actions)






