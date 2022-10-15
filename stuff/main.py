from Agent import Agent
import time

def main():

    level = 21

    with open("levels.txt") as f:
        for line in f:
            
            if level != 0 and level != int(line.split(" ")[0]):
                continue

            solve_level(line)
    

def solve_level(line):
    state = {"level": 1, "selected":'', "dimensions": [6, 6], "cursor": [3, 3], "grid": "01 BBCCMxEEELMNAAKLoNooKFFoJGGoooJHHIIo 5"}

    state["grid"]=line
    state["level"]=int(line.split(" ")[0])

    agent = Agent()

    agent.update_state(state)

    print(f"Level {state['level']}")
    start = time.time()
    x=agent.solve()
    end = time.time()
    print(f"Time: {end-start}")
    print(x)
    print(f"Moves: {len(x)}\n")

main()