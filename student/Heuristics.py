# from Functions import print_board

"""
Heuristicas admissiveis:

    ->  Distancia do carro 'A' até à saída
    ->  Número de carros que bloqueiam a passagem do carro 'A'
    ->  Igual à anterior mas a heuristica para carros mais pequenos é menor (por isso melhor) do que para carros maiores.
    ->  Número de carros bloqueados, mas se estes carros estiverem bloqueados por outros o seu custo será maior (+1 ou +2)
    ->  Espaço livre ao redor ???


    Heuristicas inadmissiveis:
    ->  número de carros à direita do carro vermelho
    
"""

def dist_to_exit(size, cars):
    return size - cars[0][1] + cars[0][-1]
        

def blocking_cars(board, size, cars):
    l, x, y, direction, length = cars[0]
    block_cars = 0

    for x_ in range(x + length, size):
        if board[y * size + x_] != 'o':
            block_cars += 1

    return block_cars


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


def blocking_cars_3(board, size, cars):
    l, x, y, direction, length = cars[0]
    block_cars = 0
    l = None

    for c in cars:
        if c[3] == 'v' and c[1] >= x + length:
            
            for y_ in range(c[2], c[2] + c[-1]):

                if y_ == y:

                    #check if is blocked or not
                    if (c[2] - 1) >= 0 and board[((c[2]-1)*size + c[1])] == 'o':
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


def heuristic_(board, size, cars):
    return blocking_cars_4(board, size, cars) + blocking_cars(board, size, cars)



    # return heuristic_(self.board, 6, self.cars)
    #     _, x, y, _, length = self.cars[0]

    #     blocking_cars = 0
    #     for pos in range(x+length + y*6, 5 + y*6):
    #         if self.board[pos] != 'o':
    #             blocking_cars += 1

    #     return blocking_cars