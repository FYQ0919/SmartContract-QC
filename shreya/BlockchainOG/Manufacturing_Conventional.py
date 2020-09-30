"""
Project Title: Blockchain FYP
Program title: Manufacturing_Conventional
This program simulates a conventional manufacturing scenario for assembly of CPUs
It calculates the time taken to complete production of user-defined number of products, part quality, rework status
and other parameters for data analysis of project
Written by Shreya Sinha
"""
from random import *
import pandas
import numpy

total_number_of_parts = input("Enter number of parts to make ")
total_number_of_parts = int(total_number_of_parts)

parts = 0
step_number = 0
total_number_of_steps = 17

# Import variables needed for each step [Parts/Production Time]
variables = pandas.read_csv('Data_Sheet.csv')
# Variables to conduct data analysis
good = 0
poor = 0
re_no = 0
pri_good_status = 0
pri_poor_status = 0
sec_good_status = 0
sec_poor_status = 0
wrong_validation = 0


# *************************** FUNCTIONS *************************************************


def get_step_status():
    """
    Determines if a manufacturing process is carried out successfully or not
    :return: Step status
    :rtype: string
    """
    probability = randint(1, 100)
    if probability < 95:
        return "Pass"
    else:
        return "Fail"


def get_production_time(step):
    """
    Determines the production time for a step between the given upper and lower bound in the excel for a given step
    :param step: manufacturing process
    :return: production time
    """
    time_min = variables.loc[step, 'Production_Time_Min']
    time_max = variables.loc[step, 'Production_Time_Max']
    production_time = randint(time_min, time_max)
    return production_time


def calculate_timestamp(part, step):
    """
    Calculates the time taken to complete the production of a part
    :param part: assembly number/product
    :param step: manufacturing process being carried out
    :return: time at which production was completed
    """
    if part == 0:
        # Calculate Timestamp for current step
        if step == 0:
            time_stamp[part][step] += variables.loc[step, 'Production_Time']
            # print("Part number: ", part, " step number: ", step + 1, " Timestamp1: ",
            # time_stamp[part][step])
        else:
            time_stamp[part][step] += variables.loc[step, 'Production_Time'] + time_stamp[part][step - 1]
            # print("Part number: ", part, " step number: ", step + 1, " Timestamp2: ",
            # time_stamp[part][step])
    else:
        if step == 0:
            time_stamp[part][step] += variables.loc[step, 'Production_Time'] + time_stamp[part - 1][step]
            # print("Part number: ", part, " step number: ", step + 1, " Timestamp3: ",
            # time_stamp[part][step])
        else:
            time_stamp[part][step] += variables.loc[step, 'Production_Time'] + max(time_stamp[part - 1][step],
                                                                                   time_stamp[part][step - 1])
            # print("Part number: ", part, " step number: ", step + 1, " Timestamp4: ",
            # time_stamp[part][step])

    time_stamp[part][step] += variables.loc[step, 'Validation_Time']
    return


def get_validation_time(step):
    """
    Determine validation time for a step based on a given lower and upper limit
    Only human validators take extra time for validation as they can only perform one task at a time
    """
    if variables.loc[step, 'Validator_Type'] == "Human":
        time_min = variables.loc[step, 'Validation_Time_Min']
        time_max = variables.loc[step, 'Validation_Time_Max']
        validation_time = randint(time_min, time_max)
    else:
        validation_time = 0
    return validation_time


def actual_part_status():
    """
    Finds the actual part status of an assembly to compare with simulation results
    """
    for Row in range(0, total_number_of_parts):
        for Column in range(0, total_number_of_steps):

            quay = randint(1, 100)
            if quay < 85:
                actual_quality[Row][Column] = "Good"
            else:
                actual_quality[Row][Column] = "Poor"
    return


def calculate_good(part_number):
    good_no = 0
    for i in range(0, total_number_of_steps):
        if quality[part_number][i] == 'Good':
            good_no += 1
    return good_no


def calculate_poor(part_number):
    poor_no = 0
    for i in range(0, total_number_of_steps):
        if quality[part_number][i] == 'Poor':
            poor_no += 1
    return poor_no


def count_2d(R, C):
    q = 0
    for c in range(0, C):
        if quality[R][c] == 'Good' or quality[R][c] == 'Poor':
            q += 1
    return q


