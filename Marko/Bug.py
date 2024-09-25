from abc import abstractmethod


class Bug:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def get_moves(self, current_state):
        raise NotImplementedError("This method should not be called directly.")


class Queen(Bug):
    def __init__(self, x, y):
        super().__init__(x, y)

    def get_moves(self, current_state):
        # [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]
        ...


