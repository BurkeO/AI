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

    def equal(self,second_node):
        x = second_node.point.x
        y = second_node.point.y
        if x == self.point.x and y== self.point.y:
            return True
        return False

    def connected(self,second_node):
        x = second_node.point.x
        y = second_node.point.y

        x_difference = abs(x-self.point.x)
        y_difference = abs(y-self.point.y)

        left_or_right = x_difference==1
        above_or_below = y_difference==1

        same_y = y_difference==0
        same_x = x_difference==0

        if same_x and above_or_below:
            return True
        if same_y and left_or_right:
            return  True
        return False
