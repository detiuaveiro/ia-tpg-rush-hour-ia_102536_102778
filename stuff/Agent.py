def ola():
    print("ola")

class Agent:

    def __init__(self):
        self.cursor = None
        self.selected = None
        self.current_grid = None
        self.current_cars = None
        ola()

    
    def update_state(self, state):
        self.cursor = state["cursor"]
        self.selected = state["selected"]