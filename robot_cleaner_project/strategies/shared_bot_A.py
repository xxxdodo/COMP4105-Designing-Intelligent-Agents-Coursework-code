# strategies/shared_bot.py
import heapq

class SharedBotA:
    def __init__(self, shared_map):
        self.x = 0
        self.y = 0
        self.env = None
        self.shared_map = shared_map
        self.path = []

    def act(self):
        if self.env.is_dirty(self.x, self.y):
            self.env.clean_tile(self.x, self.y)
            self.path.clear()
            return

        if self.path:
            nx, ny = self.path.pop(0)
            self.x, self.y = nx, ny
            return

        self.shared_map.add((self.x, self.y))
        targets = [
            (i, j)
            for i in range(self.env.size)
            for j in range(self.env.size)
            if self.env.is_dirty(i, j)
        ]
        if not targets:
            return

        targets.sort(key=lambda p: abs(p[0]-self.x) + abs(p[1]-self.y))
        goal = targets[0]

        full_path = self._a_star((self.x, self.y), goal)
        self.path = full_path[1:] if full_path else []
        if self.path:
            nx, ny = self.path.pop(0)
            self.x, self.y = nx, ny

    def _a_star(self, start, goal):
        N = self.env.size
        grid = self.env.grid
        open_set = [(0 + manhadun(start, goal), 0, start, None)]
        came_from = {}
        g_score = {start: 0}

        while open_set:
            f, g, current, parent = heapq.heappop(open_set)
            if current in came_from:
                continue
            came_from[current] = parent
            if current == goal:
                path = []
                node = current
                while node:
                    path.append(node)
                    node = came_from[node]
                return list(reversed(path))
            x, y = current
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = (x+dx) % N, (y+dy) % N
                if grid[nx][ny] == 'obstacle':
                    continue
                tentative_g = g + 1
                neighbor = (nx, ny)
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + manhadun(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor, current))
        return []
def manhadun(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])