## Trainer Srcipt for Ray Cluster 
## Version 0.1 
import time
from datetime import datetime
import pandas as pd
import pickle 
import sys
sys.path.append("./findrl_ray/finenv")
sys.path.append("./FinRL")
import finrl
from finenv.env_stocktrading import StockTradingEnv
from finenv.preprocessors import data_split

import argparse

import psutil
import ray
ray._private.utils.get_system_memory = lambda: psutil.virtual_memory().total
from ray.tune.registry import register_env
from gymnasium.wrappers import EnvCompatibility

from ray.rllib.agents import ppo

#Parser for num_workers variable in training jobs## 
parser = argparse.ArgumentParser(description="num_workers")
parser.add_argument('--workers',type=int,help='num_workers')
args = parser.parse_args()
num_workers = args.workers
                    
print('args loaded',num_workers)

#from finrl.meta.data_processor import DataProcessor

# load the DataFrame from a pickle file, point to home of clutser container. 
train = pd.read_csv('dataset/train_data.csv')
train = train.set_index(train.columns[0])
train.index.names = ['']

INDICATORS = ['macd','boll_ub','boll_lb','rsi_30','cci_30','dx_30','close_30_sma','close_60_sma']

stock_dimension = len(train.tic.unique())
state_space = 1 + 2*stock_dimension + len(INDICATORS)*stock_dimension
buy_cost_list = sell_cost_list = [0.001] * stock_dimension
num_stock_shares = [0] * stock_dimension

def env_creator(env_config):
    # env_config is passed as {} and defaults are set here
    df = env_config.get('df', train)
    hmax = env_config.get('hmax', 10000)
    initial_amount = env_config.get('initial_amount', 1000000)
    num_stock_shares = env_config.get('num_stock_shares', [0] * stock_dimension)
    buy_cost_pct = env_config.get('buy_cost_pct', buy_cost_list)
    sell_cost_pct = env_config.get('sell_cost_pct', sell_cost_list)
    state_space = env_config.get('state_space', 1 + 2*stock_dimension + len(INDICATORS)*stock_dimension)
    stock_dim = env_config.get('stock_dim', stock_dimension)
    tech_indicator_list = env_config.get('tech_indicator_list', INDICATORS)
    action_space = env_config.get('action_space', stock_dimension)
    reward_scaling = env_config.get('reward_scaling', 1e-3)
    return EnvCompatibility(StockTradingEnv(
        df=df,
        hmax=hmax,
        initial_amount=initial_amount,
        num_stock_shares=num_stock_shares,
        buy_cost_pct=buy_cost_pct,
        sell_cost_pct=sell_cost_pct,
        state_space=state_space,
        stock_dim=stock_dim,
        tech_indicator_list=tech_indicator_list,
        action_space=action_space,
        reward_scaling=reward_scaling
    ))
ray.shutdown()
print(f"ray is being initialized")
config = ppo.PPOConfig()  
config = config.training(gamma=0.9, lr=0.00025, kl_coeff=0.3)  
config = config.resources(num_gpus=0)  
config = config.rollouts(num_rollout_workers=num_workers)

# registering the environment to ray
register_env("finrl", env_creator)
#trainer = ppo.PPOTrainer(env='finrl', config=config)
trainer = config.build(env="finrl") 
    
# Train away -------------------------------------------------------------
total_episodes=1000
agent_name = 'ppo'
ep = 0
results = []
job_time = time.time()
date = datetime.now().strftime('%y%m%d')

while ep <= total_episodes:
    start = time.time()
    results.append(trainer.train())
    ep += 1
    if ep % 5 == 0:
        rwd = results[-1]['episode_reward_mean']
        print(f'Mean Rwd:{rwd}')   
    print(f'Current episode{ep} \nTime/Its:{time.time()-start:.2f}s')
    if ep % 100 == 0:
        cwd_checkpoint = f"results/{agent_name}_{date}_{ep}"
        trainer.save(cwd_checkpoint)
        print(f"Checkpoint saved in directory {cwd_checkpoint}")
        
print(f'Complete training job took{time.time()-job_time:.2f}s')