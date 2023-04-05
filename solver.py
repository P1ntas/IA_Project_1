import sys
from collections import deque
from heapq import heappush, heappop
from queue import PriorityQueue
from copy import deepcopy

class Node:
    def __init__(self, board, depth, cost, move=None):
        self.board = board
        self.depth = depth
        self.cost = cost
        self.move = move
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(str(self.board))

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
            return None, self.count_unjoined_pieces_heuristic()
        
        if maximizing_player:
            best_value = -sys.maxsize
            best_move = None
            for move in self.board.get_possible_moves():
                if move == self.board.get_last_move():
                    continue
                self.board.make_move(move)
                _, value = self.minimax(depth - 1, False)
                self.board.undo_move()
                if value > best_value:
                    best_value = value
                    best_move = move
            return best_move, best_value
        else:
            best_value = sys.maxsize
            best_move = None
            for move in self.board.get_possible_moves():
                if move == self.board.get_last_move():
                    continue
                self.board.make_move(move)
                _, value = self.minimax(depth - 1, True)
                self.board.undo_move()
                if value < best_value:
                    best_value = value
                    best_move = move
            return best_move, best_value

    

    def bfs(self, board):
        # initialize queue with initial board
        queue = deque([(board, [])])

        # initialize set to keep track of visited states
        visited = set()

        # initialize node counter
        nodes_explored = 0

        while queue:
            # get next board and path from queue
            board, path = queue.popleft()

            # check if board is complete
            if board.win_condition():
                return path

            # generate children and add to queue if not visited before
            board.selected_tile = board.get_first_tile()
            if board.selected_tile is None:
                return path
            for move in board.get_possible_moves():
                new_board = board.copy()
                new_board.make_move(move)
                if new_board not in visited:
                    queue.append((new_board, path + [move]))
                    nodes_explored += 1
                    visited.add(new_board)

        # if no complete board is found, return None
        return None, nodes_explored


    def greedy(self, board):
        # initialize list of moves
        moves = []

        # repeat until game is complete
        while not board.win_condition():
            # get all possible moves
            possible_moves = board.get_possible_moves()
            if len(possible_moves) == 0:
                return moves
            # initialize best move and its score
            best_move = possible_moves[0]
            best_score = 0

            # evaluate all possible moves
            for move in possible_moves:
                new_board = board.copy()
                new_board.make_move(move)
                new_solver = Solver(new_board)
                score = new_solver.count_unjoined_pieces_heuristic()
                if score > best_score:
                    best_move = move
                    best_score = score

            # add best move to list of moves and update board
            moves.append(best_move)
            board.make_move(best_move)

        return moves

    
    def iterative_deepening(self, max_depth):
        best_move = None
        best_value = -sys.maxsize
        for depth in range(1, max_depth + 1):
            for move in self.board.get_possible_moves():
                self.board.make_move(move)
                value = self.minimax(depth, False)
                self.board.undo_move()
                if value > best_value:
                    best_value = value
                    best_move = move
        return best_move
    

    def astar(self):
        # initialize queue with initial board
        queue = deque([(self.board, [])])

        # initialize set to keep track of visited states
        visited = set()

        # initialize node counter
        nodes_explored = 0

        while queue:
            # get next board and path from queue
            board, path = queue.popleft()

            # check if board is complete
            if board.win_condition():
                return path, nodes_explored

            # generate children and add to queue if not visited before
            for move in board.get_possible_moves():
                new_board = board.copy()
                new_board.make_move(move)
                new_path = path + [move]
                if new_board not in visited:
                    queue.append((new_board, new_path))
                    nodes_explored += 1
                    visited.add(new_board)

            # sort queue based on f_score
            queue = deque(sorted(queue, key=lambda x: self.f_score(x[0], x[1])))

        # if no complete board is found, return None
        return None, nodes_explored

    def f_score(self, board, path):
        return len(path) + self.board.count_unjoined_pieces_heuristic()



