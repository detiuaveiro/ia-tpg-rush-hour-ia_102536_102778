from Functions import *
from Agent import Agent
from Node import Node
import time

# car = ( letter, x, y, orientation, length )

def main():

    state = {"level": 1, "selected":'', "dimensions": [6, 6], "cursor": [3, 3], "grid": "01 BBCCMxEEELMNAAKLoNooKFFoJGGoooJHHIIo 5"}

    level = 57

    agent = Agent()

    total_times=0
    with open("levels.txt") as f:
        for line in f:
            
            if level != 0 and level != int(line.split(" ")[0]):
                continue

            print(f"\nLevel: {line.split(' ')[0]} -> {line.split(' ')[1]}")

            board= [*line.split(" ")[1]]
            print_board(board, 6)

            agent.selected= ''
            agent.cursor = [3, 3]
            agent.level = state["level"]
            agent.size = state["dimensions"][0]
            agent.grid = get_grid(line.split(" ")[1], agent.size)
            agent.cars = get_cars(agent.grid, agent.size)

            agent.root= Node(None, board, agent.cars, None, 0, 0)

            start = time.time()
            path= agent.solve()
            end = time.time()

            total_times += end-start

            print("Time: ", end-start)
            print("Path: ", path)
            print("Moves: ", len(path))


    print("Total Time: ", total_times)


if __name__ == "__main__":
    main()

