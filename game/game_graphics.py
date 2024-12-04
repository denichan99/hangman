import pygame
import sys
from game_logic import initialize_game, get_display_word, is_game_over, process_guess

# Константы
WIDTH, HEIGHT = 1000, 600  # Увеличен размер экрана
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Правильный маппинг символов для русской раскладки с дополнительными клавишами
RUSSIAN_KEYMAP = {
    pygame.K_a: 'ф', pygame.K_b: 'и', pygame.K_c: 'с', pygame.K_d: 'в', pygame.K_e: 'у',
    pygame.K_f: 'а', pygame.K_g: 'п', pygame.K_h: 'р', pygame.K_i: 'ш', pygame.K_j: 'о',
    pygame.K_k: 'л', pygame.K_l: 'д', pygame.K_m: 'ь', pygame.K_n: 'т', pygame.K_o: 'щ',
    pygame.K_p: 'з', pygame.K_q: 'й', pygame.K_r: 'к', pygame.K_s: 'ы', pygame.K_t: 'е',
    pygame.K_u: 'г', pygame.K_v: 'м', pygame.K_w: 'ц', pygame.K_x: 'ч', pygame.K_y: 'н',
    pygame.K_z: 'я',
    pygame.K_LEFTBRACKET: 'х',  # '[' на английской раскладке -> 'х'
    pygame.K_RIGHTBRACKET: 'ъ',  # ']' на английской раскладке -> 'ъ'
    pygame.K_SEMICOLON: 'ж',  # ';' на английской раскладке -> 'ж'
    pygame.K_QUOTE: 'э',  # '\'' на английской раскладке -> 'э'
    pygame.K_COMMA: 'б',  # ',' на английской раскладке -> 'б'
    pygame.K_PERIOD: 'ю',  # '.' на английской раскладке -> 'ю',
}

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Виселица")
font = pygame.font.Font(None, 36)


def draw_hangman(attempts_left):
    """Отображает виселицу в зависимости от оставшихся попыток"""
    if attempts_left < 7:
        pygame.draw.line(screen, BLACK, (10, 340), (90, 340), 5)
        pygame.draw.line(screen, BLACK, (50, 50), (50, 340), 5)  # Столб
        pygame.draw.line(screen, BLACK, (50, 50), (150, 50), 5)  # Брус
        pygame.draw.line(screen, BLACK, (150, 50), (150, 100), 5)  # Веревка
    if attempts_left < 6:
        pygame.draw.circle(screen, BLACK, (150, 130), 30, 5)  # Голова
    if attempts_left < 5:
        pygame.draw.line(screen, BLACK, (150, 160), (150, 260), 5)  # Тело
    if attempts_left < 4:
        pygame.draw.line(screen, BLACK, (150, 180), (120, 240), 5)  # Левая рука
    if attempts_left < 3:
        pygame.draw.line(screen, BLACK, (150, 180), (180, 240), 5)  # Правая рука
    if attempts_left < 2:
        pygame.draw.line(screen, BLACK, (150, 260), (125, 310), 5)
    if attempts_left < 1:
        pygame.draw.line(screen, BLACK, (150, 260), (175,310), 5)


def draw_game_state(game_state, message):
    """Отображает текущее состояние игры"""
    screen.fill(WHITE)

    # Отображение оставшихся попыток
    attempts_text = f"Осталось попыток: {game_state['attempts_left']}"
    attempts_surface = font.render(attempts_text, True, BLACK)
    screen.blit(attempts_surface, (WIDTH - 300, 50))  # Сдвигаем надпись в правую верхнюю часть

    # Отображение слова в левой верхней части
    display_word = get_display_word(game_state)
    word_surface = font.render(display_word, True, BLACK)
    screen.blit(word_surface, (500, 300))  # Сдвигаем слово в левую верхнюю часть

    # Отображение виселицы
    draw_hangman(game_state['attempts_left'])

    # Отображение сообщения
    message_surface = font.render(message, True, GRAY)
    screen.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, 400))

    # Разделение алфавита на три ряда и их отображение
    rows = [
        "й ц у к е н г ш щ з х ъ",
        "ф ы в а п р о л д ж э",
        "я ч с м и т ь б ю"
    ]

    row_height = 40  # Высота одного ряда
    start_x = (WIDTH - 450) // 2  # Для выравнивания по центру
    start_y = HEIGHT - 125  # Начальная позиция для букв

    for row_index, row in enumerate(rows):
        x_pos = start_x
        y_pos = start_y + (row_height * row_index)

        for letter in row.split():
            color = GRAY if letter in game_state["guessed_letters"] else BLACK
            letter_surface = font.render(letter, True, color)
            screen.blit(letter_surface, (x_pos, y_pos))
            x_pos += 40  # Сдвиг по горизонтали


def handle_user_input(game_state, message):
    """Обрабатывает ввод пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:  # Обрабатываем нажатие клавиши
            guess = None

            # Получаем символ, соответствующий нажатой клавише
            if event.key in RUSSIAN_KEYMAP:
                guess = RUSSIAN_KEYMAP[event.key]

            if guess and guess.isalpha():  # Если буква валидная
                message = process_guess(game_state, guess)

    return message


def game_loop(word):
    """Основной игровой цикл"""
    game_state = initialize_game(word)
    clock = pygame.time.Clock()
    message = ""  # Сообщение для отображения

    while not is_game_over(game_state):
        # Обрабатываем ввод пользователя
        message = handle_user_input(game_state, message)

        # Отображаем состояние игры
        draw_game_state(game_state, message)

        pygame.display.flip()
        clock.tick(FPS)

    # Завершение игры
    if all(letter in game_state["guessed_letters"] for letter in game_state["word"]):
        win_text = "Поздравляю! Вы победили!"
        win_surface = font.render(win_text, True, GREEN)
        screen.blit(win_surface, (WIDTH // 2 - win_surface.get_width() // 2, 400))
    else:
        lose_text = "Вы проиграли! Загаданное слово: " + game_state["word"]
        lose_surface = font.render(lose_text, True, RED)
        screen.blit(lose_surface, (WIDTH // 2 - lose_surface.get_width() // 2, 400))

    pygame.display.flip()
    pygame.time.wait(2000)


if __name__ == "__main__":
    word = "питон"  # Для теста, можешь заменить на вызов get_random_word()
    game_loop(word)
