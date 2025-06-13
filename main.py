import pygame
import chess
import chess.engine
import sys
import random

from functions import (
    WIDTH, HEIGHT, SQUARE_SIZE, FPS,
    WHITE, BROWN, HIGHLIGHT, POPUP_BG,
    BUTTON_COLOR, BUTTON_HOVER, load_images,
    draw_board, square_to_coords, draw_pieces,
    highlight_squares, animate_move, mouse_to_square,
    draw_popup, draw_side_selection, draw_difficulty_slider
)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess with AI")
    clock = pygame.time.Clock()
    images = load_images()
    board = chess.Board()

    difficulty = 5
    engine_path = "stockfish/stockfish"
    try:
        engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        engine.configure({"Skill Level": difficulty})
    except Exception as e:
        print(f"Ошибка загрузки Stockfish: {e}")
        pygame.quit()
        sys.exit()

    player_color = None
    selected_square = None
    waiting_for_player = True
    adjusting_difficulty = False
    game_over = False
    last_move = None

    # --- Выбор стороны и сложности ---
    while player_color is None:
        screen.fill((200, 200, 200))
        mouse_pos = pygame.mouse.get_pos()
        white_button, black_button = draw_side_selection(screen, mouse_pos)
        slider_rect, knob_rect = draw_difficulty_slider(screen, mouse_pos, difficulty)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                engine.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if white_button.collidepoint(mouse_pos):
                    player_color = chess.WHITE
                elif black_button.collidepoint(mouse_pos):
                    player_color = chess.BLACK
                elif knob_rect.collidepoint(mouse_pos):
                    adjusting_difficulty = True
            if event.type == pygame.MOUSEBUTTONUP:
                adjusting_difficulty = False
            if event.type == pygame.MOUSEMOTION and adjusting_difficulty:
                x, _ = mouse_pos
                difficulty = max(0, min(20, (x - (WIDTH // 2 - 100)) // 10))
                engine.configure({"UCI_LimitStrength": True})
                engine.configure({"Skill Level": difficulty})
                engine.configure({"UCI_Elo": 1320 + difficulty * 30})

        pygame.display.flip()
        clock.tick(FPS)

    if player_color == chess.BLACK:
        waiting_for_player = False
    else:
        waiting_for_player = True

    while True:
        game_over = board.is_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                engine.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and waiting_for_player and not game_over:
                pos = pygame.mouse.get_pos()
                square = mouse_to_square(pos, player_color)
                if square is None:
                    continue
                piece = board.piece_at(square)
                if selected_square is None:
                    if piece and piece.color == player_color:
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        try:
                            animate_move(screen, images, board, move, player_color)
                            board.push(move)
                            selected_square = None
                            waiting_for_player = False
                        except Exception as error:
                            print(f"Ошибка при ходе: {error}")
                            selected_square = None
                    else:
                        selected_square = None
            if event.type == pygame.KEYDOWN and game_over:
                if event.key in (pygame.K_y, pygame.K_z):
                    board.reset()
                    waiting_for_player = True
                    game_over = False
                elif event.key in (pygame.K_n, pygame.K_y):
                    pygame.quit()
                    engine.quit()
                    sys.exit()

        if not waiting_for_player and not game_over:
            try:
                result = engine.play(board, chess.engine.Limit(time=0.1))
                animate_move(screen, images, board, result.move, player_color)
                board.push(result.move)
                waiting_for_player = True

            except Exception as error:
                print(f"Ошибка хода ИИ: {error}")
                waiting_for_player = True

        screen.fill((0, 0, 0))
        draw_board(screen, player_color)
        highlight_squares(screen, board, selected_square, player_color)
        draw_pieces(screen, board, images, player_color)

        if game_over:
            outcome = board.outcome()
            if outcome:
                if outcome.winner == player_color:
                    draw_popup(screen, "You Win!")
                elif outcome.winner is None:
                    draw_popup(screen, "Draw!")
                else:
                    draw_popup(screen, "You Lose!")

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    pygame.init()
    main()
