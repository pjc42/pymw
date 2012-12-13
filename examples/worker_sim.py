#!/usr/bin/env python

from pymw import *
import random
import cProfile
import pstats

# Select a worker and task from each list to be matched together
# If no matches are suitable at this time, return None for both
def worker_scheduler(task_list, worker_list):
	return task_list[0], worker_list[0]

# Worker speed is the number of instructions a worker can perform per second
# In this case, worker speeds are a normal distribution with mean 2 and stddev 0.3, with a minimum speed of 1
def worker_speed(worker_num):
	return max(1, random.normalvariate(2, 9))

# Generate worker availabilities
# Worker availabilities are a list of pairs, each pair is a time span and availability A from 0 to 1
# This means that for the time span, the worker runs at A*(normal speed)
# In this case, workers oscillate on and off every 100 seconds and shut down after 10000 seconds
def worker_avail(worker_num):
	avail_lens = [100 for i in range(100000)]
	avail_fracs = [i%2 for i in range(100000)]
	return avail_lens, avail_fracs

# Task lengths are in terms of number of instructions
# In this case short tasks are uniformly distributed in [15, 30] and long tasks are in [60, 90]
def short_task_run_estimate(worker):
	return 15/worker._speed

def long_task_run_estimate(worker):
	return 60/worker._speed

def run_everything():
	# Create the grid simulation interface and PyMW_Master object
	interface_obj = pymw.interfaces.grid_simulator.GridSimulatorInterface()
	pymw_master = pymw.PyMW_Master(interface=interface_obj, scheduler_func=worker_scheduler)
	
	# Create 10 workers with characteristics generated by worker_speed() and worker_avail()
	interface_obj.generate_workers(100, worker_speed, worker_avail)
	
	event_trace_file = open("/Users/eheien/Downloads/overnet03_tab/event_trace.tab", "r")
	#interface_obj.read_workers_from_fta_tab_files(event_trace_file, num_workers=500)
	event_trace_file.close()
	
	# Run 100 long tasks and 100 short tasks
	tasks = []
	tasks.extend([pymw_master.submit_task(long_task_run_estimate) for i in range(100)])
	tasks.extend([pymw_master.submit_task(short_task_run_estimate) for i in range(100)])
	for task in tasks:
		res_task, res = pymw_master.get_result(task)
	
	# Print the final run statistics	
	stats = pymw_master.get_status()
	del stats["tasks"]
	print(stats)

run_everything()
#cProfile.run('run_everything()', 'fooprof')
#p = pstats.Stats('fooprof')
#p.sort_stats('time').print_stats()
