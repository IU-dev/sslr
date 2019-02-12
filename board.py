import pygame
import itertools
import random
import tracer


class Board:

    def __init__(self, cols, rows, size):
        self._cols = cols
        self._rows = rows
        self._size = size
        self._surface = pygame.Surface([self.get_width(), self.get_height()])
        self._board = [[(0, 0, 0) for i in range(cols)] for i in range(rows)]
        self._colored = [[(0, 0, 0) for i in range(cols)] for i in range(rows)]
        self._guessed = [[False for i in range(cols)] for i in range(rows)]
        self._queue = []
        self._selected = []
        self._tracer = tracer.Tracer(self._board)
        self._active = False
        self._colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0)
        ]
        for i in range(len(self._colored)):
            for j in range(len(self._colored[i])):
                self._colored[i][j] = self._colors[random.randint(0, 3)]
        self._ticks = 0

    def guess(self):
        row = random.randint(0, 9)
        cell = random.randint(0, 9)
        self._guessed[row][cell] = True
        self._queue.append((row, cell))
        print(self._queue)

    def show_combination(self):
        for cell in self._queue:
            if self._guessed[cell[0]][cell[1]]:
                self._board[cell[0]][cell[1]] = self._colored[cell[0]][cell[1]]
                self._ticks = 2000

    def handle_timer(self, ticks):
        if self._ticks > 0:
            self._ticks -= ticks
            if self._ticks <= 0:
                self._ticks = 0
                for cell in self._queue:
                    if self._guessed[cell[0]][cell[1]]:
                        self._board[cell[0]][cell[1]] = (0, 0, 0)

    def get_surface(self):
        return self._surface

    def render(self):
        self._surface.fill((0, 0, 0))
        pygame.draw.rect(self._surface, (255, 255, 255),
                         (0, 0, self.get_width(), self.get_height()), 1)
        for i in range(self._cols):
            for j in range(self._rows):
                self.render_cell((i, j))
        return self.get_surface()

    def render_cell(self, cell):
        my_top = cell[1] * self._size
        my_left = cell[0] * self._size
        if self.get_item(cell):
            color = self.get_item(cell)
            pygame.draw.rect(self._surface, (255, 255, 255), (my_left, my_top, self._size, self._size), 1)
            if cell == self._active:
                pygame.draw.rect(self._surface, color, (my_left + 3, my_top + 3, self._size - 6, self._size - 6))
            else:
                pygame.draw.rect(self._surface, color, (my_left + 1, my_top + 1, self._size - 2, self._size - 2))
        else:
            pygame.draw.rect(self._surface, (255, 255, 255), (my_left, my_top, self._size, self._size), 1)

    def get_cell(self, x, y):
        return x // self._size, y // self._size

    def get_item(self, cell):
        return self._board[cell[0]][cell[1]]

    def click(self, pos):
        self._selected.append(self.get_cell(pos[0], pos[1]))
        print('Selected: ',self._selected)
        if self._selected == self._queue:
            self.guess()
            self.show_combination()
            self._selected.clear()
        elif len(self._selected) == len(self._queue):
            pygame.quit()


    def step(self):
        if self._active:
            self.step_with_active()
        else:
            self.step_without_active()

    def collapse(self, new_cells):
        cells_to_delete = dict()
        for cell in new_cells:
            series_cells = self.get_series_cells(cell)
            for s_cell in series_cells:
                cells_to_delete[s_cell] = True
        for cell in cells_to_delete:
            self.set_item(cell, False)
        return len(cells_to_delete)

    def get_series_cells(self, cell):
        return self.get_horizontal_series_cells(cell) + self.get_vertical_series_cells(cell)

    def get_horizontal_series_cells(self, cell):
        horizontal_cells = [cell]
        i = cell[0] + 1
        while i < len(self._board):
            next_cell = (i, cell[1])
            horizontal_cells.append(next_cell)
            i += 1
        i = cell[0] - 1
        while i >= 0:
            next_cell = (i, cell[1])
            horizontal_cells.append(next_cell)
            i -= 1
        return horizontal_cells

    def get_vertical_series_cells(self, cell):
        vertical_cells = [cell]
        i = cell[1] + 1
        while i < len(self._board[cell[0]]):
            next_cell = (cell[0], i)
            vertical_cells.append(next_cell)
            i += 1
        i = cell[1] - 1
        while i >= 0:
            next_cell = (cell[0], i)
            vertical_cells.append(next_cell)
            i -= 1
        return vertical_cells

    def step_without_active(self):
        if self.get_item(self.clicked_cell):
            self._active = self.clicked_cell

    def get_height(self):
        return self._rows * self._size

    def get_width(self):
        return self._cols * self._size

    def in_board(self, pos):
        if self._left > pos[0]:
            return False
        if self._left + self.get_height() < pos[0]:
            return False
        if self._top > pos[1]:
            return False
        if self._top + self.get_width() < pos[1]:
            return False
        return True

    def clear_active(self):
        self._active = False
