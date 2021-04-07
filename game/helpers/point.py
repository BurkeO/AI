from game.environment.action import Action


class Point:

    def __init__(self, x, y, is_special=False):
        self.x = x
        self.y = y
        self.is_special = is_special

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self.x) + str(self.y))

    def move(self, action: Action):
        return Point(self.x + action.value[0], self.y + action.value[1], self.is_special)
