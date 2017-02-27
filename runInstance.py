# -*- coding: utf-8 -*-

from joblib import Parallel, delayed
import multiprocessing
from runTest import *

inputs = range(2) 

num_cores = multiprocessing.cpu_count()
    
results = Parallel(n_jobs=num_cores)(delayed(runMinecraftTest)() for i in inputs)