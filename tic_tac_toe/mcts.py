import math
import random
from board import Board 
from time import time

class Node:
    def __init__(self, board: Board, last_move=None, parent=None):
        self.board = board
        self.last_move = last_move  # (row, col, symbol)
        self.n_visits = 0
        self.n_wins = 0
        self.children = []
        self.parent = parent
    
    def is_fully_expanded(self):
        return len(self.children) == len(self.get_possible_moves())
    
    def get_possible_moves(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board.check_position(c, r) == True]
    
    def is_terminal(self) -> bool:
        return self.board.check_winner != "" and self.is_fully_expanded()
    
class MCTS:
    def __init__(self, board: Board, simulations=100):
        self.root = Node(board)
        self.simulations = simulations
    
    def uct(self, node: Node):
        if node.n_visits == 0:
            return float('inf')
        win_rate = node.n_wins / node.n_visits
        exploration = math.sqrt(math.log(node.parent.n_visits) / node.n_visits)
        return win_rate + math.sqrt(2) * exploration

    def selection(self, node: Node):
        print('Selecting node')
        if not node.children:
            return node
        best_child = max(node.children, key=lambda child: self.uct(child))
        print('Selected completed')
        return self.selection(best_child)
    
    def backpropagation(self, node: Node, win: bool):
        win_value = 1 if win else 0
        node.n_wins += win_value
        node.n_visits += 1
        
        if node.parent:
            self.backpropagation(node.parent, win)
            
    def expansion(self, node: Node):
        print('Expansion process')
        possible_moves = [
            (r, c) for r in range(3) for c in range(3) if node.board.check_position(c, r) == True
        ]
        if len(possible_moves) == 0:
            return node
        move = random.choice(possible_moves)
        row = move[0]
        column = move[1]
        next_symbol = "O" if sum(1 for row in node.board.board for cell in row if cell != "") % 2 == 0 else "X"
        new_board = Board(node.board.width, node.board.height, [row[:] for row in node.board.board])
        new_board.mark_position(column, row, next_symbol)
        new_node = Node(
            new_board, (row, column, next_symbol, node)
        )
        node.children.append(new_node)
        print('Expansion finished')
        return new_node
        
    def simulate(slef, node: Node):
        print('Simulation process')
        new_board = Board(node.board.width, node.board.height, [row[:] for row in node.board.board])
        possible_moves = [
            (r, c) for r in range(3) for c in range(3) if new_board.check_position(c, r) == True
        ]
        # print(possible_moves)
        # return False
        while len(possible_moves) > 0 or new_board.check_winner() == "":
            print(f'Having {len(possible_moves)}')
            print(f'Winner: {new_board.check_winner()}')
            move = random.choice(possible_moves)
            row = move[0]
            column = move[1]
            next_symbol = "O" if sum(1 for row in new_board.board for cell in row if cell != "") % 2 == 0 else "X"
            print(f'Going to mark the position: {row}, {column} with: {next_symbol}')
            new_board.mark_position(column, row, next_symbol)
            print(new_board.board)
            
            possible_moves = [
                (r, c) for r in range(3) for c in range(3) if new_board.check_position(c, r) == True
            ]
        print('Simulation finished')
        return new_board.check_winner() == "X"

    def run(self):
        node = self.root
        for i in range(self.simulations):
            print(f"Running simulation: {i}")
            node = self.selection(node)
            if node.is_terminal():
                break
            node = self.expansion(node)
            win = self.simulate(node)
            print('Backpropagation')
            self.backpropagation(node, win)
            print('Backpropagated')
        return self.root
            
        
    def best_move(self):
        return max(self.root.children, key=lambda child: child.n_visits)