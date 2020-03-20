#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''

一个基本的智能体与环境交互案例

'''


from gym import envs
import gym
import numpy as np


# 智能体对象
class BeSpokeAgent:
    def __init__(self, env):
        pass

    def decide(self, observation):
        position, velocity = observation
        lb = min(-0.09*(position+0.25)**2+0.03, 0.3*(position+0.9)**4-0.008)
        ub = -0.07*(position+0.38)**2+0.06
        if lb < velocity < ub:
            action = 2
        else:
            action = 0
        return action

    def learn(self, *args):
        pass


# 智能体与环境的交互
def play_montecarlo(env, agent, render=False, train=False):
    '''

    :param env:
    :param agent:
    :param render:
    :param train:
    :return: 返回奖励
    '''
    episode_reward = 0
    observation = env.reset()
    while True:
        if render:
            env.render()

        action = agent.decide(observation)
        next_observation, reward, done, _ = env.step(action)
        episode_reward += reward
        if train:
            agent.learn(observation, action, reward, done)
        if done:
            break
        observation = next_observation

    return episode_reward


if __name__ == "__main__":

    # 强化学习环境查看
    envs_specs = envs.registry.all()
    envs_id = [envs_spec.id for envs_spec in envs_specs]
    print(envs_id)
    env = gym.make("MountainCar-v0")
    agent = BeSpokeAgent(env)
    print('观测空间={}'.format(env.observation_space))
    print('动作空间={}'.format(env.action_space))
    print('观测范围={}~{}'.format(env.observation_space.low, env.observation_space.high))
    print('动作数={}'.format(env.action_space.n))
    env.seed(0)
    # 一次性
    episode_reward = play_montecarlo(env, agent, render=True)
    print('回合奖励{}'.format(episode_reward))
    # 10个回合
    episode_rewards =[play_montecarlo(env, agent, render=True) for _ in range(10)]
    print('100 回合输出奖励{}'.format(np.mean(episode_rewards)))