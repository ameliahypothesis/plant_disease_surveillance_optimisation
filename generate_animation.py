# Generate animation of randomly selected simulations
import time
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import datetime
from scipy.spatial.distance import pdist, squareform
from joblib import dump, load
import geopandas as gpd
from shapely.geometry import LineString, Point, MultiLineString, box
from shapely.ops import unary_union
import os
import sys
module_dir = '/home/physics/estszj/research_project'
sys.path.append(module_dir)
from simulation import vlogistic
from CONSTANT import ALPHA, BETA, SIGMA0, LOGISTIC_RATE, PREVALENCE

cwd = '/gpfs/home/physics/estszj/research_project/ana00_runSimulation/'
filename_sim = 'df_sims02.joblib'
save_dir=f'{cwd}/animation02/'

# Read data
data_sims = load(os.path.join(cwd, filename_sim))

num_sim=10

# total number of simulations
num_sim_tot = len(data_sims)
rand_ID = np.random.choice(np.arange(num_sim_tot), size=num_sim, replace=False)

print(f'num of animations:{num_sim}, alpha, beta, sigma0, logistic rate, prev are: {ALPHA}, {BETA}, {SIGMA0}, {LOGISTIC_RATE}, {PREVALENCE}')

start_time = datetime.datetime.now()
print("Start time:", start_time, flush=True)

for j in range(num_sim):
    
    ID = rand_ID[j]
    filename_ani=f'animation_prev05_sim{ID}.gif'
    sim_j = data_sims[ID]
    time_NextEventAll_arr = np.append(sim_j['time_1st_S2C'], sim_j['time_1st_C2I'])
    time_NextEventAll_arr_sorted = np.sort(time_NextEventAll_arr).copy()
    time_NextEventAll_arr_sorted_sub = time_NextEventAll_arr_sorted[time_NextEventAll_arr_sorted!=np.inf]
    
    time_max = int(time_NextEventAll_arr_sorted_sub.max())+10
    print('animation#:',j, 'time max=', time_max,  flush=True)
    
    times = np.arange(0, time_max, 10)
    
    x = sim_j['x'].copy()
    y = sim_j['y'].copy()
    host_population = sim_j['host_population'].copy()
    state = sim_j['state'].copy()
    time_1st_S2C = sim_j['time_1st_S2C'].copy()
    time_1st_C2I = sim_j['time_1st_C2I'].copy()
  
    series_ID_inS = np.zeros((len(times), x.shape[0]), dtype=bool)
    series_ID_inC = np.zeros((len(times), x.shape[0]), dtype=bool)
    series_ID_inI = np.zeros((len(times), x.shape[0]), dtype=bool)
    series_x_inS = np.zeros((len(times), x.shape[0]))
    series_y_inS = np.zeros((len(times), y.shape[0]))
    series_x_inC = np.zeros((len(times), x.shape[0]))
    series_y_inC = np.zeros((len(times), y.shape[0]))
    series_x_inI = np.zeros((len(times), x.shape[0]))
    series_y_inI = np.zeros((len(times), y.shape[0]))
    series_host_prop_inC = np.zeros((len(times), x.shape[0]))
    series_host_prop_inI = np.zeros((len(times), x.shape[0]))
    series_prevalence_inI = np.zeros(len(times))
    series_prevalence = np.zeros(len(times))
    
    for i, t in enumerate(times):
        # print(t)
        ID_inS_at_t = time_1st_S2C > t
        ID_inC_at_t = (time_1st_S2C <= t) & (time_1st_C2I > t)
        ID_inI_at_t = time_1st_C2I <= t
    
        x_inS_at_t, y_inS_at_t = x[time_1st_S2C > t], y[time_1st_S2C > t]
        x_inC_at_t, y_inC_at_t = x[(time_1st_S2C <= t) & (time_1st_C2I > t)], y[(time_1st_S2C <= t) & (time_1st_C2I > t)]
        x_inI_at_t, y_inI_at_t = x[time_1st_C2I <= t], y[time_1st_C2I <= t]
    
        time_1st_S2C_dummy = time_1st_S2C.copy()
        time_1st_C2I_dummy = time_1st_C2I.copy()
        time_1st_S2C_dummy[time_1st_S2C> t] = np.inf
        time_1st_C2I_dummy[time_1st_C2I> t] = np.inf
        host_num_inC, host_prop_inC, host_num_inI, host_prop_inI = vlogistic(time=t,
                                                                             time_eventS2C = time_1st_S2C_dummy,
                                                                             time_eventC2I = time_1st_C2I_dummy,
                                                                             host_population = host_population,
                                                                             sigma0 = SIGMA0,
                                                                             c = LOGISTIC_RATE)
    
        series_ID_inS[i] = ID_inS_at_t
        series_ID_inC[i] = ID_inC_at_t
        series_ID_inI[i] = ID_inI_at_t
        series_host_prop_inC[i] = host_prop_inC
        series_host_prop_inI[i] = host_prop_inI
        series_prevalence_inI[i] = np.sum(host_num_inI)/ np.sum(host_population)
        series_prevalence[i] = np.sum(host_num_inC + host_num_inI)/ np.sum(host_population)
      
      
    # plot animation =================
    fig, ax = plt.subplots(figsize = (10,10))
    times_sub = times
    def animate(T):
        ax.clear()
        t = times_sub[T]
        hostpop0 = sim_j['host_population'] == 0
        
        # plt.scatter(xy[:,0], xy[:,1], c='lightgrey', s=5, alpha=0.5)
        fig1=plt.scatter(sim_j['x'] ,sim_j['y'], marker='s', s=50, linewidths=0, edgecolors='none', alpha=0.2, 
                          c=sim_j['host_population'], cmap='RdYlGn_r')
                          
        plt.scatter(sim_j['x'][hostpop0] ,sim_j['y'][hostpop0], marker='s', s=50, linewidths=0, edgecolors='none', alpha=1, 
                          c='black')
        # plt.colorbar(fig1, ax=ax, label='number of plants')
        # plt.scatter(x[series_ID_inS[i, :]] , y[series_ID_inS[i, :]], s=5, alpha=0.3, label = 'S')
        plt.scatter(x[series_ID_inC[T, :]] , y[series_ID_inC[T, :]] , s=15, alpha=0.8, label = 'C')
        plt.scatter(x[series_ID_inI[T, :]] , y[series_ID_inI[T, :]] , s=30, alpha=1, c='r', label = 'I')
        plt.legend()
        ax.set_title(f'week {t}, prev={series_prevalence[T]}')
    
    animation = FuncAnimation(fig, animate, frames=len(times_sub))
    animation.save(f'{save_dir}/{filename_ani}', writer=PillowWriter(fps=10))
  
end_time = datetime.datetime.now()
print("End time:", end_time, flush=True)
print("Time taken for simulation:", end_time - start_time, flush=True) 