# car = ( letter, x, y, orientation, length )

class Node:

    def __init__(self, parent, grid_num, cars, action):
        """
        Node constructor
        """
        self.parent = parent
        self.grid_num = grid_num
        self.cars = cars
        self.action = action

        # self.cost = parent.cost + 1
        # self.heuristic = 0


    def new_node(self, car, idx, direction, size, letters):
        """
        Create new node
        """
        letter , x , y , orientation, length = car

        new_grid_num = self.grid_num

        # left 
        if direction == 'a':
            # place the 'o'
            new_grid_num -= letters[letter] << 8 * (y * size + x + length - 1)
            # place the letter
            new_grid_num += letters[letter] << 8 * (y * size + x - 1)
            # change car
            x -= 1
        # right
        elif direction == 'd':
            # place the 'o'
            new_grid_num -= letters[letter] << 8 * (y * size + x)
            # place the letter
            new_grid_num += letters[letter] << 8 * (y * size + x + length)
            # change car
            x += 1
        # up
        elif direction == 'w':
            # place the 'o'
            new_grid_num -= letters[letter] << 8 * ((y + length - 1) * size + x)
            # place the letter
            new_grid_num += letters[letter] << 8 * ((y - 1) * size + x)
            # change car
            y -= 1
        # down
        else:
            # place the 'o'
            new_grid_num -= letters[letter] << 8 * (y * size + x)
            # place the letter
            new_grid_num += letters[letter] << 8 * ((y + length) * size + x)
            # change car
            y += 1

        # copy the cars
        new_cars = [*self.cars]
        # change car
        new_cars[idx] = (letter, x, y, orientation, length)
        # create new node
        return Node(self, new_grid_num, new_cars, (letter, direction))


    def expand(self, size, letters):
        """
        Expand node
        """
        # loop through cars
        for idx, car in enumerate(self.cars):
            _, x, y, orientation, length = car
            # horizontal
            if orientation == 'h':
                # left
                if x > 0 and self.grid_num >> 8 * (y * size + x - 1) & 0xFF == 0:
                    yield self.new_node(car, idx, 'a', size, letters)
                # right
                if x + length < size and self.grid_num >> 8 * (y * size + x + length) & 0xFF == 0:
                    yield self.new_node(car, idx, 'd', size, letters)
            # vertical
            else:
                # up
                if y > 0 and self.grid_num >> 8 * ((y - 1) * size + x) & 0xFF == 0:
                    yield self.new_node(car, idx, 'w', size, letters)
                # down
                if y + length < size and self.grid_num >> 8 * ((y + length) * size + x) & 0xFF == 0:
                    yield self.new_node(car, idx, 's', size, letters)


    # def __lt__(self, other):
    #     """
    #     Compare nodes
    #     """
    #     return self.cost + self.heuristic < other.cost + other.heuristic
