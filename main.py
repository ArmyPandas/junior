import random
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle


class CityGrid:
    def __init__(self, n, m, block_coverage=0.3):
        self.n = n
        self.m = m
        self.grid = self.generate_grid(block_coverage)
        self.towers = []  # Список башен и их радиусов

    def generate_grid(self, block_coverage):
        grid = [[0] * self.m for _ in range(self.n)]
        num_blocks = int(self.n * self.m * block_coverage)
        block_positions = random.sample(range(self.n * self.m), num_blocks)

        for position in block_positions:
            row = position // self.m
            col = position % self.m
            grid[row][col] = 1

        return grid

    def place_towers(self, radius):
        towers = []

        def is_covered(row, col):
            for tower in towers:
                tower_row, tower_col, tower_radius = tower
                if (row - tower_row) ** 2 + (col - tower_col) ** 2 <= tower_radius ** 2:
                    return True
            return False

        for row in range(self.n):
            for col in range(self.m):
                if self.grid[row][col] == 0 and not is_covered(row, col):
                    towers.append((row, col, radius))

        self.towers = towers
        return towers

    def visualize(self):
        fig, ax = plt.subplots()
        blocked = []
        tower_positions = np.array(self.towers)
        coverage = np.zeros((self.n, self.m))

        for row in range(self.n):
            for col in range(self.m):
                if self.grid[row][col] == 1:
                    blocked.append((row, col))
                for tower in tower_positions:
                    tower_row, tower_col, tower_radius = tower
                    if (row - tower_row) ** 2 + (col - tower_col) ** 2 <= tower_radius ** 2:
                        coverage[row][col] = 1

        if blocked:
            blocked = np.array(blocked)
            ax.scatter(blocked[:, 1], blocked[:, 0], c='black', marker='s', label='Blocked')

        for i, tower in enumerate(self.towers):
            tower_row, tower_col, tower_radius = tower
            ax.scatter(tower_col, tower_row, c='red', marker='^', label='Towers' if i == 0 else "")
            if i == 0:
                circle = Circle((tower_col, tower_row), tower_radius, color='red', fill=False, linestyle='dotted',
                                label='Tower Radius')
            else:
                circle = Circle((tower_col, tower_row), tower_radius, color='red', fill=False, linestyle='dotted')
            ax.add_patch(circle)

        ax.imshow(coverage, cmap='Blues', alpha=0.3)
        ax.legend()

        ax.set_xlim(0, self.m)
        ax.set_ylim(0, self.n)
        plt.gca().invert_yaxis()
        plt.show()



# Пример использования
if __name__ == "__main__":
    n = 10
    m = 10
    block_coverage = 0.3
    tower_radius = 3

    city = CityGrid(n, m, block_coverage)
    towers = city.place_towers(tower_radius)
    city.visualize()

