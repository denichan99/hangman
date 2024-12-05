from graphics import game_loop
from mechanics import get_random_word

if __name__ == "__main__":
    word = get_random_word()
    game_loop(word)
