
import random
from collections import deque

import matplotlib.pyplot as plt
import tensorflow as tf

import numpy as np
from keras import Sequential
from keras.src.layers import Dense
from keras.src.optimizers import Adam

from Learnbased_betting.Learnbased_Betting_Training.bettingenvironmenteasy import BettingEnvironmentEasy
from Rulebased_Betting.calculatebids import CalculateBids
from Rulebased_Betting.calculategamemodevalue import CalculateGamemodeValue
from Rulebased_Betting.helpersbetting import HelpersBetting


class BettingAgentEasySkataufnahme:

    def __init__(self):
        self.action_size = 2
        self.batch_size = 32
        self.memory = deque(maxlen=100)
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.2
        self.learning_rate = 0.001
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(90,activation = "relu",input_shape=(136,)))
        model.add(Dense(45,activation = "relu"))
        model.add(Dense(self.action_size,activation = "softmax"))
        model.compile(loss = "mse", optimizer = Adam(learning_rate = self.learning_rate))
        return model

    def remember(self,state,action,reward,next_state,reward_decide,reward_discard,done):
        self.memory.append((state,action,reward,next_state,reward_decide,reward_discard,done))

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

        states = np.zeros((self.batch_size,136))
        targets = np.zeros((self.batch_size, 2))

        for i, (state, action, reward, next_state,reward_decide,reward_discard, done) in enumerate(minibatch):
            state_vector = self.encode_state(state)
            if next_state.get("skataufnahme"):
                target = reward + reward_decide + reward_discard
            else:
                target = reward + reward_decide
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
        player = {"playerId":"player1"}
        hand_vector = self.encode_hand(state.get("hand"))

        betting_vector = np.zeros(0)

        modes = [
            "Kreuz",
            "Pik",
            "Herz",
            "Karo",
            "Grand",
            "Null"
        ]

        for i in modes:
            if i == "Null":
                betting = 23
            else:
                multiplier = CalculateGamemodeValue.calculate_multiplier(state.get("hand"))
                betting = int(CalculateBids.create_gamemode(i,player,multiplier,CalculateBids.check_clubs_jack(state.get("hand"))).get("betting"))
            vector = np.array(list(np.binary_repr(betting).zfill(8))).astype(np.int8)
            betting_vector = np.concatenate((betting_vector,vector))
        for i in modes:
            if i == "Null":
                betting = 35
            else:
                multiplier = CalculateGamemodeValue.calculate_multiplier(state.get("hand"))
                betting = int(CalculateBids.create_gamemode_hand(i,player,multiplier,CalculateBids.check_clubs_jack(state.get("hand"))).get("betting"))
            vector = np.array(list(np.binary_repr(betting).zfill(8))).astype(np.int8)
            betting_vector = np.concatenate((betting_vector,vector))

        winner_betting = 18
        if len(state.get("previous_bets")) !=0:
            winner_betting = int(state.get("previous_bets")[-1].get("gamemode").get("betting"))

        winning_vector = np.array(list(np.binary_repr(winner_betting).zfill(8))).astype(np.int8)

        state_vector = np.concatenate((hand_vector,winning_vector,betting_vector))
        return state_vector.reshape(1,-1)




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
    agent = BettingAgentEasySkataufnahme()
    agent_decide = BettingAgentEasyDecide()

    env = BettingEnvironmentEasy()

    success = []

    reward_buffer = deque(maxlen= 10)

    for e in range(n_episodes):
        state = env.reset()
        done = False


        while not done:
            action = agent.act(state)

            next_state, reward, done = env.step_take_skat(action)

            reward_buffer.append(reward)

            agent.remember(state,action,reward,next_state,done)

            state = next_state

        if len(agent.memory) > agent.batch_size:
            agent.train(agent.batch_size,agent_decide)
        if e % 10 == 0:

            print(e,agent.epsilon,sum(reward_buffer)/10)




    plt.plot(success)
    plt.show()


