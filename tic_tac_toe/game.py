import pygame
from board import Board
import threading

class Game():
    
    def start(self, ):
        pygame.init()
        WIDTH, HEIGHT = 720, 720

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        
        running = True
        board = Board(WIDTH, HEIGHT)
        
        game_over = False
        p0 = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if game_over:
                    print(board.check_winner())
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x, y = event.pos
                    col = x // board.square_size
                    line = y // board.square_size
                    if p0:
                        board.mark_position(col, line, "O")
                        p0 = False
                    else:
                        board.mark_position(col, line, "X")
                        p0 = True
                    
                    for l in board.board:
                        print(l)
                    winner = board.check_winner()
                    if winner == "X" or winner == "O":
                        game_over = True
                        thread = threading.Thread(target=board.stop_threads)
                        thread.start()
                        
            screen.fill("white")
            board.draw_lines(pygame, screen)
            board.draw_figures(pygame, screen)
            pygame.display.flip()