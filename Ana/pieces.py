from abc import abstractmethod, ABC


class Piece:
    def __init__(self, name, color, curr_pos):
        self.name = name
        self.color = color
        # coords where it is positioned on the board
        self.curr_pos = curr_pos

    @abstractmethod
    def check_valid_move(self, new_pos):
        raise NotImplementedError("This method should not be called directly.")


class Queen(Piece, ABC):
    # each piece should have different number of it, saved as a static counter
    total_num = 0

    def __init__(self, name, color, curr_pos):
        super().__init__(name, color, curr_pos)
        self.total_limit = 1
        Queen.total_num += 1

    def allowed_movements(self):
        x, y = self.curr_pos[0], self.curr_pos[1]
        return [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]

    def check_valid(self, new_pos):
        return new_pos in self.allowed_movements()


class Beetle(Piece, ABC):
    total_num = 2

    def __init__(self, name, color, curr_pos):
        super().__init__(name, color, curr_pos)
        self.total_limit = 1
        Beetle.total_num += 1

    def allowed_movements(self):
        x, y = self.curr_pos[0], self.curr_pos[1]
        return [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]

    def check_valid(self, new_pos):
        return new_pos in self.allowed_movements()


class Spider(Piece, ABC):
    total_num = 2

    def __init__(self, name, color, curr_pos):
        super().__init__(name, color, curr_pos)
        self.total_limit = 1
        Queen.total_num += 1

    def check_valid(self, new_pos):
        pass

    def allowed_movements(self):
        pass
