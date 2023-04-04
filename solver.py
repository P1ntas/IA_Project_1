import sys
from queue import Queue
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
        print("minimax")
        if maximizing_player:
            best_value = -sys.maxsize
            best_move = None
            for move in self.board.get_possible_moves():
                self.board.make_move(move)
                _, value = self.minimax(depth - 1, False)
                self.board.undo_move(move)
                if value > best_value:
                    best_value = value
                    best_move = move
            return best_move, best_value
        else:
            best_value = sys.maxsize
            best_move = None
            for move in self.board.get_possible_moves():
                self.board.make_move(move)
                _, value = self.minimax(depth - 1, True)
                self.board.undo_move(move)
                if value < best_value:
                    best_value = value
                    best_move = move
            return best_move, best_value



    
    def bfs(self, board, depth):
        queue = Queue()
        visited = set()
        last_moves = {}
        queue.put((board, 0, True, None))
        best_value = -sys.maxsize
        best_path = []
        while not queue.empty():
            board, curr_depth, maximizing_player, parent = queue.get()
            if curr_depth == depth or board.win_condition():
                value = self.count_unjoined_pieces_heuristic()
                if maximizing_player:
                    if value > best_value:
                        best_value = value
                        best_path = [board]
                        while parent:
                            best_path.insert(0, parent)
                            parent = last_moves.get(parent)
                    elif value == best_value:
                        while parent:
                            best_path.insert(0, parent)
                            parent = last_moves.get(parent)
                else:
                    if value < best_value:
                        best_value = value
                        best_path = [board]
                        while parent:
                            best_path.insert(0, parent)
                            parent = last_moves.get(parent)
                    elif value == best_value:
                        while parent:
                            best_path.insert(0, parent)
                            parent = last_moves.get(parent)
            else:
                moves = board.get_possible_moves()
                for move in moves:
                    if move in last_moves and last_moves[move] == board:
                        continue
                    new_board = board.copy()
                    new_board.make_move(move)
                    if new_board in visited:
                        continue
                    visited.add(new_board)
                    last_moves[new_board] = board
                    queue.put((new_board, curr_depth + 1, not maximizing_player, board))
        return best_path


    def greddy(self):
        best_move = None
        best_value = -sys.maxsize
        for move in self.board.get_possible_moves():
            self.board.make_move(move)
            value = self.count_unjoined_pieces_heuristic()
            self.board.undo_move(move)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move
    
    def iterative_deepening(self, max_depth):
        best_move = None
        best_value = -sys.maxsize
        for depth in range(1, max_depth + 1):
            for move in self.board.get_possible_moves():
                self.board.make_move(move)
                value = self.minimax(depth, False)
                self.board.undo_move(move)
                if value > best_value:
                    best_value = value
                    best_move = move
        return best_move
    

    def a_star(self, depth):
        start_node = Node(self.board, 0, self.count_unjoined_pieces_heuristic())
        queue = PriorityQueue()
        queue.put(start_node)
        visited = set()
        
        while not queue.empty():
            node = queue.get()
            
            if node.board.win_condition() or node.depth == depth:
                return node.move
            
            if node.board not in visited:
                visited.add(node.board)
                moves = node.board.get_possible_moves()
                
                for move in moves:
                    new_board = node.board.copy()
                    new_board.make_move(move)
                    new_node = Node(new_board, node.depth+1, node.depth+1+self.count_unjoined_pieces_heuristic(), move)
                    
                    if new_board not in visited:
                        queue.put(new_node)
        
        return None


