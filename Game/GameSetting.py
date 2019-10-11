class GameSetting:
    def __init__(self, background_color, screen_size, cell_size, game_tick_time):
        self.background_color = background_color
        self.screen_size = screen_size
        self.screen_width, self.screen_height = screen_size
        self.cell_size = cell_size

        self.col_count = screen_size[0] // cell_size
        self.row_count = screen_size[1] // cell_size

        self.score_position = cell_size * int((self.col_count * 0.2)), cell_size * int((self.row_count * 0.8))

        self.center_position = cell_size * (self.col_count // 2), cell_size * (self.row_count // 2)

        self.game_tick_time = game_tick_time
