from Functions import *

# car = ( letter, x, y, orientation, length )
# move = ( letter, direction )

class RandomCounter:

    def __init__(self, path):
        """
        RandomCounter constructor
        """
        self.size = None
        self.grid = None
        self.cars = None
        self.cars_idx = None
        self.random_move = None
        # pointer to agent path
        self.path = path
        # moves to use for testing
        self.moves = None


    def update_path(self, old_board, new_board, size):
        """
        Update path
        """
        self.size = size
        self.grid = get_grid(new_board, size)
        self.cars = get_cars(self.grid, size)
        self.cars_idx = {car[0]: car for car in self.cars}
        self.moves = [*self.path]
        
        self.random_move = self.detect_random_move(get_grid(old_board, size))
        print(f"Random move detected: {self.random_move}")

        return self.check_path()


    def check_path(self):
        """
        Check if the path is valid and if not try to fix it
        """
        # map the reverse direction
        reverse = {'a': 'd', 'd': 'a', 'w': 's', 's': 'w'}

        # simulate the moves to see if the path is valid and try to fix it if not
        idx = 0 
        while idx < len(self.moves):
            move = self.moves[idx]
            car = self.cars_idx[move[0]]

            if self.random_move is not None and self.random_move[0] == move[0]:
                # if the move is the same
                if move[1] == self.random_move[1]:
                    # remove the move
                    self.moves.pop(idx)
                    # the random move was beneficial
                    print(f"Fix: remove {move}")
                    self.random_move = None
                    continue
                # if the move is not the same
                else:
                    # add the move to counter the random move
                    self.moves.insert(idx, move)
                    # we add the counter move here bc we are moving the car that moved randomly
                    print(f"Fix: add {move} again")
                    self.random_move = None

            # if the move is possible
            if self.verify_move(car, move[1]):
                # move the car
                move_car(self.grid, car, move[1])
                idx += 1
                continue

            # else, the car got stuck bc of the random move
            if self.random_move is None:
                return False
            # insert the counter move here bc its close to the stuck car
            new_move = (self.random_move[0], reverse[self.random_move[1]])
            self.moves.insert(idx, new_move)
            print(f"Fix: add new move {new_move}")
            self.random_move = None 

        # check if it worked
        if test_win(self.cars[0], self.size - 2):
            if self.random_move is not None:
                print(f"Random move doesnt change anything")

            # update the agent path
            self.path[:] = self.moves
            return True
        # if it didn't work
        return False


    def detect_random_move(self, old_grid):
        """
        Detect random move
        """
        # loop through the grid
        for y in range(self.size):
            for x in range(self.size):
                # gird changed
                if old_grid[y][x] != self.grid[y][x]:
                    # if the first change is a 'o' in the new grid
                    # means that the car moved down or right
                    if self.grid[y][x] == 'o':
                        car_letter = old_grid[y][x]  
                        # find the direction
                        if y + 1 < self.size and old_grid[y + 1][x] == car_letter:
                            # car moved down
                            return (car_letter, 's')
                        elif x + 1 < self.size and old_grid[y][x + 1] == car_letter:
                            # car moved right
                            return (car_letter, 'd')    
                    # car moved up or left
                    else:
                        car_letter = self.grid[y][x]
                        # find the direction
                        if y + 1 < self.size and self.grid[y + 1][x] == car_letter:
                            # car moved up
                            return (car_letter, 'w')
                        elif x + 1 < self.size and self.grid[y][x + 1] == car_letter:
                            # car moved left
                            return (car_letter, 'a')

    
    def verify_move(self, car, direction):
        """
        Verify if a move is possible
        """
        _, x, y, _, length = car
        # check left
        if direction == 'a':
            if x - 1 >= 0 and self.grid[y][x - 1] == 'o':
                return True
        # check right
        elif direction == 'd':
            if x + length < self.size and self.grid[y][x + length] == 'o':
                return True
        # check up
        elif direction == 'w':
            if y - 1 >= 0 and self.grid[y - 1][x] == 'o':
                return True
        # check down
        else:
            if y + length < self.size and self.grid[y + length][x] == 'o':
                return True
        # move not possible
        return False
