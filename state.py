class GameState:
    def __init__(self, size=4):
        self.size = size
        self.board = list(range(1, size**2)) + [0]
        self.steps = 0

    def get_heuristic(self):
        from logic import GameLogic
        return GameLogic.heuristic(self.board, self.size)