def calculate_incorrect_validation(part_number):
    """
    Determining the discrepancy in secondary validation by comparing with the randomly generated actual status of
    manufacturing processes.
    :return: number of processes that have been incorrectly validated
    :rtype: integer
    """
    bf = 0  # break factor for incrementing actual row number
    act_row = 0
    incorrect_validation = 0
    for nr in range(0, part_number - 1):
        for nc in range(0, total_number_of_steps - 1):
            # print("nr", nr, "nc", nc, "act row", act_row)
            if count_2d(nr, total_number_of_steps) != 17:
                bf = 1
                # print("Count", count_2d(nr, total_number_of_steps))
                break

            if quality[nr][nc] != actual_quality[act_row][nc]:
                # print("Actual", actual_quality[act_row][nc], "Quality", quality[nr][nc], "act row", act_row)
                incorrect_validation += 1
        if bf == 0:
            act_row += 1
        else:
            bf = 0

    return incorrect_validation


def count_quality():
    """
    Determining if an assembly process is completed (all 17 steps)
    :return: number of steps completed in the assembly of a part
    :rtype: integer
    """
    proc = 0
    for xx in range(0, total_number_of_parts):
        for yy in range(0, total_number_of_steps):
            if quality[xx][yy] == 'Good' or quality[xx][yy] == 'Poor':
                proc += 1
    return proc


# Initialise a 2D array to store all timestamps
rows, cols = (total_number_of_parts, total_number_of_steps)
time_stamp = [[0 for i in range(cols)] for j in range(rows)]
# 2D Array to store actual part quality
actual_quality = [['' for i in range(cols)] for j in range(rows)]
# 2D Array to store the part status after each step simulation
quality = [['' for i in range(cols)] for j in range(rows)]
# 0 - part cannot be reworked. 1 part can be reworked
rework = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Calculate the actual part statuses before starting simulation
actual_part_status()
print(actual_quality)
# Simulation Start
while parts < total_number_of_parts:
    # print('Part Number:')
    # print(parts)

    while step_number < total_number_of_steps:
        # Determine step pass/fail
        step_status = get_step_status()
        # Determine Production Time
        variables.loc[step_number, 'Production_Time'] = get_production_time(step_number)
        variables.loc[step_number, 'Validation_Time'] = get_validation_time(step_number)
        # print("Production time ", variables.loc[step_number, 'Production_Time'])
        # print("Validation time ", variables.loc[step_number, 'Validation_Time'])
        # print("Step Status :", step_status)
        calculate_timestamp(parts, step_number)
        # Primary Validation status
        if step_status == 'Pass':
            part_quality = 'Good'
            pri_good_status += 1

        else:
            part_quality = 'Poor'
            pri_poor_status += 1
        # Calculating waste %
        if step_number == total_number_of_steps - 1:
            good += calculate_good(parts)
            poor += calculate_poor(parts)
        # Check if part needs to be reworked or move to next step
        if step_status == 'Pass':
            quality[parts][step_number] = part_quality

        else:
            if rework[step_number] != 0:
                # This part can be reworked
                re_no += 1
                quality[parts][step_number] = 'Good'
                time_stamp[parts][step_number] += variables.loc[step_number, 'Production_Time']
                # print("new timestamp", time_stamp[parts][step_number])
                good += 1
            else:
                # This part has been scrapped and a new part must be made
                total_number_of_parts += 1
                # Copy previous part's timestamps into the array for scrapped part to calculate subsequent timestamps
                if parts != 0:
                    for i in range(step_number + 1, total_number_of_steps):
                        time_stamp[parts][i] = time_stamp[parts - 1][i]
                # Append a row to the timestamp array for the new part
                row = []
                row.extend([0] * total_number_of_steps)
                time_stamp = numpy.vstack([time_stamp, row])
                # Add part quality to the array for secondary validation
                quality[parts][step_number] = part_quality
                row = []
                row.extend([''] * total_number_of_steps)
                quality = numpy.vstack([quality, row])
                break
        step_number += 1

    step_number = 0
    parts += 1

print(time_stamp)
print(quality)
print("Parts", parts)
wrong_validation = calculate_incorrect_validation(parts)
print("Incorrect Validation:", wrong_validation)
print("Count quality", count_quality())
print("Good: ", good, "Pri_Good: ", pri_good_status, "Poor: ", poor, "Pri_Poor", pri_poor_status)
waste = [(pri_good_status + pri_poor_status) - (total_number_of_steps * 5)] + [wrong_validation]
print("Waste", waste)
print("Rework: ", re_no)
