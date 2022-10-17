from Agent import Agent
import time
import asyncio


async def main():

    level = 1

    agent = Agent()

    with open("levels.txt") as f:
        for line in f:
            
            if level != 0 and level != int(line.split(" ")[0]):
                continue

            # await solve_level(line, agent)
            await solve_level_basic(line, agent)

    print("Done")
    # exit()
    

async def solve_level(line, agent):
    state = {"level": 1, "selected":'', "dimensions": [6, 6], "cursor": [3, 3], "grid": "01 BBCCMxEEELMNAAKLoNooKFFoJGGoooJHHIIo 5"}

    state["grid"]=line
    state["level"]=int(line.split(" ")[0])

    print(f"Level {state['level']}")
    
    agent.update(state)

    print(f"Solution: {agent.solution}")
    print(f"Moves: {len(agent.solution)}\n")

    

async def solve_level_basic(line, agent):
    state = {"level": 1, "selected":'', "dimensions": [6, 6], "cursor": [3, 3], "grid": "01 BBCCMxEEELMNAAKLoNooKFFoJGGoooJHHIIo 5"}

    state["grid"]=line
    state["level"]=int(line.split(" ")[0])

    print(f"Level {state['level']}")
    agent.update_state(state)

    print(agent.action())

    start = time.time()
    await agent.solve()
    end = time.time()
    print(f"Time: {end-start}")

    # for key in agent.solution:
    #     print(key, end=", ")
    # print()

    print(agent.action())

asyncio.run(main())
# main()