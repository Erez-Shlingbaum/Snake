from Snake.SnakeBody import SnakeBody


class Snake:
    def __init__(self, surface, cell_size, initial_position, head_image, body_image):
        self.surface = surface
        self.body_image = body_image
        self.body_parts = [SnakeBody(initial_position, head_image)]
        self.directionDict = {
            "Left": lambda back, front: back.update_position(
                (front.current_position[0] - cell_size, front.current_position[1])),
            "Up": lambda back, front: back.update_position(
                (front.current_position[0], front.current_position[1] - cell_size)),
            "Right": lambda back, front: back.update_position(
                (front.current_position[0] + cell_size, front.current_position[1])),
            "Down": lambda back, front: back.update_position(
                (front.current_position[0], front.current_position[1] + cell_size))
        }

    def get_front_part(self):
        return self.body_parts[-1]

    def get_back_part(self):
        return self.body_parts[0]

    def get_direction_came_from(self):
        front_x, front_y = self.get_front_part().current_position
        second_x, second_y = self.body_parts[-2].current_position

        if front_x > second_x and front_y == second_y:
            return "Left"
        if front_x < second_x and front_y == second_y:
            return "Right"
        if front_x == second_x and front_y > second_y:
            return "Up"
        if front_x == second_x and front_y < second_y:
            return "Down"

    def move(self, direction):
        back = self.get_back_part()
        front = self.get_front_part()
        self.directionDict[direction](back, front)
        self.body_parts.pop(0)
        self.body_parts.append(back)

    def draw(self):
        for part in self.body_parts:
            part.draw(self.surface)

    def add_body_part(self, direction):
        """
        adds new body part in the direction specified (next to the front of this snake)
        * make sure that this function is called INSTEAD of the move function when needed
        """
        front = self.body_parts[-1]
        new_part = SnakeBody((0, 0), self.body_image)  # 0,0 does not matter...
        self.directionDict[direction](new_part, front)
        self.body_parts.append(new_part)
