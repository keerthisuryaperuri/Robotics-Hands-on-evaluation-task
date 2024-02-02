import random
import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta



# Parameters
N = 5  # Number of robots
L, W = 9, 6  # Grid size
P = 3  # Number of packing stations
mean_interval = 30  # Mean interval between orders (seconds)
variance = 25  # Variance for order generation
mean_items_per_order = 6  # Mean number of items per order
variance_items_per_order = 9  # Variance for item count distribution
packing_time_per_item = 5  # Time to pack one item (seconds)
robot_speed = 1  # Robot speed in m/s

# Simulation time
simulation_time = 3600  # 1 hour in seconds

# Initialize variables and data structures
orders = []
current_packing_station = 1
current_order_num = 1
current_time = 0

# Define a function to generate random item lists
def generate_item_list():
    num_items = max(1, int(np.random.normal(mean_items_per_order, variance_items_per_order)))
    return sorted(random.sample(range(1, L * W + 1), num_items))

# Define a function to calculate Manhattan distance between two nodes
def manhattan_distance(node1, node2):
    x1, y1 = divmod(node1 - 1, L)
    x2, y2 = divmod(node2 - 1, L)
    return abs(x1 - x2) + abs(y1 - y2)

# Simulate order generation (Part 1)
while current_time < simulation_time:
    order = {
        'generated_time': str(timedelta(seconds=current_time)),
        'order_num': current_order_num,
        'item_list': generate_item_list(),
        'packing_station': current_packing_station
    }
    orders.append(order)
    # Update variables for the next order
    current_order_num += 1
    current_packing_station = (current_packing_station % P) + 1
    time_interval = max(0, int(np.random.normal(mean_interval, variance)))
    current_time += time_interval

# Simulation of picking modes and performance comparison (Part 2)
split_time_list = []
whole_time_list = []
order_num_list = []
pick_node_list = []
results1 =[]

whole_order_time = 0
split_order_time = 0

for order in orders:
    for it in order['item_list']:
        for robot_num in range(1, N + 1):
            # Simulate picking the order using the two modes
            start_time = max(whole_order_time, split_order_time)
            
            # Whole order by one robot
            whole_order_time = start_time + len(order['item_list']) * packing_time_per_item
            
            # Split order into items, one robot per item
            split_order_time = start_time + packing_time_per_item

        # Calculate the time taken to complete the split order
        split_order_completion_time = split_order_time + manhattan_distance(1, order['packing_station'])
        
        split_time_list.append(
        time.strftime("Day: %d   %H:%M:%S", time.gmtime(split_order_completion_time)),    
        )
        order_num_list.append(
        order['order_num'],
        )
        pick_node_list.append(
        it,
        )

    whole_order_completion_time = whole_order_time + manhattan_distance(1, order['packing_station']) 
    for it in order['item_list']:   
        whole_time_list.append(
        time.strftime("Day: %d   %H:%M:%S", time.gmtime(whole_order_completion_time)),
        )
        
data1 = {'Order Num': order_num_list,
         'Pick_node': pick_node_list,
         'completed_time_mode_1': whole_time_list,
         'completed_time_mode_2': split_time_list,
        }

# Create a DataFrame to store the results
results1_df = pd.DataFrame(data1)

# Write the results to a CSV file
results1_df.to_csv('report.csv', index=False)

