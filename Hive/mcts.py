import math
import random
import copy



class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state  # Copy of game state
        self.parent = parent  # Parent node
        self.move = move  # Move taken to reach this state
        self.children = []  # Possible future states
        self.visits = 0  # How many times this node has been visited
        self.wins = 0  # How many times this node has won

    def uct_score(self, exploration_weight=1.4):
        if self.visits == 0:
            return float('inf')  # Ensure unvisited nodes are explored first
        return (self.wins / self.visits) + exploration_weight * math.sqrt(math.log(self.parent.visits) / self.visits)

    def best_child(self):
        return max(self.children, key=lambda child: child.uct_score())

def monte_carlo_tree_search(state, possible_moves, simulations=2):
    root = MCTSNode(copy.deepcopy(state))

    for _ in range(simulations):
        node = root
        temp_state = copy.deepcopy(state)

        # 1. Selection: Traverse tree using UCT
        while node.children:
            node = node.best_child()
            temp_state.get_tile_by_piece(node.move[0]).move_piece(node.move[1])
            temp_state.next_turn()

        # 2. Expansion: Add child nodes if game is not over
        if not is_terminal_state(temp_state):
            for move in possible_moves:
                new_state = copy.deepcopy(temp_state)
                new_state.get_tile_by_piece(move[0]).move_piece(move[1])
                new_state.next_turn()
                child_node = MCTSNode(new_state, parent=node, move=move)
                node.children.append(child_node)

            # Pick a random new child to simulate
            node = random.choice(node.children)

        # 3. Simulation: Play random moves until game ends
        result = simulate_random_game(temp_state)

        # 4. Backpropagation: Update node statistics
        while node:
            node.visits += 1
            node.wins += result  # Assuming +1 for win, 0 for loss
            node = node.parent

    # Return the best move found
    return root.best_child().move

def is_terminal_state(state):
    # Check if the game is over (someone won or it's a draw)
    return state.check_winner() is not None

def simulate_random_game(state):
    temp_state = copy.deepcopy(state)

    while not is_terminal_state(temp_state):
        pieces = temp_state.get_tiles_with_pieces(include_inventory=True)

        if not pieces:
            break  # No valid moves left

        moveable_piece = random.choice(pieces)
        valid_moves = moveable_piece.get_all_valid_moves(temp_state)
        if valid_moves:
            where_to_move = random.choice(valid_moves)
            temp_state.get_tile_by_piece(moveable_piece).move_piece(where_to_move)
            temp_state.next_turn()

    winner = temp_state.check_winner()
    return 1 if winner == "AI" else 0  # Assuming "AI" is your bot's player identifier
