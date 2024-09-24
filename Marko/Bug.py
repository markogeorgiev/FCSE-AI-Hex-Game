from abc import abstractmethod, ABC

class Bug:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def get_moves(self, current_state):
        raise NotImplementedError("This method should not be called directly.")

    @