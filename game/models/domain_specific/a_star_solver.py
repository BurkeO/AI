from typing import List

from game.environment.tile import Tile
from game.helpers.node import Node
from game.helpers.point import Point
from game.models.base_game_model import BaseGameModel
from game.helpers.priority_queue import PriorityQueue
from game.environment.environment import Environment
from math import sqrt


class AStarSolver(BaseGameModel):
    def __init__(self, test_name="", test_case=""):
        super().__init__("A Star", "a_star", "star", test_name, test_case)

    def move(self, environment):
        super().move(environment)
        a_star_path = self.a_star(environment, self.starting_node, self.fruit_nodes)
        if len(a_star_path) >= 2:
            for fruit_node in self.fruit_nodes:
                self.transposition_table[fruit_node] = a_star_path
            first_point = a_star_path[-2]
            return first_point.action
        return environment.snake_action

    def a_star(self, environment: Environment, starting_node: Node, fruit_nodes_list: List[Node]):
        heuristic = 0
        queue = PriorityQueue()
        point_to_running_weight = {}
        current_node = starting_node
        if current_node in fruit_nodes_list:
            return self._recreate_path_for_node(current_node)
        point_to_running_weight[current_node.point] = 0
        queue.push(current_node, heuristic)
        while queue.isEmpty() is False:
            current_node = queue.pop()
            if current_node in fruit_nodes_list:
                return self._recreate_path_for_node(current_node)
            for action in environment.possible_actions_for_current_action(current_node.action):
                child_node_point = current_node.point.move(action)
                if child_node_point not in point_to_running_weight or child_node_point in [node.point for node in
                                                                                           fruit_nodes_list]:
                    neighbor = environment.tiles[child_node_point.y][child_node_point.x]
                    if neighbor == Tile.empty or neighbor == Tile.fruit:
                        child_node = Node(child_node_point, action, previous_node=current_node)
                        if child_node.point not in point_to_running_weight:
                            for fruit_node in fruit_nodes_list:
                                queue.push(child_node, point_to_running_weight[current_node.point] + 1 +
                                           AStarSolver.heuristic_func(child_node.point, fruit_node.point,
                                                                      environment.special_boost))
                            point_to_running_weight[child_node.point] = point_to_running_weight[current_node.point] + 1
        return []

    @staticmethod
    def heuristic_func(current_point: Point, end_point: Point, boost=0):
        """
        Simple Euclidean distance
        :param boost: the boost that special points give to the length
        :param current_point: current point of snake's head
        :param end_point: point of fruit
        :return:
        """
        if end_point.is_special:
            result = sqrt(((end_point.x - current_point.x) ** 2) + ((end_point.y - current_point.y) ** 2)) - boost
            return 0 if result < 0 else result
        return sqrt(((end_point.x - current_point.x) ** 2) + ((end_point.y - current_point.y) ** 2))
