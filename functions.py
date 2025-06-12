import platform
import pygame
import chess
import chess.engine
import sys

try:
    import pygame.gfxdraw
    GFXDRAW_AVAILABLE = True
except ImportError:
    GFXDRAW_AVAILABLE = False

# Настройки окна и доски
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
FPS = 120

# Цвета
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
HIGHLIGHT = (158, 158,158, 158)
POPUP_BG = (200, 200, 200, 200)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER = (150, 150, 150)



def highlight_squares(screen, board, selected_square, player_color):
    if selected_square is None:
        return

    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    center = (SQUARE_SIZE // 2, SQUARE_SIZE // 2)
    radius = SQUARE_SIZE // 5
    if GFXDRAW_AVAILABLE:
        pygame.gfxdraw.aacircle(s, center[0], center[1], radius, HIGHLIGHT)
        pygame.gfxdraw.filled_circle(s, center[0], center[1], radius, HIGHLIGHT)
    else:
        pygame.draw.circle(s, HIGHLIGHT, center, radius)
    moves = [move for move in board.legal_moves if move.from_square == selected_square]
    for move in moves:
        x, y = square_to_coords(move.to_square, player_color)
        screen.blit(s, (x, y))

# Загрузка изображений фигур

def load_images():
    pieces = {}
    dirs = ['Black Pieces', 'White Pieces']
    names = ['B', 'K', 'N', 'P', 'Q', 'R']
    for dir in dirs:
        color_prefix = 'w' if 'White' in dir else 'b'
        for name in names:
            try:
                img = pygame.image.load(f'assets/{dir}/{name}.png').convert_alpha()
                img = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
                pieces[color_prefix + name] = img
            except FileNotFoundError:
                continue
    return pieces

# Отрисовка доски
def draw_board(screen, player_color):
    colors = [WHITE, BROWN]
    for rank in range(8):
        for file in range(8):
            color = colors[(rank + file) % 2]
            rect = pygame.Rect(file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

# Конвертация шахматных координат в пиксели
def square_to_coords(square, player_color):
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    if player_color == chess.WHITE:
        x = file * SQUARE_SIZE
        y = (7 - rank) * SQUARE_SIZE
    else:
        x = (7 - file) * SQUARE_SIZE
        y = rank * SQUARE_SIZE
    return x, y

# Отрисовка фигур
def draw_pieces(screen, board, images, player_color):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            x, y = square_to_coords(square, player_color)
            name = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()
            img = images[name]
            offset_x = (SQUARE_SIZE - img.get_width()) // 2
            offset_y = (SQUARE_SIZE - img.get_height()) // 2
            screen.blit(img, (x + offset_x, y + offset_y))


# Анимация хода
def animate_move(screen, images, board, move, player_color, speed=25):
    start_x, start_y = square_to_coords(move.from_square, player_color)
    end_x, end_y = square_to_coords(move.to_square, player_color)
    piece = board.piece_at(move.from_square)
    if not piece:  # Проверка на наличие фигуры
        return
    name = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()

    clock = pygame.time.Clock()
    steps = speed
    for i in range(1, steps + 1):
        t = i / steps
        cur_x = start_x + (end_x - start_x) * t
        cur_y = start_y + (end_y - start_y) * t
        screen.fill((0, 0, 0))  # Очистка экрана
        draw_board(screen, player_color)
        draw_pieces(screen, board, images, player_color)
        img = images[name]
        offset_x = (SQUARE_SIZE - img.get_width()) // 2
        offset_y = (SQUARE_SIZE - img.get_height()) // 2
        screen.blit(img, (cur_x + offset_x, cur_y + offset_y))
        pygame.display.flip()
        clock.tick(FPS)

# Преобразование координат мыши в клетку
def mouse_to_square(pos, player_color):
    x, y = pos
    file = x // SQUARE_SIZE
    rank = y // SQUARE_SIZE
    if file < 0 or file > 7 or rank < 0 or rank > 7:  # Проверка границ
        return None
    if player_color == chess.WHITE:
        square = chess.square(file, 7 - rank)
    else:
        square = chess.square(7 - file, rank)
    return square

# Отрисовка всплывающего окна
def draw_popup(screen, message):
    popup = pygame.Surface((300, 150), pygame.SRCALPHA)
    popup.fill(POPUP_BG)
    font = pygame.font.Font("assets/fonts/Montserrat.ttf", 32)
    text = font.render(message, True, (0, 0, 0))
    popup.blit(text, (150 - text.get_width() // 2, 50 - text.get_height() // 2))
    restart_text = font.render("Restart? (Y/N)", True, (0, 0, 0))
    popup.blit(restart_text, (150 - restart_text.get_width() // 2, 100 - restart_text.get_height() // 2))
    screen.blit(popup, (WIDTH // 2 - 150, HEIGHT // 2 - 75))

# Отрисовка меню выбора стороны
def draw_side_selection(screen, mouse_pos):
    font = pygame.font.Font("assets/fonts/Montserrat.ttf", 32)

    button = (150, 60)
    offset_x = 30
    offset_y = 60
    buttons_offset_x = (
        WIDTH // 2 - offset_x - button[0],
        WIDTH // 2 + offset_x
    )
    buttons_offset_y = HEIGHT // 2 - offset_y
    white_button = pygame.Rect(buttons_offset_x[0], buttons_offset_y, button[0], button[1])
    black_button = pygame.Rect(buttons_offset_x[1], buttons_offset_y, button[0], button[1])

    white_color = BUTTON_HOVER if white_button.collidepoint(mouse_pos) else BUTTON_COLOR
    black_color = BUTTON_HOVER if black_button.collidepoint(mouse_pos) else BUTTON_COLOR

    pygame.draw.rect(screen, white_color, white_button)
    pygame.draw.rect(screen, black_color, black_button)

    white_text = font.render("White", True, (255, 255, 255))
    black_text = font.render("Black", True, (255, 255, 255))
    screen.blit(white_text, (white_button.x + 20, white_button.y + 10))
    screen.blit(black_text, (black_button.x + 20, black_button.y + 10))

    return white_button, black_button

# Отрисовка ползунка сложности
def draw_difficulty_slider(screen, mouse_pos, difficulty):
    font = pygame.font.Font("assets/fonts/Montserrat.ttf", 28)

    slider = (200, 20)
    knob = (10,30)
    slider_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, slider[0], slider[1])
    knob_rect = pygame.Rect(WIDTH // 2 - 100 + difficulty * 10, HEIGHT // 2 + 15, knob[0], knob[1])

    knob_color = BUTTON_HOVER if knob_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, BUTTON_COLOR, slider_rect)
    pygame.draw.rect(screen, knob_color, knob_rect)

    diff_text = font.render(f"Difficulty: {difficulty}", True, (0, 0, 0))
    screen.blit(diff_text, (WIDTH // 2 - diff_text.get_width() // 2, HEIGHT // 2 + 50))

    return slider_rect, knob_rect
