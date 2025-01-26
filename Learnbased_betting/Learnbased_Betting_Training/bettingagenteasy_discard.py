
import random
from collections import deque

import matplotlib.pyplot as plt
import tensorflow as tf

import numpy as np
from keras import Sequential
from keras.src.layers import Dense
from keras.src.optimizers import Adam

from Learnbased_betting.Learnbased_Betting_Training.bettingagenteasy_decide import BettingAgentEasyDecide
from Learnbased_betting.Learnbased_Betting_Training.bettingagenteasy_takeskat import BettingAgentEasySkataufnahme
from Learnbased_betting.Learnbased_Betting_Training.bettingenvironmenteasy import BettingEnvironmentEasy
from Rulebased_Betting.helpersbetting import HelpersBetting


class BettingAgentEasyDiscard:

    def __init__(self):
        self.action_size = 66
        self.batch_size = 32
        self.memory = deque(maxlen=100)
        self.gamma = 0.1
        self.beta = 0.3
        self.alpha = 0.5
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.01
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(4,activation = "relu",input_shape=(46,)))
        model.add(Dense(2,activation = "relu"))
        model.add(Dense(self.action_size,activation = "softmax"))
        model.compile(loss = "mse", optimizer = Adam(learning_rate = self.learning_rate))
        return model

    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))

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

        states = np.zeros((self.batch_size,46))
        targets = np.zeros((self.batch_size, 66))

        for i,(state,action,reward,next_state,done) in enumerate(minibatch):
            target = reward
            state_vector = self.encode_state(state)
            next_state_vector = self.encode_state(next_state)
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state_vector)))
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
        hand = state.get("hand")
        skat = state.get("skat")

        for i in skat:
            hand.append(i)
        hand_vector = self.encode_hand(hand)

        gamemode_vector = np.zeros(6)
        modes = [
            "Kreuz",
            "Pik",
            "Herz",
            "Karo",
            "Grand",
            "Null"
        ]
        gamemode = state.get("chosen_gamemode").get("name")
        for i in modes:
            if i == modes:
                gamemode[modes.index(i)] = 1

        winner_betting = 18
        if len(state.get("previous_bets")) != 0:
            winner_betting = int(state.get("previous_bets")[-1].get("gamemode").get("betting"))

        winning_vector = np.array(list(np.binary_repr(winner_betting).zfill(8))).astype(np.int8)

        state_vector =  np.concatenate((hand_vector,gamemode_vector,winning_vector)).reshape(1,-1)
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
    n_episodes = 500
    agent_discard = BettingAgentEasyDiscard()

    env = BettingEnvironmentEasy()

    for e in range(n_episodes):
        state = env.reset()
        done = False


        while not done:
            action_discard = (agent_discard.act(state))

            next_state, reward_discard, done = env.step_discard(action_discard)

            agent_discard.remember(state,action_discard,reward_discard,next_state,done)

            state = next_state

        if len(agent_discard.memory) > agent_discard.batch_size:
            agent_discard.train(agent_discard.batch_size)
        if e % 10 == 0:

            print(e, agent_discard.epsilon / 10)





