from abc import abstractmethod


class Bug:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def get_moves(self, current_state):
        raise NotImplementedError("This method should not be called directly.")


class Queen(Bug):
    # ((WhiteQueen, WhiteSpider1, WhiteSpider2, WhiteBeetle1, WhiteBeetle2, WhiteGrasshopper1, WhiteGrasshopper2, WhiteAnt1, WhiteAnt2, WhiteAnt3)
    #  (BlackQueen, BlackSpider1, BlackSpider2, BlackBeetle1, BlackBeetle2, BlackGrasshopper1, BlackGrasshopper2, BlackAnt1, BlackAnt2, BlackAnt3))

    def __init__(self, x, y):
        super().__init__(x, y)

    def get_moves(self, current_state):
        # [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]
        for tile_stack in current_state:
            if tile_stack[len(tile_stack) - 1] is None:




