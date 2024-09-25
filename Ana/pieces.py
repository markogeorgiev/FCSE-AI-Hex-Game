from abc import abstractmethod, ABC


class Piece:
    def __init__(self, curr_pos):
        self.curr_pos = curr_pos

    @abstractmethod
    def allowed_movements(self):
        pass


class Queen(Piece, ABC):
    def __init__(self, curr_pos):
        super().__init__(curr_pos)

    def allowed_movements(self):
        x, y = self.curr_pos[0], self.curr_pos[1]
        return [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]


class Beetle(Piece, ABC):
    def __init__(self, curr_pos):
        super().__init__(curr_pos)

    def allowed_movements(self):
        x, y = self.curr_pos[0], self.curr_pos[1]
        return [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]


class Spider(Piece, ABC):
    def __init__(self, curr_pos):
        super().__init__(curr_pos)

    def allowed_movements(self):
        pass
