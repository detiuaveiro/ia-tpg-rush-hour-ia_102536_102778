class Node:

    def __init__(self, grid, cars, parent=None):
        """
        Node constructor
        """
        self.parent = parent
        self.grid = grid
        self.cars = cars
        self.move = None


    @property
    def grid_str(self):
        """
        Get the grid as a string
        """
        return "".join(["".join(row) for row in self.grid])

    


    