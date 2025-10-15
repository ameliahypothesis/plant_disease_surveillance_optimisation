import os
os.environ["OMP_NUM_THREADS"] = "1"  # limit each process to 1 thread
#os.environ["OPENBLAS_NUM_THREADS"] = "1"
#os.environ["MKL_NUM_THREADS"] = "1"
import sys
module_dir = '/home/physics/estszj/research_project'
sys.path.append(module_dir)

from multiprocessing import Pool
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import LineString, Point, MultiLineString, box
from shapely.ops import unary_union
import datetime
from scipy.spatial.distance import pdist, squareform
from joblib import dump, load
from simulation import host_distribution_casava, simulate_ibm, logistic
from CONSTANT import ALPHA, BETA, SIGMA0, LOGISTIC_RATE, PREVALENCE


if __name__ == '__main__':
    direc = '/home/physics/estszj/research_project'
    cwd = '/home/physics/estszj/research_project/parameterise_beta/'
    filename_logbeta = f'logbeta_x10y3e5.joblib'
    filename_timediff = f'time_diff_x10y3e5.joblib'    # simulation data file name
    shp_road = gpd.read_file(f'{direc}/shapefiles/road northern DRC (BasSudNodMon_Survey_Road).shp')
    shp_area = gpd.read_file(f'{direc}/shapefiles/production northern DRC (northDRC_prod_1km2).shp')

    host_distr, road_sub = host_distribution_casava(road=shp_road, area=shp_area, 
                                        x_bound=[1e6, 1e6+269000], y_bound=[3e5, 3e5+269000], 
                                        grid_level = True, plot_poly=False, plot_point=False,
                                        plot_save_path=f'{cwd}')

    RATE=0.003120016864814313
    PREV_FINAL0=0.1067
    PREV_FINAL1=0.1418
    
    

    np.random.seed(0)
    num_simulations=10
    
    logbeta_arr = np.random.uniform(low=10, high=15, size=num_simulations)
    
    ### ORDER IS: host_distr,alpha, beta, logistic_rate, prev_threshold,entry_method='risk',num_init_S2C=1,init_point_ID=1700,seed=0
    params_list0 = [(host_distr, ALPHA, np.exp(logb), LOGISTIC_RATE, PREV_FINAL0, 'risk', 1, 1700, 0) for logb in logbeta_arr]
    params_list1 = [(host_distr, ALPHA, np.exp(logb), LOGISTIC_RATE, PREV_FINAL1, 'risk', 1, 1700, 0) for logb in logbeta_arr]
    
    
    
    ### parallel processing with timing
    start_time = datetime.datetime.now()
    print("Start time:", start_time, flush=True)
    
    
    ### parallel processing
    with Pool(48) as p:  # use a pool of 48 worker processors
        result0=p.starmap(simulate_ibm, params_list0)
        result1=p.starmap(simulate_ibm, params_list1)
    
    time_at_prev_arr0 = np.zeros_like(logbeta_arr)
    time_at_prev_arr1 = np.zeros_like(logbeta_arr)
    
    for i, sim0 in enumerate(result0):
        all_event_times = np.append(sim0['time_1st_S2C'], sim0['time_1st_C2I'])
        all_event_times=all_event_times[all_event_times!=np.inf]
        time_at_prev_arr0[i]= all_event_times.max()
    
    for j, sim1 in enumerate(result1):
        all_event_times = np.append(sim1['time_1st_S2C'], sim1['time_1st_C2I'])
        all_event_times=all_event_times[all_event_times!=np.inf]
        time_at_prev_arr1[j]= all_event_times.max()
    
    time_diff = time_at_prev_arr1-time_at_prev_arr0
    
    end_time = datetime.datetime.now()
    print("End time:", end_time, flush=True)
    print("Time taken for simulation:", end_time - start_time, flush=True)
    
    ### write data
    dump(logbeta_arr, os.path.join(cwd, filename_logbeta))
    dump(time_diff, os.path.join(cwd, filename_timediff))
    
    
    
        
