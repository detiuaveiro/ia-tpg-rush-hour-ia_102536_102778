from Agent import Agent
import random
import time

state = {'dimensions': [6, 6], 'level': 1, 'grid': '1 oooooHoxCCoHAAoGoooFoGoooFDDxooooooo 5', 'score': -605, 'game_speed': 10, 'cursor': [3, 3], 'selected': '', 'player': 'leo'}

direction = [ "vertical", "horizontal" ]
moves= [ "left", "right", "up", "down"]

def print_grid(grid):
    print()
    for i in grid:
        for j in i:
            print(j, end=' ')
        print()
    print()

agent = Agent()
agent.update_state(state)

grid = agent.start_grid
cars = agent.start_cars


# movable = agent.movable_cars(cars, grid)
# print_grid(grid)
# for i in movable:
#     print(cars[i[0]][0], moves[i[1]], end='; ')
# print()
# move = random.choice(movable)
# print(f"\nMoving {cars[move[0]][0]} {moves[move[1]]}")
# agent.move_car(cars[move[0]], move[1], grid)
# print_grid(grid)


print_grid(grid)
start = time.time()
moves=0
# while grid[2][5] != 'A':
while moves < 1000000:
    move = random.choice(agent.movable_cars(cars, grid))
    agent.move_car(cars[move[0]], move[1], grid)
    moves+=1
end = time.time()
print(f"Time: {end-start} seconds")
print(f"Moves: {moves}")
print_grid(grid)

# arr = agent.solve()

# for node in arr:
#     print_grid(node.grid)