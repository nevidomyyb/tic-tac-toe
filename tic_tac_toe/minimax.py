from board import Board
import copy

class Computer():
    
    def ai_move(self, board: Board, callback):
        b = Board(board.width, board.height, [row[:] for row in board.board])
        move = self.best_move(b)
        if move:
            board.mark_position(move[1], move[0], "X")
        callback()
    
    def minimax(self, board: Board, depth, is_maximazing, max_depth=10):
        
        winner = board.check_winner()
        if winner == "X":
            return 1
        elif winner == "O":
            return -1
        elif board.is_full():
            return 0
        
        if depth >= max_depth:
            return 0 
        
        if is_maximazing:
            best_score = -float('inf')
            for row in range(3):
                for col in range(3):
                    if board.check_position(col, row):
                        board.board[row][col] = "X"
                        score = self.minimax(board, depth+1, False)
                        board.board[row][col] = ""
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board.check_position(col, row):
                        board.board[row][col] = "O"
                        score = self.minimax(board, depth + 1,True)
                        board.board[row][col] = ""
                        best_score = min(best_score, score)
            return best_score 
        
    def best_move(self, board: Board):
        best_score = -float('inf')
        move = None
        for row in range(3):
            for col in range(3):
                if board.check_position(col, row):
                    board.board[row][col] = "X"
                    score = self.minimax(board, 0, False)
                    board.board[row][col] = ""
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        return move