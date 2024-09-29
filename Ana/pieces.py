from abc import abstractmethod


class Piece:
    def __init__(self, name):
        self.name = name # (color + piece type) ex. WhiteBeetle1 ; queen will be queen
        self.position = None
        self.color = 'white' if 'White' in self.name else 'black'

    def update_position(self, new_pos):
        self.position = new_pos

    @abstractmethod
    def allowed_movements(self, board, firstRound, secondRound):
        pass

class Queen(Piece):
    def allowed_movements(self, board, firstRound, secondRound):
        # move this into a seperate method for placing a piece, keep this one for moving a piece only.
        if firstRound:
            return board.show()
        elif secondRound:
            return board.get_adjacent_spaces(board.pieces[next(iter(board.pieces))].position)

        adjacent_spaces = board.get_adjacent_spaces(self.position)
        valid_moves = []
        for space in adjacent_spaces:
            if (board.is_empty(space) and
                board.has_adjacent_piece(space) and
                not board.breaks_hive(self.position, space)):
                valid_moves.append(space)
        return valid_moves

class Beetle(Piece):
    def allowed_movements(self, board, firstRound, secondRound):
        if firstRound:
            return board.show()
        elif secondRound:
            return board.get_adjacent_spaces(board.pieces[next(iter(board.pieces))].position)

        adjacent_spaces = board.get_adjacent_spaces(self.position)
        valid_moves = []
        for space in adjacent_spaces:
            if (board.has_adjacent_piece(space) and
                not board.breaks_hive(self.position, space)):
                valid_moves.append(space)
        return valid_moves

class Spider(Piece):
    def allowed_movements(self, board, firstRound, secondRound):
        if firstRound:
            return board.show()
        elif secondRound:
            return board.get_adjacent_spaces(board.pieces[next(iter(board.pieces))].position)

        valid_moves = set()
        visited = {self.position}
        self._dfs(board, self.position, 0, visited, valid_moves)
        return list(valid_moves)

    def _dfs(self, board, position, steps, visited, valid_moves):
        if steps == 3:
            valid_moves.add(position)
            return

        for neighbor in board.get_adjacent_spaces(position):
            if board.is_valid_slide(position, neighbor) and neighbor not in visited:
                visited.add(neighbor)
                self._dfs(board, neighbor, steps + 1, visited, valid_moves)
                visited.remove(neighbor)