import time
from student.Agent import Agent

def main():

    state = {"level": 1, "selected":'', "dimensions": [6, 6], "cursor": [3, 3], "grid": "01 BBCCMxEEELMNAAKLoNooKFFoJGGoooJHHIIo 5"}


    level = 0

    agent = Agent()

    total_times=0

    with open("levels.txt") as f:
        for line in f:
            
            if level != 0 and level != int(line.split(" ")[0]):
                continue

            state["grid"]=line
            state["level"]=int(line.split(" ")[0])

            print("\nLevel: ", state["level"])

            agent.update_state(state)

            start = time.time()
            path= agent.solve2()
            end = time.time()

            total_times += end-start

            print("Time: ", end-start)
            print("Path: ", path)
            print("Moves: ", len(path))


    print("Total Time: ", total_times)


if __name__ == "__main__":
    main()