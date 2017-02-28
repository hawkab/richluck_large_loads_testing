# -*- coding: utf-8 -*-

from joblib import Parallel , delayed
import multiprocessing , sys
from runTest import *

count = 10 #default

if len ( sys.argv )>1:
	count = int ( sys.argv[1])

inputs = range ( count )

num_cores = multiprocessing.cpu_count()
results = Parallel ( n_jobs = num_cores )( delayed ( runTest )( i ) for i in inputs )