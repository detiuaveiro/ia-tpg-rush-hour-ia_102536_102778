from student.Functions import print_grid

"""
Heuristicas admissiveis:

    1.  Distancia do carro 'A' até à saída
    2.  Número de carros que bloqueiam a passagem do carro 'A'
    3.  Igual à anterior mas a heuristica para carros mais pequenos é menor (por isso melhor) do que para carros maiores.
    4.  Número de carros bloqueados, mas se estes carros estiverem bloqueados por outros o seu custo será maior (+1 ou +2)
    5.  Espaço livre ao redor ???


    Heuristicas inadmissiveis:
    6.  número de carros à direita do carro vermelho
    
"""

#1.
def dist_to_exit(size, cars):
    return size - cars[0][1] + cars[0][-1]
        

#2.
def blocking_cars(board, size, cars):
    l, x, y, direction, length = cars[0]
    block_cars = 0

    for x_ in range(x + length, size):
        if board[y * size + x_] != 'o':
            block_cars += 1

    return block_cars


#3.
def blocking_cars_2(board, size, cars):
    l, x, y, direction, length = cars[0]
    block_cars = 0
    l = None

    for c in cars:
        if c[3] == 'v' and c[1] >= x + length:
            for y_ in range(c[2], c[2] + c[-1]):
                if y_ == y:
                    if c[-1] == 3:
                        block_cars += 2
                    else:
                        block_cars += 1
                    break

    return block_cars


#4.
def blocking_cars_3(board, size, cars):
    l, x, y, direction, length = cars[0]
    block_cars = 0
    l = None

    for c in cars:
        if c[3] == 'v' and c[1] >= x + length:
            
            for y_ in range(c[2], c[2] + c[-1]):

                if y_ == y:

                    #check if is blocked or not
                    if c[2] > 0 and board[((c[2]-1)*size + c[1])] == 'o':
                        block_cars += 1
                    elif (c[2] + c[-1]) < size and board[((c[2]+c[-1])*size + c[1])] == 'o':
                        block_cars += 1
                    else:
                        block_cars += 2
                    break

    return block_cars


#use the same for loop to join the blocking_cars_2 and blocking_cars_3
def blocking_cars_4(board, size, cars):
    l, x, y, direction, length = cars[0]
    block_cars1 = 0
    block_cars2 = 0
    l = None

    for c in cars:
        if c[3] == 'v' and c[1] >= x + length:
            
            for y_ in range(c[2], c[2] + c[-1]):
                if y_ == y:
                    #check block by its size
                    if c[-1] == 3:
                        block_cars1 += 2
                    else:
                        block_cars1 += 1

                    #check if it is blocked or not
                    if (c[2] - 1) >= 0 and board[((c[2]-1)*size + c[1])] == 'o':
                        block_cars2 += 1
                    elif (c[2] + c[-1]) < size and board[((c[2]+c[-1])*size + c[1])] == 'o':
                        block_cars2 += 1
                    else:
                        block_cars2 += 2
                    break

    return block_cars1 + block_cars2


#5.
def free_space(board, size, cars):
    total_free_space = 0

    for c in cars:
        l, x, y, direction, length = c

        #free space for horizontal cars
        if direction == 'h':
            #right
            for x_ in range(x+length, size):
                if board[y*size + x_] == "o":
                    total_free_space += 1
                else:
                    break

            #left
            for x_ in range(x-1, -1, -1):
                if board[y*size + x_] == "o":
                    total_free_space += 1
                else:
                    break

        #free space for vertical cars
        else:
            #down
            for y_ in range(y+length, size):
                if board[y_*size + x] == "o":
                    total_free_space += 1
                else:
                    break

            #up
            for y_ in range(y-1, -1, -1):
                if board[y_*size + x] == "o":
                    total_free_space += 1
                else:
                    break
    
    # print_board(board, size)
    # print(f"Free space: {total_free_space}\n\n")
    return total_free_space


def heuristic_(board, size, cars):
    #return 0
    #return free_space(board, size, cars)
    #return blocking_cars(board, size, cars) + free_space(board, size, cars)
    return blocking_cars_4(board, size, cars) + blocking_cars(board, size, cars)# + free_space(board, size, cars)



#aux func
def print_board(board, size):
    for i in range(size):
        for j in range(size):
            print(board[i*size + j], end=' ')
        print()
