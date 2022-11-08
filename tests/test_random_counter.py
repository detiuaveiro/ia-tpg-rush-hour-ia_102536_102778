import sys

sys.path.append('.')

from student.Functions import *
from student.RandomCounter import RandomCounter
import random

def main():
    size = 6
    
    grid_str = "IBBxooIooLDDJAALooJoKEEMFFKooMGGHHHM"
    path = [('M', 'w'), ('H', 'd'), ('K', 's'), ('E', 'a'), ('E', 'a'), ('L', 's'), ('D', 'a'), ('D', 'a'), ('D', 'a'), ('L', 'w'), ('M', 'w'), ('M', 'w'), ('E', 'd'), ('E', 'd'), ('E', 'd'), ('L', 's'), ('L', 's'), ('D', 'd'), ('A', 'd'), ('K', 'w'), ('D', 'd'), ('A', 'd'), ('K', 'w'), ('F', 'd'), ('J', 's'), ('I', 's'), ('K', 'w'), ('B', 'a'), ('K', 'w'), ('A', 'a'), ('A', 'a'), ('L', 'w'), ('F', 'd'), ('F', 'd'), ('F', 'd'), ('L', 's'), ('A', 'd'), ('A', 'd'), ('K', 's'), ('K', 's'), ('K', 's'), ('A', 'a'), ('K', 's'), ('A', 'a'), ('D', 'a'), ('D', 'a'), ('L', 'w'), ('L', 'w'), ('E', 'a'), ('M', 's'), ('F', 'a'), ('M', 's'), ('E', 'a'), ('E', 'a'), ('L', 's'), ('D', 'd'), ('D', 'd'), ('D', 'd'), ('L', 'w'), ('E', 'd'), ('E', 'd'), ('K', 'w'), ('G', 'd'), ('B', 'd'), ('I', 'w'), ('A', 'a'), ('K', 'w'), ('K', 'w'), ('E', 'a'), ('J', 's'), ('E', 'a'), ('E', 'a'), ('K', 's'), ('K', 's'), ('L', 's'), ('D', 'a'), ('M', 'w'), ('F', 'd'), ('A', 'd'), ('L', 's'), ('A', 'd'), ('A', 'd'), ('I', 's'), ('K', 'w'), ('B', 'a'), ('K', 'w'), ('K', 'w'), ('A', 'a'), ('A', 'a'), ('L', 'w'), ('F', 'a'), ('F', 'a'), ('M', 's'), ('F', 'a'), ('E', 'd'), ('L', 's'), ('J', 'w'), ('G', 'a'), ('H', 'a'), ('A', 'd'), ('M', 's'), ('A', 'd'), ('A', 'd')]
    rc = RandomCounter(path)

    grid = get_grid(grid_str, size)
    cars = get_cars(grid)

    cars_idx = {cars[i][0]: i for i in range(len(cars))}

    print("Path:", path)
    print("\nStarting grid:")

    num_rand_moves = 0

    while path:
        
        print_grid(grid)
        grid_str = ''.join([''.join(i) for i in grid])

        grid_cp = [[*i] for i in grid]
        cars_cp = [[*i] for i in cars]
        
        random_move = random.choice(movable_cars(cars_cp, size, grid_cp))
        move_car(grid_cp, random_move[0], random_move[1])
        print(f"Simulating random move: {random_move[0][0]} -> {random_move[1]}")
        num_rand_moves += 1
        print_grid(grid_cp)

        new_grid_str = ''.join([''.join(i) for i in grid_cp])
        res = rc.update_path(grid_str, new_grid_str, size)

        print(f"Fix worked: {res}")
        print()

        grid = [[*i] for i in grid_cp]
        cars = [[*i] for i in cars_cp]

        if not res or not path:
            break
        
        print(f"Remaining path: {path}")
        move = path.pop(0)

        car = cars[cars_idx[move[0]]]
        print(f"Simulating move: {move[0]} -> {move[1]}")
        move_car(grid, car, move[1])


    print("Final grid:")
    print_grid(grid)

    print(f"Number of random moves: {num_rand_moves}")



def movable_cars(cars, size, grid):
    movable=[]
    for car in cars:
        if car[3]=='h': # if car is horizontal
            if car[1]-1 >= 0 and grid[car[2]][car[1]-1] == 'o':
                movable.append((car, 'a')) # 0 = left
            if car[1]+car[4] < size and grid[car[2]][car[1]+car[4]] == 'o':
                movable.append((car, 'd')) # 1 = right
        else: # if car is vertical
            if car[2]-1 >= 0 and grid[car[2]-1][car[1]] == 'o':
                movable.append((car, 'w')) # 2 = up
            if car[2]+car[4] < size and grid[car[2]+car[4]][car[1]] == 'o':
                movable.append((car, 's')) # 3 = down
    return movable

if __name__ == "__main__":
    main()

