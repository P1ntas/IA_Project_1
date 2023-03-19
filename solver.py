import sys


class Solver:

    def __init__(self, board):
        self.board = board

    def disjoint_groups_heuristic(self):
        counts = {}
        for piece in self.board.pieces:
            if not piece.joined:
                if piece.color not in counts:
                    counts[piece.color] = 1
                    stack = [(piece.row, piece.col)]
                    while stack:
                        row, col = stack.pop()
                        piece = next((p for p in self.board.pieces if p.row == row and p.col == col), None)
                        if piece and not piece.joined and piece.color == counts[piece.color]:
                            piece.joined = True
                            if row > 0:
                                stack.append((row - 1, col))
                            if row < self.board.height - 1:
                                stack.append((row + 1, col))
                            if col > 0:
                                stack.append((row, col - 1))
                            if col < self.board.width - 1:
                                stack.append((row, col + 1))
                else:
                    counts[piece.color] += 1
        return sum(counts.values())

    def count_unjoined_pieces_heuristic(self):
        return len([piece for piece in self.board.pieces if not piece.joined])

    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.board.win_condition():
            return self.count_unjoined_pieces_heuristic()

        if maximizing_player:
            best_value = -sys.maxsize
            for move in self.board.get_possible_moves():
                self.board.make_move(move)
                value = self.minimax(depth - 1, False)
                self.board.undo_move(move)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = sys.maxsize
            for move in self.board.get_possible_moves():
                self.board.make_move(move)
                value = self.minimax(depth - 1, True)
                self.board.undo_move(move)
                best_value = min(best_value, value)
            return best_value