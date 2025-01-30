
import random
from collections import deque

import matplotlib.pyplot as plt
import tensorflow as tf

import numpy as np
from keras import Sequential
from keras.src.layers import Dense
from keras.src.optimizers import Adam

from Learnbased_betting.Learnbased_Betting_Training.bettingagenteasy_takeskat import BettingAgentEasySkataufnahme
from Learnbased_betting.Learnbased_Betting_Training.bettingenvironmenteasy import BettingEnvironmentEasy
from Rulebased_Betting.calculatebids import CalculateBids
from Rulebased_Betting.calculategamemodevalue import CalculateGamemodeValue
from Rulebased_Betting.helpersbetting import HelpersBetting


class BettingAgentEasyDecide:

    def __init__(self):
        self.action_size = 6
        self.batch_size = 32
        self.memory = deque(maxlen=100)
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.2
        self.learning_rate = 0.001
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(64,activation = "relu",input_shape=(89,)))
        model.add(Dense(32,activation = "relu"))
        model.add(Dense(self.action_size,activation = "softmax"))
        model.compile(loss = "mse", optimizer = Adam(learning_rate = self.learning_rate))
        return model

    def remember(self,state,action,reward,next_state,reward_discard,done):
        self.memory.append((state,action,reward,next_state,reward_discard,done))

    def act(self,state):
       if np.random.rand() <= self.epsilon:
           return random.randrange(self.action_size)
       act = self.model.predict(self.encode_state(state))
       print(act)
       for x in state["previous_bets"]:
           print(x["gamemode"])
       return np.argmax(act[0])

    def train(self,batch_size):
        minibatch = random.sample(self.memory,batch_size)

        states = np.zeros((self.batch_size,89))
        targets = np.zeros((self.batch_size, 6))

        for i, (state, action, reward, next_state,reward_discard, done) in enumerate(minibatch):
            state_vector = self.encode_state(state)
            if state.get("skataufnahme"):
                target = reward + reward_discard
            else:
                target = reward
            target_f = self.model.predict(state_vector)
            target_f[0][action] = target

            states[i] = state_vector
            targets[i] = target_f

        self.model.fit(states,targets,epochs = 1,verbose = 0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self,name):
        self.model.save_weights(name)

    def encode_state(self,state):
        player = {"playerId": "player1"}
        hand_vector = self.encode_hand(state.get("hand"))

        skat_vector = np.zeros(1)

        modes = [
            "Kreuz",
            "Pik",
            "Herz",
            "Karo",
            "Grand",
            "Null"
        ]

        betting_vector = np.zeros(0)

        if state.get("skataufnahme"):
            skat_vector[0] = 1
            for i in modes:
                if i == "Null":
                    betting = 23
                else:
                    multiplier = CalculateGamemodeValue.calculate_multiplier(state.get("hand"))
                    betting = int(CalculateBids.create_gamemode(i, player, multiplier,
                                                                CalculateBids.check_clubs_jack(state.get("hand"))).get(
                        "betting"))
                vector = np.array(list(np.binary_repr(betting).zfill(8))).astype(np.int8)
                betting_vector = np.concatenate((betting_vector, vector))
        else:
            for i in modes:
                if i == "Null":
                    betting = 35
                else:
                    multiplier = CalculateGamemodeValue.calculate_multiplier(state.get("hand"))
                    betting = int(CalculateBids.create_gamemode_hand(i, player, multiplier,
                                                                     CalculateBids.check_clubs_jack(
                                                                         state.get("hand"))).get("betting"))
                vector = np.array(list(np.binary_repr(betting).zfill(8))).astype(np.int8)
                betting_vector = np.concatenate((betting_vector, vector))

        winner_betting = 18
        if len(state.get("previous_bets")) != 0:
            winner_betting = int(state.get("previous_bets")[-1].get("gamemode").get("betting"))

        winning_vector = np.array(list(np.binary_repr(winner_betting).zfill(8))).astype(np.int8)

        state_vector =  np.concatenate((hand_vector,skat_vector,winning_vector,betting_vector)).reshape(1,-1)
        return state_vector

    def encode_hand(self, hand):
        suits = ["clubs", "spades", "hearts", "diamonds"]
        values = ["ace", "king", "queen", "jack", "10", "9", "8", "7"]
        encoding = np.zeros((len(suits), len(values)))

        for card in hand:
            suit_index = suits.index(card["suit"])
            value_index = values.index(card["value"])
            encoding[suit_index][value_index] = 1

        return encoding.flatten()

if __name__ == "__main__":
    print('GPU name: ', tf.config.experimental.list_physical_devices('GPU'))
    action_size = 2
    n_episodes = 500
    agent_betting = BettingAgentEasyDecide()

    env = BettingEnvironmentEasy()

    for e in range(n_episodes):
        state = env.reset()
        done = False


        while not done:
            action_betting = agent_betting.act(state)

            next_state, reward_betting, done = env.step_decide(action_betting)

            agent_betting.remember(state, action_betting, reward_betting, next_state, done)

            state = next_state

        if len(agent_betting.memory) > agent_betting.batch_size:
            agent_betting.train(agent_betting.batch_size)

        if e % 10 == 0:

            print(e, agent_betting.epsilon / 10)





