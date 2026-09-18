import pygame
import random
import time
from state import GameState
from logic import GameLogic, Solver
from view import GameView, WIDTH, HEIGHT

class PlayController:
    def __init__(self, size=4):
        self.state = GameState(size)
        self.history = []

    def move(self, direction):
        if direction in GameLogic.get_legal_moves(self.state.board, self.state.size):
            self.history.append(list(self.state.board))
            self.state.board = GameLogic.apply_move(self.state.board, direction, self.state.size)
            self.state.steps += 1

    def shuffle(self):
        for _ in range(100):
            moves = GameLogic.get_legal_moves(self.state.board, self.state.size)
            self.state.board = GameLogic.apply_move(self.state.board, random.choice(moves), self.state.size)
        self.state.steps = 0

def main():
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    ctrl = PlayController(4)
    view = GameView(screen, ctrl)
    ctrl.shuffle()

    running = True
    while running:
        view.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:    ctrl.move('UP')
                if event.key == pygame.K_DOWN:  ctrl.move('DOWN')
                if event.key == pygame.K_LEFT:  ctrl.move('LEFT')
                if event.key == pygame.K_RIGHT: ctrl.move('RIGHT')
                if event.key == pygame.K_r:     ctrl.shuffle()
                if event.key == pygame.K_s:
                    start = time.time()
                    path = Solver.solve(ctrl.state.board, ctrl.state.size)
                    print(time.time()-start)
                    if path:
                        for m in path:
                            ctrl.move(m)
                            view.draw()
                            pygame.time.delay(100)
    pygame.quit()

if __name__ == "__main__":
    main()