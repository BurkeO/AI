import os
import random
import shutil
from statistics import mean
from datetime import datetime

import numpy as np

from game.environment.action import Action
from game.helpers.constants import Constants
from game.models.base_game_model import BaseGameModel
from tf_models.ddqn_model import DDQNModel

GAMMA = 0.99
MEMORY_SIZE = 10000
BATCH_SIZE = 32
REPLAY_START_SIZE = 32
TRAINING_FREQUENCY = 4
TARGET_NETWORK_UPDATE_FREQUENCY = TRAINING_FREQUENCY * 1000
MODEL_PERSISTENCE_UPDATE_FREQUENCY = 10000
SCORE_LOGGING_FREQUENCY_STEPS = 10000
LEARNING_LOGGING_FREQUENCY = 10000

EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.1
EXPLORATION_TEST = 0.01
EXPLORATION_STEPS = 150000
EXPLORATION_DECAY = (EXPLORATION_MAX - EXPLORATION_MIN) / EXPLORATION_STEPS


class BaseDDQNGameModel(BaseGameModel):
    model_dir_path = Constants.MODEL_DIRECTORY + "ddqn/"
    model_input_shape = (Constants.FRAMES_TO_REMEMBER, Constants.ENV_WIDTH, Constants.ENV_HEIGHT)

    def __init__(self, long_name, short_name, abbreviation):
        BaseGameModel.__init__(self, long_name, short_name, abbreviation)

        self.model_path = self.model_dir_path + Constants.DQN_MODEL_NAME

        
        if not os.path.exists(os.path.dirname(self.model_path)):
            os.makedirs(os.path.dirname(self.model_path))

        self.action_space = len(Action.possible())
        self.ddqn = DDQNModel(self.model_input_shape, self.action_space).model
        self._load_model()

    def move(self, environment):
        BaseGameModel.move(self, environment)

    def _save_model(self):
        self.ddqn.save_weights(self.model_path)

    def _load_model(self):
        if os.path.isfile(self.model_path):
            self.ddqn.load_weights(self.model_path)


class DDQNSolver(BaseDDQNGameModel):

    def __init__(self):
        BaseDDQNGameModel.__init__(self, "Double DQN", "double_dqn", "ddqn")

    def move(self, environment):
        BaseDDQNGameModel.move(self, environment)

        if np.random.rand() < 0.01:
            action_vector = random.randrange(self.action_space)
        else:
            state = environment.state()
            q_values = self.ddqn.predict(np.expand_dims(np.asarray(state).astype(np.float64), axis=0), batch_size=1)
            action_vector = Action.action_from_vector(np.argmax(q_values[0]))
        return Action.normalized_action(environment.snake_action, action_vector)


