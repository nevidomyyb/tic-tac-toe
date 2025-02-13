from board import Board
from time import time
import math
import random

class Node():
    
    #'l' for line
    #'c' for column
    #'s' for symbol (X or O)
    def __init__(self, board: Board, last_move: list['l', 'c', 's'], parent: 'Node'):
        self.board = board
        self.last_move = last_move
        self.n_visits = 0
        self.n_wins = 0
        self.childs : list['Node'] = []
        self.parent = parent        

class Computer():
    
    def __init__(self, board: Board, last_move):
        self.root = Node(
            board,
            last_move, []
        )
        
    def uct(self, node: Node):
        if node.n_visits == 0:
            return float('inf')
    
        win_rate = node.n_wins / node.n_visits
        exploration_term = math.sqrt(2) * math.sqrt(math.log(node.parent.n_visits) / node.n_visits)
        return win_rate + exploration_term
    
    def selection(self, node: Node):
        if not node.childs:
            return node
        best_child = max(node.childs, key=self.uct)
        return self.selection(best_child)
            
    def backpropagation(self, node: Node, win: bool):
        win_value = 1 if win else 0
        node.n_wins += win_value
        node.n_visits += 1
        
        if node.parent:
            self.backpropagation(node.parent, win)
            
    def expansion(self, node: Node):
        
        board = node.board
        possibles_moves = [(r, c) for r in range(3) for c in range(3) if not board.check_position(c, r)]
        if not possibles_moves:
            if board.check_winner() == "X":
                win = True
            else:
                win = False
            
            self.backpropagation(node, win)
            return node

        r, c = random.choice(possibles_moves)
        next_symbol = "O" if sum(1 for row in board.board for cell in row if cell != "") % 2 == 0 else "X"
        new_board = Board(board.width, board.height, [row[:] for row in board.board])
        new_board.mark_position(c, r, next_symbol)
        new_node = Node(new_board, [r, c, next_symbol], node)
        node.childs.append(new_node)
        
        if new_board.is_full():
            if new_board.check_winner() == "X":
                win = True
            else: win = False
            self.backpropagation(new_node, win)
        
        return new_node
    
    def print_tree(self, node: Node):
        print(node.board.board)
        print(node.last_move)
        print(node.childs)
        for child in node.childs:
            self.print_tree(child)
        print('------------------------------')
    
    def MCTS(self):
        for c in range(0,100):
            selected_node = self.selection(self.root)
            expanded_node = self.expansion(selected_node)
            
            
            
    def best_move(self):
        self.MCTS()
        self.print_tree(self.root)
        best_child = max(self.root.childs, key= lambda child: child.n_wins)
        return best_child.last_move
    
    def ai_move(self, callback):
        start = time()
        move = self.best_move()
        print(f"Move: {move} | Type: {type(move)}")
        print(f"Take : {time()-start:.5f} seconds to think.")
        if move:
            print(f"Board to play (mcts) : {self.root.board}")
            self.root.board.mark_position(move[1], move[0], "X")
        callback()
        
            
        