# Quando houver movimento random:

# Se o sitio for usado até ao fim, mover o carro para trás

# Se o sitio for usado até ao fim, recalcular solução

# Quando tiver o próximo movimento bloqueado, recalcular a solução

# Quando tiver o próximo movimento bloqueado, calcular um caminho para poder fazer o movimento
# (Pode ter consequencias depois)

# Calcular uma solução em que o final é um estado já calculado (navegar nos nós e comparar)
# (Acho q nao é boa ideia)

# Calcular soluçao, MAS usar o que está calculado pra chegar rapidamente ao resultado
# (idk how)

# Ver o ponto em q vai bloquear e calcular uma solução até lá e depois seguir a solução original

# Para ver se é benefico/indiferente: retirar esse move dos moves e ver se chega à soluçao
# Se bloquear antes de mover essa peça, é pq foi a razao de bloquear
# Se bloquear depois, é pq ficou fora do sitio e bloqueou outro carro

# Usar os moves calculados a partir do final??

def main():
    grid_str = "oooooHoxCCoHAAoGoooFoGoooFDDxooooooo"
    moves= [('H', 's'), ('H', 's'), ('H', 's'), ('C','d'), ('C','d'), ('G','w'),('G','w'),('A','d'), ('A','d'), ('A','d'), ('A','d')]

    move_keys={'a': 'left', 'd': 'right', 'w': 'up', 's': 'down', ' ': 'space', '':'none'}

    grid = get_grid(grid_str, (6, 6))
    cars = get_cars(grid, (6, 6))

    cars_idx={cars[i][0]:i for i in range(len(cars))}

    # print("Level: 4")
    # print_grid(grid)
    # print(f"Number of moves: {len(moves)}")

    # count=0
    # while moves:
    #     car = cars[cars_idx[moves[0][0]]]
        
    #     if not verify_move(car, moves[0][1], grid):
    #         print_grid(grid)
    #         print("Invalid move: ",moves[0])
            
    #         moves.insert(0, ('C','d'))
    #         print("Added move: ",moves[0])
    #         # moves.pop(0)
    #         count+=1
    #         continue

    #     print(f"Moving car {car[0]} to {move_keys[moves[0][1]]}")

    #     move_car(car, moves[0][1], grid)
    #     moves.pop(0)

    #     if count == 3:
    #         # print_grid(grid)
    #         print(f"\nRandom move: C to {move_keys['a']}")
    #         move_car(cars[cars_idx['C']], 'a', grid)     

    #     count+=1   

    # print_grid(grid)

    print_grid(grid)
    new_grid_str= "oooooHoxoCCHAAoGoooFoGoooFDDxooooooo" # changed C to right


    if get_str(grid) != new_grid_str:
        print("Random move happened")
        print(detect_random(grid, new_grid_str, (6, 6)))
        print_grid(get_grid(new_grid_str, (6, 6)))


        print("Checking solution...")
        print(check_solution(grid, cars, moves, new_grid_str, (6, 6)))

    

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
                print("Added move: ", move)
                break

    #TODO mudar o for pra um while e quando bloquear meter o move oposto

    for move in moves_cp:
        # print_grid(grid_cp)
        # print(f"Moving car {move[0]} to {move_keys[move[1]]}")

        car = cars_cp[cars_idx[move[0]]]
        
        if not verify_move(car, move[1], grid_cp):
            print_grid(grid_cp)
            print("Invalid move: ",move)
            return False

        move_car(car, move[1], grid_cp)

    print_grid(grid_cp)

    moves= moves_cp


    return True



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


def get_str(grid):
    """
    Get the string from the grid
    """
    return ''.join([''.join(i) for i in grid])


def get_grid(str, size):
    """
    Get the grid from a string
    """
    return [[*str[i*size[0]:i*size[0]+size[0]]] for i in range(size[1])]


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
    # cars_.sort(key=lambda x: x[0])
    return cars_

def move_car(car, direction, grid):
    """
    Move the car to a given direction
    """
    match direction:
        case 'a': # left
            grid[car[2]][car[1]-1] = car[0]
            grid[car[2]][car[1]+car[4]-1] = 'o'
            car[1] -= 1
        case 'd': # right
            grid[car[2]][car[1]+car[4]] = car[0]
            grid[car[2]][car[1]] = 'o'
            car[1] += 1
        case 'w': # up
            grid[car[2]-1][car[1]] = car[0]
            grid[car[2]+car[4]-1][car[1]] = 'o'
            car[2] -= 1
        case 's': # down
            grid[car[2]+car[4]][car[1]] = car[0]
            grid[car[2]][car[1]] = 'o'
            car[2] += 1

main()