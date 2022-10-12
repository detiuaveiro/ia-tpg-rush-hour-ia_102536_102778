from random import choice

class Agent:
    def __init__(self):
        self.current_state = None

    async def update_state(self, state):
        if self.current_state is None or self.current_state["level"] != state["level"]:
            self.calculate_solution()

        self.current_state = state

    async def calculate_solution(self):
        while 1:
            continue

    def get_action(self):
        return self.get_random_action()

    def get_random_action(self):
        return choice(["w", "a", "s", "d", " "])
    