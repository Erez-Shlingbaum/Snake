import random
import sys
import time

import pygame as pyg

from Snake.Snake import Snake


class Game:
    def __init__(self, setting):
        self.setting = setting

        self.screen = self.init_setting()
        self.snake = self.init_snake()
        self.apple_image = self.init_food()
        self.food_rect = self.apple_image.get_rect()

        self.food_position = self.generate_food_position()
        self.food_rect = self.food_rect.move(self.food_position[0], self.food_position[1])

        self.current_direction = "Right"
        self.current_time = pyg.time.get_ticks()

    def start(self):
        while True:
            self.handle_events()
            self.update_logic()
            self.draw()

    def handle_events(self):
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                sys.exit()
            if event.type == pyg.KEYDOWN:
                direction_came_from = self.snake.get_direction_came_from()
                if event.key == pyg.K_UP and "Up" != direction_came_from:
                    self.current_direction = "Up"
                elif event.key == pyg.K_DOWN and "Down" != direction_came_from:
                    self.current_direction = "Down"
                elif event.key == pyg.K_LEFT and "Left" != direction_came_from:
                    self.current_direction = "Left"
                elif event.key == pyg.K_RIGHT and "Right" != direction_came_from:
                    self.current_direction = "Right"

    def update_logic(self):
        is_snake_moved, should_generate_food = self.handle_game_logic()
        if is_snake_moved:
            if self.check_fail():
                self.lose_game()
                time.sleep(0.5)
                sys.exit()
            if should_generate_food:
                self.food_position = self.generate_food_position()
                self.food_rect.x = self.food_position[0]
                self.food_rect.y = self.food_position[1]
            self.current_time = pyg.time.get_ticks()

    def draw(self):
        self.screen.fill(self.setting.background_color)
        self.snake.draw()
        self.screen.blit(self.apple_image, self.food_rect)
        pyg.display.flip()

    def init_setting(self):
        pyg.init()
        screen = pyg.display.set_mode(self.setting.screen_size)
        return screen

    def init_snake(self):
        head_image = pyg.image.load("Resources/snake_head.png")
        body_image = pyg.image.load("Resources/snake_body.png")

        head_image = pyg.transform.scale(head_image, (self.setting.cell_size, self.setting.cell_size))
        body_image = pyg.transform.scale(body_image, (self.setting.cell_size, self.setting.cell_size))

        snake = Snake(self.screen, self.setting.cell_size, self.setting.center_position, head_image,
                      body_image)
        snake.add_body_part("Right")
        snake.add_body_part("Right")
        return snake

    def init_food(self):
        apple_image = pyg.image.load("Resources/apple.png")
        apple_image = pyg.transform.scale(apple_image, (self.setting.cell_size, self.setting.cell_size))
        return apple_image

    def check_fail(self):
        """
        This function checks if the user lost the game.
        This function assumes the snake already moved before calling, and might be on a bad position
        """
        front = self.snake.get_front_part()

        # Check if snake collided with the screen border
        x_snake, y_snake = front.current_position
        if x_snake < 0 or x_snake > self.setting.screen_width or y_snake < 0 or y_snake > self.setting.screen_height:
            return True

        # Check snake collision
        for body_part in self.snake.body_parts:
            if front != body_part and front.current_position == body_part.current_position:
                return True
        return False

    def is_food_on_snake(self, food_position):
        """
        Helper function for generate_food_position(...)
        """
        if food_position is None:
            return False
        # Check if the food_position equals to one of the snake body parts position
        for part in self.snake.body_parts:
            if food_position == part.current_position:
                return True
        return False

    def generate_food_position(self):
        def gen_position():
            col_range = self.setting.col_count - 1
            row_range = self.setting.row_count - 1
            return random.randint(0, col_range) * self.setting.cell_size, random.randint(0,
                                                                                         row_range) * self.setting.cell_size

        new_position = gen_position()
        while self.is_food_on_snake(new_position):
            new_position = gen_position()
        return new_position

    # TODO: encapsulate return value in a class or make a better function
    def handle_game_logic(self):
        """
        This function return True if the snake moved
        :return (snake_moved : bool, should_generate_new_food):
        """
        if pyg.time.get_ticks() - self.current_time >= self.setting.game_tick_time:  # if snake should move.
            self.snake.move(self.current_direction)
            if self.is_food_on_snake(self.food_position):
                self.snake.add_body_part(self.current_direction)
                return True, True  # We need to generate new food!
            return True, False
        return False, False

    def lose_game(self):
        print("LOSE")
        game_over = pyg.image.load("Resources/gameover.png")
        game_over = pyg.transform.scale(game_over, (self.setting.screen_width, self.setting.screen_height))
        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over, game_over.get_rect())
        pyg.display.flip()
