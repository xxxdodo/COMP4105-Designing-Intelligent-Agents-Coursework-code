# [Reference from "simpleBot2_withMapping.py" (module code)] Memory strategy

import random

class MemoryBot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.env = None
        self.memory_map = set()

    def act(self):
        if self.env.is_dirty(self.x, self.y):
            self.env.clean_tile(self.x, self.y)
            return


        self.memory_map.add((self.x, self.y))


        candidates = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx = (self.x + dx) % self.env.size
            ny = (self.y + dy) % self.env.size
            if self.env.grid[nx][ny] != 'obstacle' and (nx, ny) not in self.memory_map:
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
