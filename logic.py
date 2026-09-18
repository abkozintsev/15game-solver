import heapq

class GameLogic:
    @staticmethod
    def get_legal_moves(board, size):
        blank_idx = board.index(0)
        r, c = divmod(blank_idx, size)
        check_map = {'UP': (1, 0), 'DOWN': (-1, 0), 'LEFT': (0, 1), 'RIGHT': (0, -1)}
        moves = []
        for move, (dr, dc) in check_map.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                moves.append(move)
        return moves

    @staticmethod
    def apply_move(board, direction, size):
        new_board = list(board)
        blank_idx = new_board.index(0)
        r, c = divmod(blank_idx, size)
        if direction == 'UP':    target_idx = (r + 1) * size + c
        elif direction == 'DOWN':  target_idx = (r - 1) * size + c
        elif direction == 'LEFT':  target_idx = r * size + (c + 1)
        elif direction == 'RIGHT': target_idx = r * size + (c - 1)
        new_board[blank_idx], new_board[target_idx] = new_board[target_idx], new_board[blank_idx]
        return new_board

    @staticmethod
    def heuristic(board, size):
        distance = 0
        for i, tile in enumerate(board):
            if tile != 0:
                curr_r, curr_c = divmod(i, size)
                goal_r, goal_c = divmod(tile - 1, size)
                distance += abs(curr_r - goal_r) + abs(curr_c - goal_c)
        
        # Linear Conflict logic for speed
        for r in range(size):
            row = [board[r*size+c] for c in range(size) if board[r*size+c] != 0 and (board[r*size+c]-1)//size == r]
            for i in range(len(row)):
                for j in range(i+1, len(row)):
                    if row[i] > row[j]: distance += 2
        return distance

class Solver:
    @staticmethod
    def solve(start_board, size):
        goal = tuple(list(range(1, size**2)) + [0]) #e.g. (1,2,3,0) for 2x2
        start = tuple(start_board) 
        if start == goal: return []
        
        weight = 10000 # A* weight
        pq = [(GameLogic.heuristic(start_board, size) * weight, 0, start, [])]
        visited = {start: 0}

        #f = g + h
        #g = cost(previous) + 1
        while pq:
            f, g, current, path = heapq.heappop(pq)
            if current == goal: 
                return path
            curr_list = list(current)
            for move in GameLogic.get_legal_moves(curr_list, size):
                next = tuple(GameLogic.apply_move(curr_list, move, size))
                if next not in visited or (g+1) < visited[next]:
                    visited[next] = g + 1
                    h = GameLogic.heuristic(list(next), size)
                    heapq.heappush(pq, (g + 1 + h * weight, g + 1, next, path + [move]))
        return None