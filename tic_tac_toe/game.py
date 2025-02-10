import pygame
from board import Board
import threading
from minimax import Computer
import time
class Game():
    
    def set_ai_thinking(self, value):
        global ai_thinking
        ai_thinking = value
        self.p0 = True
        
    
    def start(self, ):
        
        pygame.init()
        WIDTH, HEIGHT = 720, 720

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        
        running = True
        board = Board(WIDTH, HEIGHT)
        
        game_over = False
        self.p0 = True
        
        clock = pygame.time.Clock()
        
        computer = Computer()
        computer_thinking = False
        
        
        
        while running:
            screen.fill("white")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x, y = event.pos
                    col = x // board.square_size
                    line = y // board.square_size
                    if self.p0 and not game_over:
                        if board.check_position(col, line):
                            board.mark_position(col, line, "O")
                            self.p0 = False
                            computer_thinking = True
                            winner = board.check_winner()
                            if winner == "X" or winner == "O":
                                game_over = True
                            if not game_over:
                                threading.Thread(target=computer.ai_move, args=(board, lambda: self.set_ai_thinking(False))).start()

            clock.tick(60)
            board.draw_lines(pygame, screen)
            board.draw_figures(pygame, screen)
            pygame.display.flip()
            winner = board.check_winner()
            if winner == "X" or winner == "O":
                game_over = True
                thread = threading.Thread(target=board.stop_threads)
                thread.start()
                print(f"Winner: {winner}")
                time.sleep(3)
                pygame.quit()
                running = False
                        
            
            