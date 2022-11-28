from Map_gen import Map_gen
from BFS import BFS

def main():
    size = 8
    car_prob = 80
    x_prob = 5
    min_depth = 30
    num_boards = 1

    map = Map_gen()
    map.update(size, car_prob, x_prob)

    maps = []
    while len(maps) < num_boards:
        print("Generating map...")
        map.generate()
        map_str = str(map)
        print_map(map.map)
        BFS.size = map.size
        bfs = BFS(map_str)
        res = bfs.search(min_depth)
        if res is not None:
            print("Found solution!")
            maps.append((res[0], map_str, res[1]))
        else:
            print("No solution found")

    print("\n\nMaps:")
    for i in range(len(maps)):
        depth, map_str, num_nodes = maps[i]
        print(f"Map {i+1}:")
        print(f"Board : {map_str}")
        print(f"Total number of nodes: {num_nodes}")
        print(f"Moves: {depth}\n")



def print_map(map):
    for i in range(len(map)):
        for j in range(len(map)):
            print(map[i][j], end=' ')
        print()

if __name__ == '__main__':
    main()