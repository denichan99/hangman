import random

def initialize_game(word): # Инициализирует игру
    return {
        "word": word,
        "guessed_letters": set(),
        "attempts_left": 7,
    }

def get_display_word(game_state): # Возвращает текущее состояние слова с учетом угаданных букв
    return " ".join(
        [letter if letter in game_state["guessed_letters"] else "_" for letter in game_state["word"]]
    )

def is_game_over(game_state): # Проверяет, завершена ли игра
    return game_state["attempts_left"] == 0 or all(
        letter in game_state["guessed_letters"] for letter in game_state["word"]
    )

def process_guess(game_state, guess): # Обрабатывает ввод буквы игроком
    if guess in game_state["guessed_letters"]:
        return "Вы уже пробовали эту букву."
    
    game_state["guessed_letters"].add(guess)
    
    if guess not in game_state["word"]:
        game_state["attempts_left"] -= 1
        return f"Ошибка! Буквы '{guess}' нет в слове."
    return f"Правильно! Буква '{guess}' есть в слове."

def get_random_word(filename='words.txt'):
    with open(filename, 'r', encoding = 'utf-8') as file:
        words = file.readlines()
    return random.choice(words).strip()
