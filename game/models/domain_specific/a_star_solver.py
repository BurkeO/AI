from game.environment.tile import Tile
from game.helpers.node import Node
from game.helpers.point import Point
from game.helpers.queue import Queue
from game.models.base_game_model import BaseGameModel
from game.helpers.priority_queue import PriorityQueue
from game.environment.environment import Environment


class AStarSolver(BaseGameModel):
    def __init__(self):
        super().__init__("A Star", "a_star", "star")

    def move(self, environment):
        super().move(environment)
        a_star_path = self.a_star(environment, self.starting_node, self.fruit_node)
        if a_star_path:
            self.transposition_table[self.fruit_node] = a_star_path
            first_point = a_star_path[-2]
            return first_point.action
        return environment.snake_action

    def a_star(self, environment: Environment, starting_node: Node, fruit_node: Node):
        # TODO change heuristic from just saying 0 each time
        heuristic = 0
        queue = PriorityQueue()
        point_to_running_weight = {}
        start = starting_node
        if start == fruit_node:
            return self._recreate_path_for_node(start)
        point_to_running_weight[start.point] = 0
        queue.push(start, heuristic)
        while queue.isEmpty() is False:
            current_node = queue.pop()
            if current_node == fruit_node:
                return self._recreate_path_for_node(current_node)
            for action in environment.possible_actions_for_current_action(current_node.action):
                child_node_point = Point(current_node.point.x + action[0], current_node.point.y + action[1])
                if child_node_point not in point_to_running_weight or child_node_point == fruit_node.point:
                    neighbor = environment.tiles[child_node_point.y][child_node_point.x]
                    if neighbor == Tile.empty or neighbor == Tile.fruit:
                        child_node = Node(child_node_point, action, previous_node=current_node)
                        if child_node.point not in point_to_running_weight:
                            queue.push(child_node, point_to_running_weight[current_node.point] + 1 + heuristic)
                            point_to_running_weight[child_node.point] = point_to_running_weight[current_node.point] + 1
        return []

