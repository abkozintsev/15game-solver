import pygame
from logic import GameLogic

WIDTH, HEIGHT = 800, 800
TILE_BG, EMPTY_BG = (52, 73, 94), (44, 62, 80)
HIGHLIGHT = (46, 204, 113)

class GameView:
    def __init__(self, screen, controller):
        self.screen = screen
        self.ctrl = controller
        self.font = pygame.font.SysFont("Verdana", 18)
        self.mini_font = pygame.font.SysFont("Verdana", 10)
        self.tile_size = 400 // controller.state.size
        self.mini_tile_size = 80 // controller.state.size
        pygame.display.set_caption("15game")

    def draw(self):
        self.screen.fill((33, 33, 33))
        state = self.ctrl.state
        ox, oy = (WIDTH-400)//2, (HEIGHT-400)//2

        for i, tile in enumerate(state.board):
            r, c = divmod(i, state.size)
            rect = pygame.Rect(ox + c*self.tile_size, oy + r*self.tile_size, self.tile_size-5, self.tile_size-5)
            pygame.draw.rect(self.screen, TILE_BG if tile != 0 else EMPTY_BG, rect, border_radius=8)
            if tile != 0:
                txt = self.font.render(str(tile), True, (255,255,255))
                self.screen.blit(txt, txt.get_rect(center=rect.center))

        stats = f"Moves: {state.steps} | H: {state.get_heuristic()}"
        self.screen.blit(self.font.render(stats, True, HIGHLIGHT), (20, 20))
        self.draw_previews(ox, oy)
        pygame.display.flip()

    def draw_previews(self, ox, oy):
        legal = GameLogic.get_legal_moves(self.ctrl.state.board, self.ctrl.state.size)
        dirs = {'UP': (WIDTH//2, oy+480), 'DOWN': (WIDTH//2, oy-80), 
                'LEFT': (ox+480, oy+200), 'RIGHT': (ox-80, oy+200)}
        
        for move, pos in dirs.items():
            if move in legal:
                sim = GameLogic.apply_move(self.ctrl.state.board, move, self.ctrl.state.size)
                mx, my = pos[0]-40, pos[1]-40
                for i, tile in enumerate(sim):
                    r, c = divmod(i, self.ctrl.state.size)
                    rect = pygame.Rect(mx + c*self.mini_tile_size, my + r*self.mini_tile_size, 
                                       self.mini_tile_size-1, self.mini_tile_size-1)
                    pygame.draw.rect(self.screen, (41, 128, 185) if tile != 0 else EMPTY_BG, rect)
                self.screen.blit(self.font.render(move, True, (200,200,200)), (pos[0]-20, pos[1]+45))