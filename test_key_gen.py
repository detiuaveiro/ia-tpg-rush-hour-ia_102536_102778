from student.Functions import *
from student.KeyGenerator import KeyGenerator

def main():

    size = 6
    grid_str = "ooBoooooBooCAABooCoooooooooooooooooo"
    path = [('B', 's'), ('B', 's'), ('B', 's'), ('A', 'd'), ('A', 'd'), ('A', 'd'), ('C', 'w'), ('A', 'd')]

    k_gen = KeyGenerator(path)

    cursor = [3,3]
    selected = ''

    grid = get_grid(grid_str, size)
    cars = get_cars(grid)

    k_gen.size = size
    k_gen.cursor = cursor
    k_gen.selected = selected
    k_gen.grid = grid
    k_gen.cars = cars

    print_grid(grid)
    print(f"Cursor: {cursor}")
    print(f"Selected: {selected}")
    print(f"Move: {path[0]}")

    while path:
        
        key = k_gen.next_key()
        print(f"Key: {key}")
        k_gen.simulate(key)

        if k_gen.moving:
            k_gen.move_completed()
            print(f"'o' space: {k_gen.moved}")

            if path:
                print()
                print_grid(grid)
                print(f"Cursor: {cursor}")
                print(f"Selected: {selected}")
                print(f"Move: {path[0]}")

    print()
    print_grid(grid)
    
main()