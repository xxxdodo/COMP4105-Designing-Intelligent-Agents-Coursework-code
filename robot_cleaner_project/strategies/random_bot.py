# [Reference from "SimpleBot2.py" (module code)] Random strategy
import random

class RandomBot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.env = None
        self.turning_count = 0
        self.moving_count = random.randint(5, 10)

    def act(self):
        if self.env.is_dirty(self.x, self.y):
            self.env.clean_tile(self.x, self.y)
            return

        if self.turning_count > 0:
            direction = random.choice(['up', 'down', 'left', 'right'])
            self.turning_count -= 1
        elif self.moving_count > 0:
            direction = random.choice(['up', 'down', 'left', 'right'])
            self.moving_count -= 1
        else:
            self.turning_count = random.randint(2, 5)
            self.moving_count = random.randint(5, 10)
            direction = random.choice(['up', 'down', 'left', 'right'])

        dx, dy = 0, 0
        if direction == 'up':
            dx, dy = -1, 0
        elif direction == 'down':
            dx, dy = 1, 0
        elif direction == 'left':
            dx, dy = 0, -1
        elif direction == 'right':
            dx, dy = 0, 1

        new_x = (self.x + dx) % self.env.size
        new_y = (self.y + dy) % self.env.size

        if self.env.grid[new_x][new_y] != 'obstacle':
            self.x, self.y = new_x, new_y
