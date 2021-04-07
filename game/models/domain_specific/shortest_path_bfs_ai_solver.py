from game.environment.tile import Tile
from game.helpers.node import Node
from game.helpers.point import Point
from game.helpers.queue import Queue
from game.models.base_game_model import BaseGameModel


class ShortestPathBFSSolver(BaseGameModel):

    def __init__(self):
        BaseGameModel.__init__(self, "Shortest Path BFS", "shortest_path_bfs", "spb")

    def move(self, environment):
        BaseGameModel.move(self, environment)
        shortest_path_move_from_transposition_table = self._path_move_from_transposition_table(self.starting_node,
                                                                                               self.fruit_nodes)
        if shortest_path_move_from_transposition_table:
            return shortest_path_move_from_transposition_table

        shortest_path = self.shortest_path(environment, self.starting_node, self.fruit_nodes)
        if shortest_path:
            self.transposition_table[self.fruit_nodes] = shortest_path
            first_point = shortest_path[-2]
            return first_point.action
        return environment.snake_action

    def shortest_path(self, environment, start, end):
        queue = Queue([start])
        visited_nodes = {start}
        shortest_path = []
        while queue.queue:
            current_node = queue.dequeue()
            if current_node == end:
                shortest_path = self._recreate_path_for_node(current_node)
                break
            for action in environment.possible_actions_for_current_action(current_node.action):
                child_node_point = current_node.point.move(action)
                neighbor = environment.tiles[child_node_point.y][child_node_point.x]
                if neighbor == Tile.empty or neighbor == Tile.fruit:
                    child_node = Node(child_node_point)
                    child_node.action = action
                    child_node.previous_node = current_node
                    if child_node not in visited_nodes and child_node not in queue.queue:
                        visited_nodes.add(current_node)
                        queue.enqueue(child_node)
        if shortest_path:
            return shortest_path
        else:
            return []
