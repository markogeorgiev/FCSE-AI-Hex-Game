class Squares():
    def __init__(self, initial, goal):
        super().__init__(initial, goal)

    def move_block(self, block_coords, coords):
        x = block_coords[0] + coords[0]
        y = block_coords[1] + coords[1]

        if 0 <= x <= 4 and 0 <= y <= 4:
            return (x,y)
        return None

    @staticmethod
    def check_valid(state):
        for x, y in state:
            if x < 0 or x > 4 or y < 0 or y > 4:
                return False
        return True

    def successor(self, state):
        successors = dict()

        list_of_blocks = [i for i in state]
        directions = ["gore", "dolu", "levo", "desno"]
        coordinates = [(0,1),(0,-1),(-1,0),(1,0)]

        for i in range(0,5):
            for direction, coords in zip(directions, coordinates):
                new_block = self.move_block(list_of_blocks[i], coords)
                if new_block is not None:
                    tmp_list = [x for x in list_of_blocks]
                    tmp_list[i] = new_block
                    successors[f"Pomesti kvadratche {i + 1} {direction}"] = tuple(tmp_list)

        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    # def h(self, node):
    #     sum = 0
    #     for square, goal in zip(node.state, goal_state):
    #         sum+= abs(square[0] - goal[0]) + abs(square[1] - goal[1])
    #     return sum

    def goal_test(self, state):
        return state == self.goal