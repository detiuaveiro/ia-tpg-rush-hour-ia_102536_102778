import random
import time
import sys

state = {'dimensions': [6, 6], 'level': 1, 'grid': '1 oooooooooooooAAooooooooooooooooooooo 5', 'score': -605, 'game_speed': 10, 'cursor': [3, 3], 'selected': '', 'player': 'leo'}

grid= state['grid'].split(' ')[1]

grid= 'oxoCCCHoDDDMHAAKLMIEEKLMIoJFFoGGJooo'

size = state['dimensions']


def get_map(grid):
    return [[*grid[i*size[0]:i*size[0]+size[0]]] for i in range(size[1])]


def get_cars(map):
    cars = {}
    for y in range(size[1]):
        for x in range(size[0]):

            if map[y][x] != 'o' and map[y][x] != 'x':
                if y-1 >= 0 and map[y-1][x] == map[y][x]:
                    if map[y][x] not in cars:
                        cars[map[y][x]] = [x, y-1, 'v', 2]
                    else:
                        cars[map[y][x]][3] += 1
                elif x-1 >= 0 and map[y][x-1] == map[y][x]:
                    if map[y][x] not in cars:
                        cars[map[y][x]] = [x-1, y, 'h', 2]
                    else:
                        cars[map[y][x]][3] += 1

    cars_ = []
    for i in cars:
        cars_.append([i, *cars[i]]) 
    # 'v' = vertical
    # 'h' = horizontal
    # [letter, x, y, direction, length]

    return cars_


def print_map(map):
    print()
    for i in map:
        for j in i:
            print(j, end='')
        print()
    print()


def change_map(map, x, y, char):
    map[y][x] = char
    return map



def movable_cars(cars, map):
    # car =['name', x, y, direction, length]
    movable = []
    for car in cars:
        if car[3] == 'h':
            if car[1]+car[4] < size[0] and map[car[2]][car[1]+car[4]] == 'o':
                movable.append((car,'r'))
            if car[1]-1 >= 0 and map[car[2]][car[1]-1] == 'o':
                movable.append((car,'l'))
        else:
            if car[2]+car[4] < size[1] and map[car[2]+car[4]][car[1]] == 'o':
                movable.append((car,'d'))
            if car[2]-1 >= 0 and map[car[2]-1][car[1]] == 'o':
                movable.append((car,'u'))

    return movable


def move_car(car, direction, map):
    # car =['name', x, y, direction, length]
    if direction == 'r':
        map[car[2]][car[1]+car[4]] = car[0]
        map[car[2]][car[1]] = 'o'
        car[1] += 1
    elif direction == 'l':
        map[car[2]][car[1]-1] = car[0]
        map[car[2]][car[1]+car[4]-1] = 'o'
        car[1] -= 1
    elif direction == 'd':
        map[car[2]+car[4]][car[1]] = car[0]
        map[car[2]][car[1]] = 'o'
        car[2] += 1
    else:
        map[car[2]-1][car[1]] = car[0]
        map[car[2]+car[4]-1][car[1]] = 'o'
        car[2] -= 1

map = get_map(grid)

cars = get_cars(map)

def lst_cp(lst):
    return [i.copy() for i in lst]

print_map(map)
# print(cars)

# movable = movable_cars(cars, map)

# for tup in movable:
#     print(tup[0][0], tup[1])
# print()

start = time.time()
for i in range(100000):
    tup = random.choice(movable_cars(cars, map))
    move_car(tup[0], tup[1], map)

end = time.time()
print(end-start)

print_map(map)

