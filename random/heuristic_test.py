
def heuristic():
    pass


def distance_to_exit(grid, cars):
    for c in cars:
        if c[0] == 'A':
            return len(grid) - c[-1]  


def blocking_blocks(grid, cars):
    x = None
    y = None
    length = None

    blocking_cars = []
    for c in cars:
        if c[0] == 'A':
            x, y, length = c[1], c[2], c[-1]
            break

    for x_grid in range(x + length, len(grid)):
        if grid[y][x_grid] not in blocking_cars and grid[y][x_grid] != 'o':
            blocking_cars.append(grid[y][x_grid])

    return len(blocking_cars)


def lower_bound_blocking(grid, cars):
    cars_info = {c[0]: c for c in cars}
    blocking_cars = []

    x, y, length = cars_info["A"][1], cars_info["A"][2], cars_info["A"][-1]

    #find all blocking cars
    for x_ in range(x + length, len(grid)):
        if grid[y][x_] != 'o' and cars_info[grid[y][x_]] not in blocking_cars: 
            blocking_cars.append(cars_info[grid[y][x_]])


    #find all blocking cars that block the blocking cars
    block_up = 0
    block_down = 0
    total_blocking = len(blocking_cars)

    for bc in blocking_cars:
        x, y, dir, length = bc[1], bc[2], bc[3], bc[-1]

        #test up
        for y_ in range(y-1, -1, -1):
            if grid[y_][x] != 'o':
                if grid[y_][x] != 'x':
                    if cars_info[grid[y_][x]][3] == 'h':
                        block_up += 1
                    else:
                        break
                else:
                    block_up += 1

        #test down
        for y_ in range(y+length, len(grid)):
            if grid[y_][x] != 'o':
                if grid[y_][x] != 'x':
                    if cars_info[grid[y_][x]][3] == 'h':
                        block_down += 1
                    else:
                        break
                else:
                    block_down += 1

        if block_down < block_up:
            return block_down
        return block_up
