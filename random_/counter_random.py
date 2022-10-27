
from Functions import *
import random

# car = ( letter, x, y, orientation, length )
# node = ( parent, grid, cars, action, cost )


def main():
    size = (6, 6)

    grid_str = "oooooHoxCCoHAAoGoooFoGoooFDDxooooooo"
    moves= [('H', 's'), ('H', 's'), ('H', 's'), ('C','d'), ('C','d'), ('G','w'),('G','w'),('A','d'), ('A','d'), ('A','d'), ('A','d')]


    grid = get_grid(grid_str, (6, 6))
    cars = get_cars(grid, (6, 6))

    cars_idx={cars[i][0]:i for i in range(len(cars))}

    print_grid(grid)
    # new_grid_str= "oooooHoxoCCHAAoGoooFoGoooFDDxooooooo" # changed C to right


    # if get_str(grid) != new_grid_str:
    #     print("Random move happened")
    #     print(detect_random(grid, new_grid_str, (6, 6)))
    #     print_grid(get_grid(new_grid_str, (6, 6)))


    #     print("Checking solution...")
    #     print(check_solution(grid, cars, moves, new_grid_str, (6, 6)))

    count=0

    while moves:
        count+=1
        move = moves.pop(0)
        car = cars[cars_idx[move[0]]]
    
        move_car(car, move[1], grid)
        match move[1]:
            case 'a': # left
                car[1]-=1
            case 'd': # right
                car[1]+=1
            case 'w': # up
                car[2]-=1
            case 's': # down
                car[2]+=1

        if test_win(grid):
            break

        if count%1 >= 0:
            grid_cp = [[*i] for i in grid]
            car, direction=random.choice(movable_cars2(cars, size, grid_cp))
            print("Random move: ", car[0], direction)
            move_car(car, direction, grid_cp)

            new_grid_str = get_str(grid_cp)
            print("Random move happened")
            print(detect_random(grid, new_grid_str, (6, 6)))
            print_grid(get_grid(new_grid_str, (6, 6)))

            print("Checking solution...")
            print(check_solution(grid, cars, moves, new_grid_str, (6, 6)))

    print_grid(grid)



def check_solution(grid, cars, moves, new_str, size):

    move_keys={'a': 'left', 'd': 'right', 'w': 'up', 's': 'down', ' ': 'space', '':'none'}

    grid_cp= get_grid(new_str, size)
    cars_cp= get_cars(grid_cp, size)
    moves_cp= [*moves]

    cars_idx={cars[i][0]:i for i in range(len(cars))}

    random_move = detect_random(grid, new_str, size)

    for idx, move in enumerate(moves):
        if move[0] == random_move[0]: # if the car is the same

            if move[1] == random_move[1]: # if the move is the same
                moves_cp.pop(idx)
                print("Removed move: ", move)
                break

            elif move[1] != random_move[1]: # if the move is the opposite
                moves_cp.insert(idx, move)  # add the move again (quick fix?)
                print("Added1 move: ", move)
                break

    idx=0
    while idx < len(moves_cp):
        move = moves_cp[idx]
        car = cars_cp[cars_idx[move[0]]]

        # print_grid(grid_cp)
        # print("Move: ", move[0], move_keys[move[1]])
        # print("Car: ", car[0])

        if verify_move(car, move[1], grid_cp, size):
            
            move_car(car, move[1],grid_cp)
            
            match move[1]:
                case 'a': # left
                    car[1]-=1
                case 'd': # right
                    car[1]+=1
                case 'w': # up
                    car[2]-=1
                case 's': # down
                    car[2]+=1

            idx+=1
            # print("Move verified and done")

        else:

            if random_move[1] == 'a':
                move_= (random_move[0], 'd')
            elif random_move[1] == 'd':
                move_= (random_move[0], 'a')
            elif random_move[1] == 'w':
                move_= (random_move[0], 's')
            elif random_move[1] == 's':
                move_= (random_move[0], 'w')

            moves_cp.insert(idx, move_)
            print("Added2 move: ", move_)
            print(moves_cp)
            

    if test_win(grid_cp):
        moves= moves_cp
        return True

    return False


def detect_random(grid, new_str, size):
    """
    Detect if a random move happened
    """
    new_grid = get_grid(new_str, size)

    for y in range(size[1]):
        for x in range(size[0]):
            if grid[y][x] != new_grid[y][x]:

                if grid[y][x] == 'o':
                    random_car = new_grid[y][x]
                    
                    if y-1 >= 0 and new_grid[y-1][x] == random_car:
                        return (random_car, 's')
                    elif x-1 >= 0 and new_grid[y][x-1] == random_car:
                        return (random_car, 'd')

                else:
                    random_car = grid[y][x]
                    
                    if y-1 >= 0 and grid[y-1][x] == random_car:
                        return (random_car, 'w')
                    elif x-1 >= 0 and grid[y][x-1] == random_car:
                        return (random_car, 'a')


def verify_move(car, direction, grid, size=(6, 6)):
    """
    Verify if the move is valid
    """
    _, x, y, _, length = car
    match direction:
        case 'a': # left
            if x-1 < 0 or grid[y][x-1] != 'o':
                return False
        case 'd': # right
            if x+length >= size[0] or grid[y][x+length] != 'o':
                return False
        case 'w': # up
            if y-1 < 0 or grid[y-1][x] != 'o':
                return False
        case 's': # down
            if y+length >= size[1] or grid[y+length][x] != 'o':
                return False
    return True


def movable_cars2(cars, size, grid):
    movable=[]
    for car in cars:
        if car[3]=='h': # if car is horizontal
            if car[1]-1 >= 0 and grid[car[2]][car[1]-1] == 'o':
                movable.append((car, 'a')) # 0 = left
            if car[1]+car[4] < size[0] and grid[car[2]][car[1]+car[4]] == 'o':
                movable.append((car, 'd')) # 1 = right
        else: # if car is vertical
            if car[2]-1 >= 0 and grid[car[2]-1][car[1]] == 'o':
                movable.append((car, 'w')) # 2 = up
            if car[2]+car[4] < size[1] and grid[car[2]+car[4]][car[1]] == 'o':
                movable.append((car, 's')) # 3 = down
    return movable

if __name__ == "__main__":
    main()