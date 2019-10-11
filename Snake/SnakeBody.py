class SnakeBody:
    def __init__(self, current_position, body_image):
        self.body_image = body_image
        self.current_position = current_position

    def draw(self, surface):
        rect = self.body_image.get_rect()
        rect.x, rect.y = self.current_position
        surface.blit(self.body_image, rect)

    def update_position(self, new_position):
        self.current_position = new_position
