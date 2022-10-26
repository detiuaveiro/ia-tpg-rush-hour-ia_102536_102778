# car = ( letter, x, y, orientation, length )

class Node:

    def __init__(self, parent, board, cars, action, cost, heuristic):
        """
        Node constructor
        """
        self.parent = parent
        self.board = board
        self.cars = cars
        self.action = action
        self.cost = cost
        self.heuristic = heuristic


    def new_node(self, car, idx, direction, size):
        """
        Create new node
        """
        letter , x , y , _, length = car
        # copy the board
        new_board = [*self.board]

        # left 
        if direction == 'a':  
            # change board  
            new_board[y * size + x - 1] = letter
            new_board[y * size + x + length - 1] = 'o'
            # change car
            x -= 1
        # right
        elif direction == 'd':  
            # change board
            new_board[y * size + x + length] = letter
            new_board[y * size + x] = 'o'
            # change car
            x += 1
        # up
        elif direction == 'w': 
            # change board 
            new_board[(y - 1) * size + x] = letter
            new_board[(y + length - 1) * size + x] = 'o'
            # change car
            y -= 1
        # down
        else:  
            # change board
            new_board[(y + length) * size + x] = letter
            new_board[y * size + x] = 'o'
            # change car
            y += 1
            
        # copy the cars
        new_cars = [*self.cars]
        # change car
        new_cars[idx] = (car[0], x, y, car[3], car[4])
        # create new node
        return Node(self, new_board, new_cars, (car[0], direction), self.cost + 1, 0)


    def expand(self, size):
        """
        Expand node
        """
        # loop through cars
        for idx, car in enumerate(self.cars):
            _, x, y, orientation, length = car
            # horizontal
            if orientation == 'h':
                # move left
                if x > 0 and self.board[y * size + x - 1] == 'o':
                    # create new Node
                    yield self.new_node(car, idx,'a', size)
                # move right
                if x + length < size and self.board[y * size + x + length] == 'o':
                    # create new Node
                    yield self.new_node(car, idx, 'd', size)
            # vertical
            else:
                # move up
                if y > 0 and self.board[(y - 1) * size + x] == 'o':
                    # create new Node
                    yield self.new_node(car, idx, 'w', size)
                # move down
                if y + length < size and self.board[(y + length) * size + x] == 'o':
                    # create new Node
                    yield self.new_node(car, idx, 's', size)


    def __lt__(self, other):
        """
        Compare nodes
        """
        return self.cost + self.heuristic < other.cost + other.heuristic


    def __str__(self):
        """
        String representation of node
        """
        return ''.join(self.board)

