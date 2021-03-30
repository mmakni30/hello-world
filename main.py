from env import Construction
import numpy as np
import random
import pygame
import time
import matplotlib.pyplot as plt

# clock = pygame.time.Clock()
env = Construction()
Q = np.random.rand(env.observation_space.n, env.action_space.n)
episode_number = 2001
SHOW_EVERY = 100
ep_rewards = []
aggr_ep_rewards = {'ep': [], 'avg': [], 'max': [], 'min': []}
D_list = []
D = []
X = []


def take_action(state, q, eps):
    # Take an action
    if random.uniform(0, 1) < eps:
        action = random.randint(0, 3)
    else:  # Or greedy action
        action = np.argmax(q[state])
    return action


for i in range(episode_number):
    time1 = time.time()
    distance = 0
    X.append(i)
    episode_reward = 0
    window = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Construction Game")
    st = env.reset()

    while not env.crane.hook.is_finished():
        # clock.tick(1000)

        at = take_action(st, Q, 0.4)
        stp1, reward, d = env.step(at)
        atp1 = take_action(stp1, Q, 0.0)
        if atp1 == 0:
            env.crane.boom.turn_right(value=1)
            if env.crane.hook.busy:
                env.package1.move_package()
        elif atp1 == 1:
            env.crane.boom.turn_left(value=1)
            if env.crane.hook.busy:
                env.package1.move_package()
        elif atp1 == 2:
            env.crane.hook.move_along_further(value=1)
            if env.crane.hook.busy:
                env.package1.move_package()
        elif atp1 == 3:
            env.crane.hook.move_along_closer(value=1)
            if env.crane.hook.busy:
                env.package1.move_package()
        elif atp1 == 4:
            env.crane.hook.right_further(value=1)
            if env.crane.hook.busy:
                env.package1.move_package()
        elif atp1 == 5:
            env.crane.hook.right_closer(value=1)
            if env.crane.hook.busy:
                env.package1.move_package()
        elif atp1 == 6:
            env.crane.hook.left_further(value=1)
            if env.crane.hook.busy:
                env.package1.move_package()
        elif atp1 == 7:
            env.crane.hook.left_closer(value=1)
            if env.crane.hook.busy:
                env.package1.move_package()
        distance += d
        Q[st][at] = Q[st][at] + 0.1 * (reward + 0.9 * Q[stp1][atp1] - Q[st][at])
        st = stp1
        window.fill(pygame.Color("grey"))  # Fills the screen with black
        env.render(window)
    ep_rewards.append(episode_reward)
    if not i % SHOW_EVERY:
        average_reward = sum(ep_rewards[-SHOW_EVERY:]) / SHOW_EVERY
        aggr_ep_rewards['ep'].append(i)
        aggr_ep_rewards['avg'].append(average_reward)
        aggr_ep_rewards['max'].append(max(ep_rewards[-SHOW_EVERY:]))
        aggr_ep_rewards['min'].append(min(ep_rewards[-SHOW_EVERY:]))
        D_list.append(distance)
    time2 = time.time()
    duree = time2 - time1
    D.append(duree)
    pygame.quit()

plt.plot(X, D, label="duree")
plt.legend(loc=4)
plt.show()
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label="average rewards")
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label="max rewards")
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label="min rewards")
plt.legend(loc=4)
plt.show()
plt.plot(aggr_ep_rewards['ep'], D_list, label="distance parcourue")
plt.legend(loc=4)
plt.show()
