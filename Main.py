# Game Constants
from Game import Game, GameSetting


def main():
    background_color = 0, 0, 0
    screen_width, screen_height = screen_size = 800, 600
    cell_size = 25  # pixels (size of snake body part)

    col_count = screen_size[0] // cell_size
    row_count = screen_size[1] // cell_size

    # Snake Constants
    center_position = cell_size * (col_count // 2), cell_size * (row_count // 2)
    game_tick_time = 200  # milliseconds

    # Start the game
    game = Game.Game(GameSetting.GameSetting(background_color, screen_size, cell_size, game_tick_time))
    game.start()


if __name__ == "__main__":
    main()
