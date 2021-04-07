from game.helpers.color import Color


class ScreenObject:
    points = []

    def __init__(self, game, color, special_colour=Color.gold):
        from game.game import Game
        if isinstance(game, Game):
            self.game = game
            self.color = color
            self.special_colour = special_colour
        else:
            raise Exception("Pass valid Game object to the constructor")

    def draw(self, surface):
        for point in self.points:
            colour = self.special_colour if point.is_special else self.color
            self.game.draw_pixel(surface, colour, point)


class SnakeScreenObject(ScreenObject):
    def __init__(self, game):
        ScreenObject.__init__(self, game, Color.green)


class WallScreenObject(ScreenObject):
    def __init__(self, game):
        ScreenObject.__init__(self, game, Color.black)


class FruitScreenObject(ScreenObject):
    def __init__(self, game):
        ScreenObject.__init__(self, game, Color.red)
