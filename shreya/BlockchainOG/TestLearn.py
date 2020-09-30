import pandas
import random
from random import *
import requests

# JSON = JavaScript Object Notation - an open-standard file format that uses
# human-readable text to transmit data objects consisting of attribute–value
# pairs and array data types (or any other serializable value).
# It is a very common data format used for asynchronous browser–server
# communication
# noinspection PyUnresolvedReferences
import json
# noinspection PyUnresolvedReferences
from time import time
# noinspection PyUnresolvedReferences
from urllib.parse import urlparse
# noinspection PyUnresolvedReferences
from uuid import uuid4
# Requests = licensed HTTP library
# Requests will allow you to send HTTP/1.1 requests using Python.
# Add content like headers, form data, multipart files, and parameters
# via simple Python libraries. It also allows you to access the response
# data of Python in the same way.
# noinspection PyUnresolvedReferences
from flask import Flask, jsonify, request

application = Flask(__name__)
# Import variables needed for each step [Parts/Production Time]
variables = pandas.read_csv('Data_Sheet.csv')
# Import Part UID used in each step
part_id = pandas.read_csv('PartUID_Sheet.csv')
# Keeps track of Part Number used from csv file
part_id_counter = []
part_id_counter.extend([0] * 30)
# Keeps track of the steps completed during parallel production
done_array = []
done_array.extend([0] * 17)
# Part List
part_list = ['Cover', 'Intrusion_Switch', 'WLAN_Card', 'Front_Bezel', 'Expansion_Card', 'Memory_Card',
             'CoinCell_Battery', 'Hard_Drive', 'Optical_Drive', 'Power_Supply', 'Heat_Sink_Assembly', 'Processor',
             'Processor_Socket', 'System_Fan', 'Thermal_Sensor', 'Power_Switch', 'IO_Panel', 'System_Board', 'Screws',
             'Grommets', 'Power_Cable', 'Data_Cable', 'WLAN_Cable', '4pin_Power_Cable', '8pin_Power_Cable', 'Fan_Cable',
             'Captive_Screws', 'Thermal_Sensor_Cable', 'USB_Cable', 'N_A']
total_number_of_steps = 17

# HTTP Transfer over Blockchain
Post_Transaction = 'http://localhost:5000/transactions/new'
Mine_Transaction = 'http://localhost:5000/mine'

total_number_of_parts = input("Enter number of parts to make ")
total_number_of_parts = int(total_number_of_parts)


def get_production_time(step):
    print("Production time running")
    time_min = variables.loc[step, 'Production_Time_Min']
    time_max = variables.loc[step, 'Production_Time_Max']
    production_time = randint(time_min, time_max)
    return production_time


def get_validation_time(step):
    if variables.loc[step, 'Validator_Type'] == "Human":
        time_min = variables.loc[step, 'Validation_Time_Min']
        time_max = variables.loc[step, 'Validation_Time_Max']
        validation_time = randint(time_min, time_max)
    else:
        validation_time = 0
    return validation_time


def is_busy(part, step, production_time):
    free = time_array[part][step] - production_time
    print("is_busy: Free ", free)
    if free >= production_time:
        return True
    else:
        return False


def get_step_number(previous_step, part, step, production_time):
    next_step_1 = variables.loc[step, 'Next_Step_1']
    next_step_2 = variables.loc[step, 'Next_Step_2']
    next_step_3 = variables.loc[step, 'Next_Step_3']
    next_step_4 = variables.loc[step, 'Next_Step_4']
    step_array = []
    if next_step_1 > 0:  # add step number to array only if it is an integer
        step_array.append(next_step_1)
    if next_step_2 > 0:
        step_array.append(next_step_2)
    if next_step_3 > 0:
        step_array.append(next_step_3)
    if next_step_4 > 0:
        step_array.append(next_step_4)
    print("get_step_number: Step array", step_array)
    # remove elements that are busy
    for x1 in range(0, len(step_array)):
        if is_busy(part, step_array[x1], production_time):
            step_array.remove(step_array[x1])
    # if array size becomes 0 return next_step_1
    if len(step_array) == 0:  # step 17 will give error as all entries are -1. Add terminating condition
        step_array[0] = next_step_1
    import random
    next_step_option = random.choice(step_array)
    print("NEXT STEP OPTION RANDOM CHOICE", next_step_option)
    # special case for step = 4
    # special case for step = 9
    # special case for array size = 0
    if step == 4:
        if done_array[1] == 1:
            if done_array[2] == 1:
                if done_array[3] == 1:
                    next_step_option = 5
                else:
                    next_step_option = 3
            else:
                next_step_option = 2
        else:
            next_step_option = 1

    if step == 9:
        if done_array[6] == 1:
            if done_array[7] == 1:
                if done_array[8] == 1:
                    next_step_option = 10
                else:
                    next_step_option = 8
            else:
                next_step_option = 7
        else:
            next_step_option = 6

    print("next step option BEFORE ENTERING RECURSIVE FUNCTION", next_step_option)
    if done_array[next_step_option] == 1:
        # previous step number needed to ensure it does not go into infinite recursion. Remove this option from steps
        # wrong production time. It should be for the give next_step_option
        print("STEP DONE")
        return get_step_number(step, part, next_step_option, production_time)
    else:
        print("NEXT STEP END", next_step_option)
        return next_step_option


# Initialise variables needed
# Time to complete entire production process
cumulative_time = 0
cumulative_delay = 0
# Time to complete production of a single part
time_stamp = 0
step_number = 0
step_count = 0
parts = 0
previous_step_number = -1
# Data analysis parameters
failed_pri_validation = 0
failed_sec_validation = 0
rows, cols = (total_number_of_parts, total_number_of_steps)
rework = [[0 for i in range(cols)] for j in range(rows)]
time_array = [[0 for i in range(cols)] for j in range(rows)]
prod_time_array = [0]*total_number_of_steps


while parts < total_number_of_parts:
    print('Part Number:')
    print(parts)
    for z in range(0, total_number_of_steps):
        prod_time_array[z] = get_production_time(z)
    #   variables.loc[z, 'Validation_Time'] = get_validation_time(z)
    while step_count < total_number_of_steps:
        step_status = 'Pass'
        print("Done array", done_array)
        print("Chosen step number ", step_number)
        # time array is not updated
        prod_time = prod_time_array[step_number]
        time_array[parts][step_number] += prod_time
        if step_status == 'Pass':
            previous_step_number = step_number
            done_array[step_number] += 1
            print("Chosen step number before", step_number)
            step_number = get_step_number(previous_step_number, parts, step_number, prod_time)
            print("Chosen step number after ", step_number)
            step_count += 1

    done_array = [0] * 17
    parts += 1
    step_count = 0
