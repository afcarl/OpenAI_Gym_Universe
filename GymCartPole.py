import gym
import tensorflow as tf
import random
import numpy as np
from gym import wrappers
env = gym.make('CartPole-v0')
env = wrappers.Monitor(env, '/tmp/cartpole-experiment-1', force=True)

gamma = .99

# This neural network is going to take in both a state and an action 
# and is then going to output the action value function for being in 
# that state and taking that action
def neuralNet(x):
	W_1 = tf.get_variable('w_1',[4, 10], initializer=tf.random_uniform_initializer())
	h_1 = tf.matmul(x, W_1)
	W_2 = tf.get_variable('w_2', [10, 2], initializer=tf.random_uniform_initializer())
	y_ = tf.nn.softmax(tf.matmul(h_1, W_2))
	return y_ #represents the q value

sess = tf.Session()
x = tf.placeholder(tf.float32, shape=[1, 4]) #represents the state
y = tf.placeholder(tf.float32, shape=[1]) #represents true Q function
q_value = neuralNet(x)
loss = tf.reduce_mean(tf.square(y - q_value)) #MSE loss
trainer = tf.train.AdamOptimizer().minimize(loss)
sess.run(tf.global_variables_initializer())

epochs = 50
for e in range(epochs):
	initial_state = env.reset() #Observing initial state
	total_reward = 0
	for i in range(200):
	    env.render()
	    if i == 0:
	    	action = env.action_space.sample() #Selecting a random first action
	    else:
	    	action = np.argmax(sess.run([q_value],feed_dict={x: initial_state}))
	    	# Selecting an action based on a policy, not just a random choice. The action
	    	# is determined based on whichever action has the largest q value
	    initial_state = np.asarray(initial_state)
	    initial_state = initial_state.reshape([1, 4])
	    q_current = sess.run([q_value],feed_dict={x: initial_state})
	    next_state, reward, done, info = env.step(action) #Carrying out the action and observing new state and reward
	    next_state = np.asarray(next_state)
	    next_state = next_state.reshape([1, 4])	    
	    q_next = sess.run([q_value],feed_dict={x: next_state})
	    q_max = np.max(q_next) #Holds the max q value for the best action you could have taken
	    trueQvalue = reward + gamma*(q_max)
	    trueQvalue = np.asarray(trueQvalue)
	    trueQvalue = trueQvalue.reshape([1])
	    _, n_loss = sess.run([trainer, loss],feed_dict={x: initial_state, y: trueQvalue})
	    initial_state = next_state
	    if done == True:
	    	break

env.close()
#gym.upload('/tmp/cartpole-experiment-1', api_key='sk_UuAYsHNcSbuQlWPIuc7ZuQ')