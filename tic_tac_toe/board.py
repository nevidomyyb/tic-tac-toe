import pygame
import threading
import time

class Board():
    
    def __init__(self, width, height, board_matrix=None):
        if board_matrix is None:
            self.board = [
                ["", "", ""], 
                ["", "", ""], 
                ["", "", ""]
            ]
        else:
            self.board=board_matrix
        self.width = width
        self.height = height
        self.square_size = width // 3
        self.threads = []
        self.stop_thread = False
    
    def check_position(self, col, line):
        """
        return True if position is empty
        """
        if self.board[line][col] != "":
            return False
        return True
        
    def draw_lines(self, pygame: pygame, screen):
        pygame.draw.line(screen, 'black', (0, self.square_size), (self.width, self.square_size), 5)
        pygame.draw.line(screen, 'black', (0, 2*self.square_size), (self.width, 2*self.square_size), 5)
        pygame.draw.line(screen, 'black', (self.square_size, 0), (self.square_size, self.width), 5)
        pygame.draw.line(screen, 'black', (2*self.square_size, 0), (2*self.square_size, self.width), 5)
    
    def unmark_position(self, col, line):
        time.sleep(3)
        if self.stop_thread:
            return
        self.board[line][col] = ""
    
    def mark_position(self, col, line, symbol):
        if self.check_position(col, line):
            self.board[line][col] = symbol
            thread = threading.Thread(target=self.unmark_position, args=[col, line])
            thread.start()
            self.threads.append(thread)
            
    def stop_threads(self):
        self.stop_thread = True
        for thread in self.threads:
            thread.join()
        self.threads = []
        self.stop_thread = False
            
    def draw_figures(self, pygame: pygame, screen):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "O":
                    pygame.draw.circle(screen, 'red', (col * self.square_size + (self.square_size//2), row * self.square_size + (self.square_size//2)), 100, 5)
                elif self.board[row][col] == "X":
                    pygame.draw.line(
                        screen, 'purple', 
                        (col * self.square_size + 20, row * self.square_size + 20), 
                        (col * self.square_size + self.square_size - 20, row * self.square_size + self.square_size - 20), 
                    10)
                    pygame.draw.line(
                        screen, 'purple', 
                        (col * self.square_size + self.square_size - 20, row * self.square_size + 20), 
                        (col * self.square_size + 20, row * self.square_size + self.square_size - 20), 
                    10)
    
    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != "":
                return self.board[i][0]  
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != "":
                return self.board[0][i] 

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != "":
            return self.board[0][2]

        return ""
    
    def is_full(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "":  # Se houver ao menos um espaço vazio, o tabuleiro NÃO está cheio
                    return False
        return True