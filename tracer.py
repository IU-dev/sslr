class Tracer:

    def __init__(self, board):
        self._board = board

    def has_trace(self, start, finish):
        self._trace_init(start)
        self._trace()
        print_board(self._board_copy)
        return self._board_copy[finish[0]][finish[1]] > 0

    def _trace_init(self, start):
        self._board_copy = [
            [-1 if self._board[i][j] else 0 for j in range(len(self._board[i]))]
            for i in range(len(self._board))
        ]
        self._waves = [[start]]
        self._board_copy[start[0]][start[1]] = 1

    def _trace(self):
        while self._last_wave_is_not_empty():
            self._trace_next_wave()

    def _trace_next_wave(self):
        wave = []
        for field in self._get_last_wave():
            neighbors = self._get_neigbors(field)
            for neighbor in neighbors:
                if self._board_copy[neighbor[0]][neighbor[1]] == 0:
                    wave.append(neighbor)
        self._append_wave(wave)

    def _last_wave_is_not_empty(self):
        return len(self._get_last_wave()) > 0

    def _get_last_wave(self):
        return self._waves[len(self._waves) - 1]

    def _append_wave(self, wave):
        self._waves.append(wave)
        cur_wave_num = len(self._waves)
        for field in wave:
            self._board_copy[field[0]][field[1]] = cur_wave_num

    def _get_neigbors(self, field):
        candidats = [
            (field[0], field[1] - 1),
            (field[0] - 1, field[1]),
            (field[0], field[1] + 1),
            (field[0] + 1, field[1]),
        ]
        res = []
        for candidat in candidats:
            if 0 <= candidat[0] < len(self._board_copy) and 0 <= candidat[1] < len(self._board_copy[candidat[0]]):
                res.append(candidat)
        return res


def print_board(board):
    for row in board:
        print(', '.join(map(item_to_str,row)))

def item_to_str(item):
    item = str(item)
    return ' ' * (3 - len(item)) + item

if __name__ == '__main__':
    board = [
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    tracer = Tracer(board)
    print(tracer.has_trace((5, 0), (0, 9)))