class DDQNTrainer(BaseDDQNGameModel):

    def __init__(self):
        BaseDDQNGameModel.__init__(self, "Double DQN", "double_dqn_trainer", "ddqnt")
        self.ddqn_target = DDQNModel(self.model_input_shape, self.action_space).model
        self.memory = []
        self.epsilon = EXPLORATION_MAX
        self.score_output_path = "ddqn_avg_scores_" + str(Constants.ENV_HEIGHT) + "_" + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".csv"
        self.total_runs = 0

    def move(self, environment):
        BaseDDQNGameModel.move(self, environment)
        self._ddqn()

    def _ddqn(self, total_step_limit=200000, total_run_limit=None, clip=True):
        run = 0
        total_step = 0
        scores = []
        while True:
            if total_run_limit is not None and run >= total_run_limit:
                print(("Reached total run limit of: " + str(total_run_limit)))
                exit(0)

            run += 1
            env = self.prepare_training_environment()
            current_state = env.state()
            step = 0
            score = env.reward()
            while True:
                if total_step >= total_step_limit:
                    print(("Reached total step limit of: " + str(total_step_limit)))
                    exit(0)
                total_step += 1
                step += 1

                action = self._predict_move(current_state)
                action_vector = Action.action_from_vector(action)
                normalized_action = Action.normalized_action(env.snake_action, action_vector)
                next_state, reward, terminal = env.full_step(normalized_action)
                if clip:
                    np.sign(reward)
                score += reward
                self._remember(current_state, action, reward, next_state, terminal)
                current_state = next_state

                self._step_update(total_step)

                if terminal:
                    scores.append(score)
                    self.total_runs += 1
                    if len(scores) % SCORE_LOGGING_FREQUENCY_STEPS == 0:
                        self._log_dqn_scores(mean(scores))
                        print(('{{"metric": "score", "value": {}}}'.format(mean(scores))))
                        print(('{{"metric": "run", "value": {}}}'.format(run)))
                        scores = []
                    break

    def _log_dqn_scores(self, avg_score):
        output = str(self.total_runs) + "," + str(avg_score) + "\n"
        print(output)
        with open(self.score_output_path, "a") as myfile:
            myfile.write(output)

    def _predict_move(self, state):
        if np.random.rand() < self.epsilon or len(self.memory) < REPLAY_START_SIZE:
            return random.randrange(self.action_space)
        q_values = self.ddqn.predict(np.expand_dims(np.asarray(state).astype(np.float64), axis=0), batch_size=1)
        return np.argmax(q_values[0])

    def _remember(self, current_state, action, reward, next_state, terminal):
        self.memory.append({"current_state": np.asarray(current_state),
                            "action": action,
                            "reward": reward,
                            "next_state": np.asarray(next_state),
                            "terminal": terminal})
        if len(self.memory) > MEMORY_SIZE:
            self.memory.pop(0)

    def _step_update(self, total_step):
        if total_step < REPLAY_START_SIZE:
            return

        if total_step % TRAINING_FREQUENCY == 0:
            loss, accuracy, average_max_q = self._train()
            if total_step % LEARNING_LOGGING_FREQUENCY == 0:
                # TODO: batch and average these values
                print(('{{"metric": "loss", "value": {}}}'.format(loss)))
                print(('{{"metric": "accuracy", "value": {}}}'.format(accuracy)))
                print(('{{"metric": "q", "value": {}}}'.format(average_max_q)))

        self._update_epsilon()

        if total_step % MODEL_PERSISTENCE_UPDATE_FREQUENCY == 0:
            print(('{{"metric": "epsilon", "value": {}}}'.format(self.epsilon)))
            print(('{{"metric": "total_step", "value": {}}}'.format(total_step)))
            self._save_model()

        if total_step % TARGET_NETWORK_UPDATE_FREQUENCY == 0:
            self._reset_target_network()

    def _train(self):
        batch = np.asarray(random.sample(self.memory, BATCH_SIZE))
        if len(batch) < BATCH_SIZE:
            return

        current_states = []
        q_values = []
        max_q_values = []

        for entry in batch:
            current_state = np.expand_dims(np.asarray(entry["current_state"]).astype(np.float64), axis=0)
            current_states.append(current_state)
            next_state = np.expand_dims(np.asarray(entry["next_state"]).astype(np.float64), axis=0)
            next_state_prediction = self.ddqn_target.predict(next_state).ravel()
            next_q_value = np.max(next_state_prediction)
            q = list(self.ddqn.predict(current_state)[0])
            if entry["terminal"]:
                q[entry["action"]] = entry["reward"]
            else:
                q[entry["action"]] = entry["reward"] + GAMMA * next_q_value
            q_values.append(q)
            max_q_values.append(np.max(q))

        fit = self.ddqn.fit(np.asarray(current_states).squeeze(),
                            np.asarray(q_values).squeeze(),
                            batch_size=BATCH_SIZE,
                            verbose=0)
        loss = fit.history["loss"][0]
        accuracy = fit.history["acc"][0]
        return loss, accuracy, mean(max_q_values)

    def _update_epsilon(self):
        self.epsilon -= EXPLORATION_DECAY
        self.epsilon = max(EXPLORATION_MIN, self.epsilon)

    def _reset_target_network(self):
        self.ddqn_target.set_weights(self.ddqn.get_weights())
