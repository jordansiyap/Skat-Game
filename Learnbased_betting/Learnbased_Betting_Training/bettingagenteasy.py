
import random
from collections import deque

import matplotlib.pyplot as plt
import tensorflow as tf

import numpy as np
from keras import Sequential
from keras.src.layers import Dense
from keras.src.optimizers import Adam

from Learnbased_betting.Learnbased_Betting_Training.bettingagenteasy_decide import BettingAgentEasyDecide
from Learnbased_betting.Learnbased_Betting_Training.bettingagenteasy_discard import BettingAgentEasyDiscard
from Learnbased_betting.Learnbased_Betting_Training.bettingagenteasy_takeskat import BettingAgentEasySkataufnahme
from Learnbased_betting.Learnbased_Betting_Training.bettingenvironmenteasy import BettingEnvironmentEasy
from Rulebased_Betting.helpersbetting import HelpersBetting


class BettingAgentEasy:

    def __init__(self,action_size):
        self.action_size = action_size
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
        model.add(Dense(4,activation = "relu",input_shape=(51,)))
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

    def train(self,batch_size,agent_skataufnahme,agent_decide,agent_discard):
        minibatch = random.sample(self.memory,batch_size)

        states = np.zeros((self.batch_size,51))
        targets = np.zeros((self.batch_size, 2))

        for i,(state,action,reward,next_state,done) in enumerate(minibatch):
            target = reward
            state_vector = self.encode_state(state)
            next_state_vector = self.encode_state(next_state)
            state_vector_skataufnahme = agent_skataufnahme.encode_state(state)
            state_vector_decide = agent_decide.encode_state(state)
            if state.get("skataufnahme"):
                state_vector_discard = agent_discard.encode_state(state)
                if not done:
                    target = (reward + self.gamma * np.amax(self.model.predict(next_state_vector))
                              + np.amax(agent_skataufnahme.model.predict(state_vector_skataufnahme))
                              + np.amax(agent_decide.model.predict(state_vector_decide))
                              + np.amax(agent_discard.model.predict(state_vector_discard)))
            else:
                if not done:
                    target = (reward + self.gamma * np.amax(self.model.predict(next_state_vector))
                              + np.amax(agent_skataufnahme.model.predict(state_vector_skataufnahme))
                              + np.amax(agent_decide.model.predict(state_vector_decide)))
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
        hand_vector = self.encode_hand(state.get("hand"))
        gamemode_vector = np.zeros(11)


        next_betting = 18
        if len(state.get("previous_bets")) != 0:
            if state.get("previous_bets")[-1].get("gamemode").get("name") == "Raise":
                next_betting = int(state.get("previous_bets")[-1].get("gamemode").get("betting"))
            else:
                skat_bet_table = HelpersBetting.create_skat_bid_table(state.get("previous_bets")[-1].get("player"))
                for x in skat_bet_table:
                    if int(x.get("betting")) > int(state.get("previous_bets")[-1].get("gamemode").get("betting")):
                        next_betting = int(x.get("betting"))
                        break

        next_betting_vector = np.array(list(np.binary_repr(next_betting).zfill(8))).astype(np.int8)
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
            if bet["gamemode"].get("name") == "Pass":
                gamemode_vector[index] = 1
                index +=1
                if index == 2:
                    break
        bets = reversed(state["previous_bets"])
        for i,bet in enumerate(bets):
            index_bet = 2 + i*3 + bet_options.index(bet["gamemode"].get("name"))
            gamemode_vector[index_bet] = 1
            if i == 0:
                gamemode_vector[8+players.index(bet["player"])] = 1
            if i == 1:
                break


        state_vector =  np.concatenate((hand_vector,gamemode_vector,next_betting_vector)).reshape(1,-1)
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
    n_episodes = 10
    agent_betting = BettingAgentEasy(action_size)
    agent_skataufnahme = BettingAgentEasySkataufnahme()
    agent_decide = BettingAgentEasyDecide()
    agent_discard =BettingAgentEasyDiscard()

    env = BettingEnvironmentEasy()

    for e in range(n_episodes):
        state = env.reset()
        done = False


        while not done:
            action_betting = agent_betting.act(state)

            next_state_betting, reward_betting, done = env.step_betting(action_betting)

            action_skataufnahme = agent_skataufnahme.act(next_state_betting)

            next_state_skataufnahme, reward_skataufnahme, success_skataufnahme = env.step_take_skat(action_skataufnahme)

            action_decide = agent_decide.act(next_state_skataufnahme)

            next_state_decide, reward_decide, success_decide = env.step_decide(action_decide)

            if next_state_decide.get("skataufnahme"):
                action_discard = agent_discard.act(next_state_decide)

                next_state_discard,reward_discard,success = env.step_discard(action_discard)

                agent_discard.remember(next_state_decide,action_discard,reward_discard,next_state_discard,done)

            agent_betting.remember(state, action_betting, reward_betting, next_state_betting, done)

            agent_skataufnahme.remember(next_state_betting, action_skataufnahme, reward_skataufnahme, next_state_skataufnahme, done)

            agent_decide.remember(next_state_skataufnahme, action_decide, reward_decide, next_state_decide, done)

            state = next_state_decide

        if len(agent_betting.memory) > agent_betting.batch_size:
            agent_betting.train(agent_betting.batch_size,agent_skataufnahme,agent_decide,agent_discard)
            agent_skataufnahme.train(agent_skataufnahme.batch_size,agent_decide,agent_discard)
            agent_decide.train(agent_decide.batch_size,agent_discard)
            if len(agent_discard.memory) > agent_discard.batch_size:
                agent_discard.train(agent_discard.batch_size)
        if e % 10 == 0:

            print(e, agent_betting.epsilon / 10)
    agent_betting.model.save("model_betting_easy.keras")
    agent_skataufnahme.model.save("model_skataufnahme_easy.keras")
    agent_decide.model.save("model_decide_easy.keras")
    agent_discard.model.save("model_discard_easy.keras")





