from game.environment.action import Action
from game.environment.tile import Tile
from game.helpers.node import Node
from game.helpers.point import Point
from game.models.base_game_model import BaseGameModel
from game.models.domain_specific.longest_path_ai_solver import LongestPathSolver
import random


class HamiltonSolver(BaseGameModel):
    hamilton_path = []

    def __init__(self):
        BaseGameModel.__init__(self, "Hamilton", "hamilton", "ha")

    def move(self, environment):
        BaseGameModel.move(self, environment)
        if environment.is_in_fruitless_cycle():
            print(("Infinite fruitless cycle - game over at: " + str(environment.reward())))
            return environment.snake_action

        hamilton_path = self._hamilton_path(environment)

        for index in range(0, len(hamilton_path)):
            node = hamilton_path[index]
            next_index = index + 1
            if next_index == len(hamilton_path):
                return hamilton_path[0].action
            elif node.point.x == self.starting_node.point.x and node.point.y == self.starting_node.point.y:
                # self.starting_node = hamilton_path[next_index]
                return hamilton_path[next_index].action
        return environment.snake_action

    def reset(self):
        self.hamilton_path = []

    def get_neighbours(self, previous_node):
        neighbouring_points = []
        x = previous_node.point.x
        y = previous_node.point.y

        is_first_row = y==1
        is_last_row = y==10
        is_first_column = x==1
        is_last_column = x==10

        if not is_first_row:
            neighbouring_points.append(Node(Point(x,y-1), action=Action.DOWN, previous_node=previous_node))
        if not is_last_row:
            neighbouring_points.append(Node(Point(x, y + 1), action=Action.UP, previous_node=previous_node))
        if not is_first_column:
            neighbouring_points.append(Node(Point(x-1, y), action=Action.RIGHT, previous_node=previous_node))
        if not is_last_column:
            neighbouring_points.append(Node(Point(x+1,y), action=Action.LEFT, previous_node=previous_node))
        random.shuffle(neighbouring_points)
        return neighbouring_points


    def node_in_path(self, node, path):
        for path_node in path:
            if node.equal(path_node):
                return True
        return False



    def get_hamiltonian_path(self, current_node, path):
        neighbours = self.get_neighbours(current_node)
        if len(path) == 16 and current_node.connected(path[-1]):
            return path
        length_before_recursion= len(path)
        while(len(neighbours) > 0):
            next_neighbour_to_expand = neighbours.pop(0)
            if not self.node_in_path(next_neighbour_to_expand,path):
                path.append(next_neighbour_to_expand)
                self.get_hamiltonian_path(next_neighbour_to_expand,path)
                path_found = len(path)==16
                if path_found:
                    return path
                else:
                    continue
        path.pop()
        return path





    def rotate_cycle(self,cycle, starting_point):
        temp_array = cycle.copy()
        for node in cycle:
            first_node_in_place = node.point.x== starting_point.point.x and node.point.y == starting_point.point.y
            if not first_node_in_place:
                starting_node = temp_array.pop(0)
                temp_array.append(starting_node)
            else:
                self.hamilton_path = temp_array
                return

    def _hamilton_path(self, environment):
        if self.hamilton_path:
            return self.hamilton_path

        head = self.starting_node
        inverse_snake_action = Action.get_reverse(environment.snake_action)
        tail = environment.snake[-1]
        tail_point = tail.move(inverse_snake_action)
        tail = Node(tail_point)

        # clone some of the attributes for reassignment later
        starting_x = head.point.x
        starting_y = head.point.y

        # Move the snake to somewhere where the longest path will be defined
        environment.tiles[head.point.y][head.point.x] = Tile.empty
        head.action = Action.LEFT
        head.point.x = 3
        head.point.y = 1

        tail.point.x = 4
        tail.point.y = 1
        tail.action=None

        environment.snake[0].x = 3
        environment.snake[0].y = 1
        environment.snake_action = Action.LEFT
        environment.tiles[1][3] = Tile.snake

        # find the hamiltonian path
        path = []
        # self.get_hamiltonian_path(head,path)

        longest_path_solver = LongestPathSolver()
        self.hamilton_path = longest_path_solver.longest_path(head, tail, environment)


       # move the snake back to where it started in the game
        environment.tiles[1][3] = Tile.empty
        environment.tiles[starting_y][starting_x] = Tile.snake

        start_point = Point(starting_x, starting_y)
        environment.snake[0] = start_point
        start_node = Node(start_point)
        self.rotate_cycle(self.hamilton_path,start_node)
        self.starting_node = self.hamilton_path[0]
        environment.snake_action = self.starting_node.action
        return self.hamilton_path



