#!/usr/bin/env python
# -*- coding: utf-8 -*


from enum import Enum
import math


class Action(Enum):
    LEFT = (-1, 0)
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)

    @staticmethod
    def description(action):
        if action == Action.UP:
            return "↑"
        elif action == Action.DOWN:
            return "↓"
        elif action == Action.LEFT:
            return "←"
        else:
            return "→"

    @staticmethod
    def get_reverse(action: 'Action'):
        switcher = {
            Action.LEFT: Action.RIGHT,
            Action.RIGHT: Action.LEFT,
            Action.UP: Action.DOWN,
            Action.DOWN: Action.UP
        }
        return switcher[action]

    @staticmethod
    def is_reverse(current_action, new_action):
        inverse_action = Action.get_reverse(current_action)
        return new_action == inverse_action

    @staticmethod
    def action_from_vector(vector):
        return Action.possible()[vector]

    @staticmethod  # So that turning LEFT is -1, forward is 0 and turning RIGHT is 1
    def vector(start, end):
        start_index = Action.all().index(start)
        end_index = Action.all().index(end)
        diff = end_index - start_index
        bounded = max(min(diff, 1), -1)
        if abs(diff) > 1:
            return -bounded
        return bounded

    @staticmethod
    def left_neighbor(action):
        actions = Action.all()
        actions.reverse()
        return Action._neighbor(action, actions)

    @staticmethod
    def right_neighbor(action):
        actions = Action.all()
        return Action._neighbor(action, actions)

    @staticmethod
    def _neighbor(action, actions):
        actions_count = len(actions)
        for i in range(0, actions_count):
            if actions[i] == action:
                if i == actions_count - 1:
                    return actions[0]
                else:
                    return actions[i + 1]

    @staticmethod
    def adjusted_angles(action):
        if action == Action.UP:
            return math.pi / 2, math.pi * 3 / 2
        elif action == Action.LEFT:
            return math.pi, math.pi
        elif action == Action.DOWN:
            return math.pi * 3 / 2, math.pi / 2
        else:
            return 0, 0  # Angle is by default calculated according to the Action.RIGHT

    @staticmethod
    def normalized_action(current_action, new_action):
        if new_action == Action.LEFT:
            return Action.left_neighbor(current_action)
        elif new_action == Action.RIGHT:
            return Action.right_neighbor(current_action)
        else:
            return current_action

    @staticmethod
    def possible():
        return [Action.LEFT, Action.UP, Action.RIGHT]

    @staticmethod
    def all():
        return [Action.LEFT, Action.UP, Action.RIGHT, Action.DOWN]
