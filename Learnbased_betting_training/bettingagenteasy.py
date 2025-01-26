
import random
from collections import deque

import matplotlib.pyplot as plt
import tensorflow as tf

import numpy as np
from keras import Sequential
from keras.src.layers import Dense
from keras.src.optimizers import Adam

from Learnbased_betting_training.bettingenvironmenteasy import BettingEnvironmentEasy


class BettingAgentEasy:

    def __init__(self,action_size):
        self.action_size = action_size
        self.batch_size = 32
        self.memory = deque(maxlen=100)
        self.gamma = 0.5
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.01
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(4,activation = "relu",input_shape=(11,)))
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

        states = np.zeros((self.batch_size,11))
        targets = np.zeros((self.batch_size, 3))

        for i,(state,action,reward,next_state,done) in enumerate(minibatch):
            target = reward
            state_vector = self.encode_state(state)
            next_state_vector = self.encode_state(next_state)
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state_vector))
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
        state_vector = np.zeros(11)

        bet_options = [
            "Raise",
            "Check",
            "Pass"
        ]
        players = [
            {"playerId":"player1"},
            {"playerId":"player2"},
            {"playerId":"player4"}
        ]
        index = 0
        for bet in state["previous_bets"]:
            if bet["gamemode"]["name"] == "Pass":
                state_vector[index] = 1
                index +=1
                if index == 2:
                    break
        bets = reversed(state["previous_bets"])
        for i,bet in enumerate(bets):
            index_bet = 2 + i*3 + bet_options.index(bet["gamemode"]["name"])
            state_vector[index_bet] = 1
            if i == 0:
                state_vector[8+players.index(bet["player"])] = 1
            if i == 1:
                break


        return state_vector.reshape(1,-1)

if __name__ == "__main__":
    print('GPU name: ', tf.config.experimental.list_physical_devices('GPU'))
    action_size = 3
    n_episodes = 500
    agent = BettingAgentEasy(action_size)

    env = BettingEnvironmentEasy()

    success = []

    reward_buffer = deque(maxlen= 10)

    for e in range(n_episodes):
        state = env.reset()
        done = False


        while not done:
            action = agent.act(state)

            next_state, reward, done, succesful = env.step(action)

            reward_buffer.append(reward)

            if succesful:
                success.append(1)
            else:
                success.append(0)

            agent.remember(state,action,reward,next_state,done)

            state = next_state

        if len(agent.memory) > agent.batch_size:
            agent.train(agent.batch_size)
        if e % 10 == 0:

            print(e,agent.epsilon,sum(reward_buffer)/10)




    plt.plot(success)
    plt.show()


