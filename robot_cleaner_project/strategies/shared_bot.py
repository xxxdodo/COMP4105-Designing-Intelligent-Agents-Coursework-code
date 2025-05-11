
import random

class SharedBot:
    def __init__(self, shared_map):
        self.x = 0
        self.y = 0
        self.env = None
        self.shared_map = shared_map

    def act(self):
        if self.env.is_dirty(self.x, self.y):
            self.env.clean_tile(self.x, self.y)
            return

        self.shared_map.add((self.x, self.y))

        candidates = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx = (self.x + dx) % self.env.size
            ny = (self.y + dy) % self.env.size
            if self.env.grid[nx][ny] != 'obstacle' and (nx, ny) not in self.shared_map:
                candidates.append((nx, ny))

        if candidates:
            self.x, self.y = random.choice(candidates)
        else:
            for _ in range(5):
                dx, dy = random.choice([(-1,0), (1,0), (0,-1), (0,1)])
                nx = (self.x + dx) % self.env.size
                ny = (self.y + dy) % self.env.size
                if self.env.grid[nx][ny] != 'obstacle':
                    self.x, self.y = nx, ny
                    break
