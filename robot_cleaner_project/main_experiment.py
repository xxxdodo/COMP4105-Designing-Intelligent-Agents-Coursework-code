

import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from strategies.random_bot import RandomBot
from strategies.memory_bot import MemoryBot
from strategies.shared_bot import SharedBot
from strategies.memory_bot_A import MemoryBotA
from strategies.shared_bot_A import SharedBotA


class VirtualEnv:
    def __init__(self, size=20, dirt_count=50, obstacle_count=20):
        self.size = size
        #clean
        self.grid = [["clean" for _ in range(size)] for _ in range(size)]
        self.remaining_dirt = 0
        self.agents = []

        #obstacle
        obstacle = 0
        while obstacle < obstacle_count:
            x, y = random.randrange(size), random.randrange(size)
            if self.grid[x][y] == "clean":
                self.grid[x][y] = "obstacle"
                obstacle += 1

        #dirty
        dirt = 0
        while dirt < dirt_count:
            x, y = random.randrange(size), random.randrange(size)
            if self.grid[x][y] == "clean":
                self.grid[x][y] = "dirty"
                dirt += 1
        self.remaining_dirt = dirt

    def place_agents(self, agents):
        self.agents = agents
        for agent in self.agents:
            agent.env = self
            agent.x, agent.y = random.randint(0, self.size-1), random.randint(0, self.size-1)

    def step(self):
        for agent in self.agents:
            agent.act()

    def is_dirty(self, x, y):
        return self.grid[x][y] == "dirty"

    def clean_tile(self, x, y):
        if self.grid[x][y] == "dirty":
            self.grid[x][y] = "clean"
            self.remaining_dirt -= 1


def run_experiment(strategy_name, strategy_class, num_agents, runs=10):
    step_counts = []

    for _ in range(runs):
        env = VirtualEnv(size=10, dirt_count=30, obstacle_count=10)

        # shared_map
        if strategy_name.startswith("shared"):
            shared_map = set()
            agents = [strategy_class(shared_map) for _ in range(num_agents)]
        else:
            agents = [strategy_class() for _ in range(num_agents)]

        env.place_agents(agents)

        steps = 0
        while env.remaining_dirt > 0:
            env.step()
            steps += 1

        step_counts.append(steps)

    avg_steps = np.mean(step_counts)
    print(f"Strategy: {strategy_name}, Agents: {num_agents}, Avg Steps: {avg_steps:.2f}")
    return (strategy_name, num_agents, avg_steps)

def plot(data):
    df = pd.DataFrame(data, columns=["Strategy", "Agents", "Avg_Steps"])
    
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df, x="Agents", y="Avg_Steps", hue="Strategy", marker="o")
    plt.title("Average Steps vs Number of Agents")
    plt.ylabel("Average Steps (lower is better)")
    plt.xlabel("Number of Agents")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_bar(data):
    df = pd.DataFrame(data, columns=["Strategy", "Agents", "Avg_Steps"])

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="Agents", y="Avg_Steps", hue="Strategy", palette="Set2")
    plt.title("Comparison of Average Steps by Strategy and Number of Agents")
    plt.ylabel("Average Steps (lower is better)")
    plt.xlabel("Number of Agents")
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    strategies = {
        "random": RandomBot,
        "memory": MemoryBot,
        "shared": SharedBot,
        "memory_a": MemoryBotA,
        "shared_a": SharedBotA
    }
    all_results = []
    for strategy_name, strategy_class in strategies.items():
        for num in [1, 2, 3]:
            result = run_experiment(strategy_name, strategy_class, num_agents=num)
            all_results.append(result)
    plot(all_results)
    plot_bar(all_results)



