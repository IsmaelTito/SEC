import numpy as np
import random
import platform
from keras import backend as K
import os
import tensorflow as tf

def set_keras_backend(backend):

    if K.backend() != backend:
        os.environ['KERAS_BACKEND'] = backend
        reload(K)
        assert K.backend() == backend

    config = tf.ConfigProto()
    jit_level = tf.OptimizerOptions.ON_1
    config.graph_options.optimizer_options.global_jit_level = jit_level
    sess = tf.Session(config=config)
    tf.keras.backend.set_session(sess)

plt = platform.system()
np.seterr(divide = 'ignore')

CodeOcean = False

if CodeOcean == True:
    base_path = '/root/capsule/code/AnimalAI-Olympics/env-win/'
    file_path = '/root/capsule/code/sec/data/simulations/'
    print("OS IS LINUX VM CAPSULE")
else:
    if plt == "Windows":
        base_path = '../AnimalAI-Olympics/env-win/'
        file_path = './data/simulations/'
        set_keras_backend("tensorflow")
        print("OS IS WINDOWS")
    else:
        base_path = '../AnimalAI-Olympics/env-lnx/'
        file_path = './data/simulations/'
        print("OS IS LINUX")

from exp_setup_getimgs_detour import id_generator, create_env, run_simulation
from agent_reactive import ReactiveAgent

#################################################################################################################

# SET HYPERPARAMETERS

experiments = 1
episodes = 10000
save_imgs = True

docker_training = False
environment_visible = False
real_time_plots = False


#################################################################################################################

# MAIN function
def run_experiment(seed, worker_id):

    env, arenas = create_env(seed, worker_id, base_path, arenas_n=episodes, docker=docker_training, env_view=environment_visible, capsule=CodeOcean)

    ID = 'ReactiveAgent-'+id_generator(6)+'_'

    agent = ReactiveAgent()

    results = run_simulation(ID, agent, env, arenas, base_path, file_path, episodes_n=episodes, fp_view=real_time_plots, save_imgs=save_imgs, capsule=CodeOcean)
    print('FINAL SCORE: ', results)
    
    env.close()

#################################################################################################################

# RUN experiment
seed = 0
worker_id = 0

if __name__ == '__main__':
    try:
        for i in range(experiments):
            print('EXPERIMENT NUMBER ', i)
            #seed = random.randint(1,10000)
            seed += 1
            #worker_id = random.randint(1,10)
            worker_id += 1
            run_experiment(seed, worker_id)

    except KeyboardInterrupt:
        print ('Simulation interrumpted!')
