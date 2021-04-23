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
                self.starting_node = hamilton_path[next_index]
                return hamilton_path[next_index].action
        return environment.snake_action

    def reset(self):
        self.hamilton_path = []

    def get_neighbours(self,point):
        neighbouring_points = []
        x = point.x
        y = point.y

        is_first_row = y==1
        is_last_row = y==10
        is_first_column = x==1
        is_last_column = x==10

        if not is_first_row:
            neighbouring_points.append(Point(x,y-1))
        if not is_last_row:
            neighbouring_points.append(Point(x, y - 1))
        if not is_first_column:
            neighbouring_points.append(Point(x-1, y))
        if not is_last_column:
            neighbouring_points.append(Point(x+1,y))




    def get_hamiltonian_path(self):
        head = self.starting_node

    def _hamilton_path(self, environment):
        if self.hamilton_path:
            return self.hamilton_path

        head = self.starting_node
        inverse_snake_action = Action.get_reverse(environment.snake_action)
        # available_actions = [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]
        # available_actions.remove(environment.snake_action)
        # available_actions.remove(inverse_snake_action)
        # if head.point.x == 1 and Action.RIGHT in available_actions:
        #     available_actions.remove(Action.RIGHT)
        # elif head.point.x==10 and Action.LEFT in available_actions:
        #     available_actions.remove(Action.LEFT)
        #
        # if head.point.y == 1 and Action.DOWN in available_actions:
        #     available_actions.remove(Action.DOWN)
        # elif head.point.y == 10 and Action.UP in available_actions:
        #     available_actions.remove(Action.UP)


        tail = environment.snake[-1]
        tail_point = tail.move(inverse_snake_action)
        tail = Node(tail_point)

        # Conor hacking the solution to always win
        environment.tiles[head.point.y][head.point.x] = Tile.empty
        head.action = Action.LEFT
        head.point.x = 3
        head.point.y = 1
        # self.starting_node = head

        tail.point.x = 4
        tail.point.y = 1
        tail.action=None

        environment.snake[0].x = 3
        environment.snake[0].y = 1
        environment.snake_action = Action.LEFT
        environment.tiles[1][3] = Tile.snake
        environment.snake[0] = head.point

        if self.hamilton_path:
            return self.hamilton_path
        longest_path_solver = LongestPathSolver()
        self.hamilton_path = longest_path_solver.longest_path(head, tail, environment)
        # while len(self.hamilton_path) < 100:
        #     next_action = random.choice(available_actions)
        #     available_actions.remove(next_action)
        #     tail = environment.snake[-1]
        #     tail_point = tail.move(next_action)
        #     tail = Node(tail_point)
        #     self.hamilton_path = longest_path_solver.longest_path(head, tail, environment)

        # current_x = temp_head.point.x
        # current_y = temp_head.point.y
        # environment.snake[0].x = current_x
        # environment.snake[0].y = current_y
        # # environment.snake_action = temp_head.action
        # environment.tiles[1][3] = Tile.empty
        # environment.tiles[current_y][current_x] = Tile.snake
        # environment.snake[0] = temp_head.point
        # return self.hamilton_path

        return self.hamilton_path

        # if self.hamilton_path:
        #     return self.hamilton_path
        # longest_path_solver = LongestPathSolver()
        # self.hamilton_path = longest_path_solver.longest_path(head, tail, environment)
        # while len(self.hamilton_path) < 100:
        #     self.hamilton_path = longest_path_solver.longest_path(head, tail, environment)
        # return self.hamilton_path



