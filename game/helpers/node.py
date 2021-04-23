from game.helpers.point import Point


class Node:
    point = None
    previous_node = None
    action = None

    def __init__(self, point: Point, action=None, previous_node=None):
        self.point = point
        self.action = action
        self.previous_node = previous_node

    def __eq__(self, other):
        return self.point == other.point

    def __hash__(self):
        return hash(str(self.point.x) + str(self.point.y))

    def copy(self):
        return Node(Point(self.point.x, self.point.y), self.action, self.previous_node)
