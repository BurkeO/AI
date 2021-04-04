from game.environment.tile import Tile
from game.helpers.node import Node
from game.helpers.point import Point
from game.helpers.stack import Stack
from game.models.base_game_model import BaseGameModel


class ShortestPathDFSSolver(BaseGameModel):

    def __init__(self):
        BaseGameModel.__init__(self, "Shortest Path DFS", "shortest_path_dfs", "spd")

    def move(self, environment):
        BaseGameModel.move(self, environment)

        shortest_path_move_from_transposition_table = self._path_move_from_transposition_table(self.starting_node,
                                                                                               self.fruit_node)
        if shortest_path_move_from_transposition_table:
            return shortest_path_move_from_transposition_table

        stack = Stack([self.starting_node])
        visited_nodes = {self.starting_node}
        shortest_path = []
        while stack.stack:
            current_node = stack.pop()
            if current_node == self.fruit_node:
                shortest_path = self._recreate_path_for_node(current_node)
            for action in environment.possible_actions_for_current_action(current_node.action):
                child_node_point = current_node.point.move(action)
                neighbor = environment.tiles[child_node_point.y][child_node_point.x]
                if neighbor == Tile.empty or neighbor == Tile.fruit:
                    child_node = Node(child_node_point)
                    child_node.action = action
                    child_node.previous_node = current_node
                    if child_node not in visited_nodes and child_node not in stack.stack:
                        visited_nodes.add(current_node)
                        stack.push(child_node)

        if shortest_path:
            self.transposition_table[self.fruit_node] = shortest_path
            first_point = shortest_path[-2]
            return first_point.action
        return environment.snake_action
