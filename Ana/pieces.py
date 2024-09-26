# from abc import abstractmethod, ABC
#
########## WILL NOT BE USED !!! ######################################
#
# class Piece:
#     def __init__(self, curr_pos):
#         self.curr_pos = curr_pos
#
#     @abstractmethod
#     def allowed_movements(self):
#         pass
#     def check_valid_move(self, new_pos):
#         raise NotImplementedError("This method should not be called directly.")
#
#
# class Queen(Piece):
#     def __init__(self, curr_pos):
#         super().__init__(curr_pos)
#
#     def allowed_movements(self):
#         x, y = self.curr_pos[0], self.curr_pos[1]
#         return [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]
#
# class Beetle(Piece):
#     def __init__(self, curr_pos):
#         super().__init__(curr_pos)
#
#     def allowed_movements(self):
#         x, y = self.curr_pos[0], self.curr_pos[1]
#         return [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]


