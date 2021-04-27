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
        self.custom_algorithm = False

    def move(self, environment):
        self.num_rows = environment.height-2
        BaseGameModel.move(self, environment)
        if environment.is_in_fruitless_cycle():
            print(("Infinite fruitless cycle - game over at: " + str(environment.reward())))
            return environment.snake_action

        if self.custom_algorithm:
            hamilton_path = self._hamilton_path(environment)
        else:
            hamilton_path = self.modified_slitherin_hamiltonian_cycle(environment)
        return_action = environment.snake_action

        for index in range(0, len(hamilton_path)):
            node = hamilton_path[index]
            next_index = index + 1
            if next_index == len(hamilton_path):
                return_action = hamilton_path[0].action
                break
            elif node.point.x == self.starting_node.point.x and node.point.y == self.starting_node.point.y:
                return_action = hamilton_path[next_index].action
                break
        if self.custom_algorithm:
            environment.snake_action = Action.get_reverse(return_action)
            return Action.get_reverse(return_action)
        else:
            return return_action


    def reset(self):
        self.hamilton_path = []

    def get_neighbours(self, previous_node):
        neighbouring_points = []
        x = previous_node.point.x
        y = previous_node.point.y

        is_first_row = y==1
        is_last_row = y==self.num_rows
        is_first_column = x==1
        is_last_column = x==self.num_rows

        if not is_first_row and previous_node.action != Action.UP:
            neighbouring_points.append(Node(Point(x,y-1), action=Action.DOWN, previous_node=previous_node))
        if not is_last_row and previous_node.action != Action.DOWN:
            neighbouring_points.append(Node(Point(x, y + 1), action=Action.UP, previous_node=previous_node))
        if not is_first_column and previous_node.action != Action.LEFT:
            neighbouring_points.append(Node(Point(x-1, y), action=Action.RIGHT, previous_node=previous_node))
        if not is_last_column and previous_node.action != Action.RIGHT:
            neighbouring_points.append(Node(Point(x+1,y), action=Action.LEFT, previous_node=previous_node))

        return neighbouring_points


    def node_in_path(self, node, path, path_dict):
        return (node.point.x, node.point.y) in path_dict




    def get_hamiltonian_path(self, current_node, path, path_dict):
        neighbours = self.get_neighbours(current_node)
        max_recursion_reached = len(path) == self.num_rows**2
        cycle_found = len(path)>0 and current_node.connected(path[0])

        if max_recursion_reached:
            if cycle_found:
                return path
            node_to_remove = path.pop()
            del path_dict[(node_to_remove.point.x, node_to_remove.point.y)]
            return path

        while(len(neighbours) > 0):
            next_neighbour_to_expand = neighbours.pop(0)
            if not self.node_in_path(next_neighbour_to_expand,path,path_dict):
                path.append(next_neighbour_to_expand)
                path_dict[(next_neighbour_to_expand.point.x,next_neighbour_to_expand.point.y)] = True
                self.get_hamiltonian_path(next_neighbour_to_expand,path, path_dict)
                path_found = len(path)==self.num_rows**2
                if path_found:
                    return path
                else:
                    continue
        node_to_remove = path.pop()
        del path_dict[(node_to_remove.point.x,node_to_remove.point.y)]
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

    def get_first_action(self,last_point,first_point):
        x = last_point.point.x
        y = last_point.point.y

        x_difference = x - first_point.point.x
        y_difference = y - first_point.point.y


        if y_difference < 0:
            return Action.UP
        elif y_difference > 0:
            return Action.DOWN
        elif x_difference < 0:
            return  Action.LEFT
        elif x_difference > 0:
            return Action.RIGHT

    def _hamilton_path(self, environment):
        if self.hamilton_path:
            return self.hamilton_path

        head = self.starting_node

        # find the hamiltonian path
        path = [head]
        self.get_hamiltonian_path(head,path,{(head.point.x,head.point.y):True})
        first_action = self.get_first_action(path[-1], path[0])
        path[0].action = first_action
        self.hamilton_path = path

        return self.hamilton_path

    def modified_slitherin_hamiltonian_cycle(self, environment):
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
        tail.action = None

        environment.snake[0].x = 3
        environment.snake[0].y = 1
        environment.snake_action = Action.LEFT
        environment.tiles[1][3] = Tile.snake

        # find the hamiltonian path
        longest_path_solver = LongestPathSolver()
        self.hamilton_path = longest_path_solver.longest_path(head, tail, environment)

        # move the snake back to where it started in the game
        environment.tiles[1][3] = Tile.empty
        environment.tiles[starting_y][starting_x] = Tile.snake

        start_point = Point(starting_x, starting_y)
        environment.snake[0] = start_point
        start_node = Node(start_point)
        self.rotate_cycle(self.hamilton_path, start_node)
        self.starting_node = self.hamilton_path[0]
        environment.snake_action = self.starting_node.action
        return self.hamilton_path