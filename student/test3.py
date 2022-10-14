import random
import time

def main():
    size=(6, 6)
    grid=get_grid("IBBxooIooLDDJAALooJoKEEMFFKooMGGHHHM", size)
    cars=get_cars(grid, size)
    n_cars=len(cars)
    print_grid(grid)
    start=time.time()
    for i in range(1000000):
        
        idx, direction=random.choice(movable_cars1(n_cars, cars, size, grid))
        car=cars[idx]

        # car, direction=random.choice(movable_cars2(cars, size, grid))

        move_car(car, direction, grid)

    end=time.time()
    print(f"Time: {end-start}")
    print_grid(grid)

def main2():
    print()
    with open("levels.txt", "r") as f:
        for line in f:
            line= line.split(" ")

            level = 57

            if level != 0 and level != int(line[0]):
                continue
            
            size=(6,6)
            grid=get_grid(line[1], size)
            cars=get_cars(grid, size)
            
            print(f"Level: {line[0]}")
            print_grid(grid)

            start=time.time()
            moves=0
            while grid[2][5] != 'A':
                car, direction=random.choice(movable_cars2(cars, size, grid))
                move_car(car, direction, grid)
                moves+=1
            end=time.time()

            print(f"Time: {end-start}")
            print(f"Moves: {moves}")
            print_grid(grid)


def movable_cars1(n_cars, cars, size, grid):
    movable=[]
    for i in range(n_cars):
        if cars[i][3]: # if car is horizontal
            if cars[i][1]-1 >= 0 and grid[cars[i][2]][cars[i][1]-1] == 'o':
                movable.append((i, 0)) # 0 = left
            if cars[i][1]+cars[i][4] < size[0] and grid[cars[i][2]][cars[i][1]+cars[i][4]] == 'o':
                movable.append((i, 1)) # 1 = right
        else: # if car is vertical
            if cars[i][2]-1 >= 0 and grid[cars[i][2]-1][cars[i][1]] == 'o':
                movable.append((i, 2)) # 2 = up
            if cars[i][2]+cars[i][4] < size[1] and grid[cars[i][2]+cars[i][4]][cars[i][1]] == 'o':
                movable.append((i, 3)) # 3 = down
    return movable

def movable_cars2(cars, size, grid):
    movable=[]
    for car in cars:
        if car[3]: # if car is horizontal
            if car[1]-1 >= 0 and grid[car[2]][car[1]-1] == 'o':
                movable.append((car, 0)) # 0 = left
            if car[1]+car[4] < size[0] and grid[car[2]][car[1]+car[4]] == 'o':
                movable.append((car, 1)) # 1 = right
        else: # if car is vertical
            if car[2]-1 >= 0 and grid[car[2]-1][car[1]] == 'o':
                movable.append((car, 2)) # 2 = up
            if car[2]+car[4] < size[1] and grid[car[2]+car[4]][car[1]] == 'o':
                movable.append((car, 3)) # 3 = down
    return movable

def get_grid(str, size):
    """
    Get the grid from a string
    """
    return [[*str[i*size[0]:i*size[0]+size[0]]] for i in range(size[1])]

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
                        cars[grid[y][x]] = [x, y-1, 0, 2] # car is vertical
                    else:
                        cars[grid[y][x]][3] += 1 # car length is increased
                elif x-1 >= 0 and grid[y][x-1] == grid[y][x]:
                    if grid[y][x] not in cars:
                        cars[grid[y][x]] = [x-1, y, 1, 2] # car is horizontal
                    else:
                        cars[grid[y][x]][3] += 1 # car length is increased
    cars_ = [[i, *cars[i]] for i in cars]
    cars_.sort(key=lambda x: x[0])
    return cars_

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

def print_grid(grid):
    print()
    for i in grid:
        for j in i:
            print(j, end=' ')
        print()
    print()

if __name__ == "__main__":
    main2()