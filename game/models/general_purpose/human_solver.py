from pygame.locals import *

from game.environment.action import Action
from game.models.base_game_model import BaseGameModel


class HumanSolver(BaseGameModel):
    action = None

    def __init__(self):
        BaseGameModel.__init__(self, "Human", "human", "hu")

    def move(self, environment):
        BaseGameModel.move(self, environment)
        if self.action is None:
            return environment.snake_action
        is_backward_action = Action.is_reverse(environment.snake_action, self.action)
        return environment.snake_action if is_backward_action else self.action

    def user_input(self, event):
        if event.key == K_UP:
            self.action = Action.UP
        elif event.key == K_DOWN:
            self.action = Action.DOWN
        elif event.key == K_LEFT:
            self.action = Action.LEFT
        elif event.key == K_RIGHT:
            self.action = Action.RIGHT
