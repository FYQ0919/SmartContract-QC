from elena.emulators.network_emulator import app, add_routes
from elena.emulators.workcell_emulator import Workcell
from elena.emulators.workpiece_emulator import Workpiece
from elena.emulators.belt_emulator import Transporter
from elena.emulators.process_controller_emulator import ProcessController
from elena.utils import csv_functions

from datetime import datetime
from threading import Thread
import json
import os
import time
import requests


headers = {
    'Content-Type': "application/json",
}


# Input variables
threshold = 0.9
learning = False
input_num = 1   # Input set
port = 5000 + input_num + int(str(threshold)[len("0."):])
ip = '127.0.0.1'
# These lists are from excel sheets (lazy to code read excel...)
capability_list = [1., .3, .9, .3, .7, 1., .2, .4, .3, .1, .7, .5, 1., .7, .7, .5, .9]  # sim 2 input 1
# capability_list = [.8, .7, .9, .9, .8, .5, .5, .9, .7, .8, 1., 1., .7, 1., .7, .5, .8]  # sim 2 input 2
# capability_list = [.1, .8, .9, .7, .4, .9, .6, .6, .4, 1., .8, .3, .3, .5, .2, .8, .4]  # sim 2 input 4
# capability_list = [.4, .8, .3, .4, .8, .2, .9, .3, 1., .8, .2, .7, 1., .6, 1., .9, .6]  # sim 2 input 5
# capability_list = [.1, .5, .3, .7, 1., .5, .6, .8, .6, .4, .2, .4, .5, .1, .1, .6, 1.]  # sim 2 input 6
# capability_list = [.5, .2, .4, .6, .2, .4, .3, .2, 1, .5, .6, .6, .8, 1, .6, .8, .5]  # sim 2 input 8
# capability_list = [.6, .5, .1, .6, .2, .5, .2, 1, .6, .7, .7, .6, .1, .9, .8, 1, .1]  # sim 2 input 9
# capability_list = [1., .5, 1., .5, .2, .8, .3, 1, .6, .9, .3, .2, .7, .7, .2, .9, .6]  # sim 2 input 10
# capability_list = [.4, .9, .7, .8, .7, .3, .2, .7, .1, .1, .1, .6, .6, .4, .1, .3, .8]  # sim 2 input 11
# capability_list = [.4, 1., .9, .9, .2, .5, .3, .6, .9, .7, .1, .3, .8, .2, .1, .8, .8]  # sim 2 input 12
# capability_list = [.4, 1., .2, .1, .5, .1, .6, .9, .5, 1., .8, .9, .8, .9, .5, .3, .5]  # sim 2 input 13
# capability_list = [.1, 1., .2, .5, .3, .5, .9, 1., .6, .6, .2, .1, .1, .5, .4, .2, .1]  # sim 2 input 14
# capability_list = [1., .8, .5, .2, .6, 1., .1, .6, .2, 1., .8, .5, .3, .2, 1., .8, .5]  # sim 2 input 15
# capability_list = [.7, .3, .2, .5, .5, .7, .6, .3, .8, 1., .3, .1, .2, .2, .2, .1, .9]  # sim 2 input 16
# capability_list = [.7, .8, .4, .1, .1, 1., 1., .1, .6, .3, .8, .9, .8, .2, .9, .8, .6]  # sim 2 input 17
# capability_list = [.7, .1, .1, .7, .8, .2, .9, .3, .1, .8, 1., 1., .1, .5, .5, .6, .6]  # sim 2 input 18
# capability_list = [.1, .9, .6, .4, .1, .3, .9, .6, .7, 1., .1, .1, .1, 1., .4, .1, .7]  # sim 2 input 20
score_list = [.81, .44, .84, .49, .78, .99, .35, .48, .37, .10, .65, .74, .75, .84, .84, .44, .74]  # sim 2 input 1
# score_list = [0.95,0.76,0.93,0.99,0.58,0.54,0.66,0.78,0.65,0.7,0.78,0.82,0.77,0.93,0.8,0.6,0.87]  # sim 2 input 2
# score_list = [0.24,0.87,0.83,0.82,0.57,0.87,0.65,0.58,0.41,0.86,0.76,0.5,0.39,0.66,0.16,0.93,0.48]  # sim 2 input 4
# score_list = [0.53,0.7,0.39,0.48,0.77,0.3,0.85,0.34,0.84,0.79,0.29,0.93,0.97,0.48,0.72,0.83,0.69]  # sim 2 input 5
# score_list = [0.13,0.62,0.35,0.82,0.99,0.71,0.72,0.78,0.67,0.47,0.34,0.56,0.81,0.16,0.3,0.83,0.81]  # sim 2 input 6
# score_list = [0.6,0.23,0.52,0.67,0.3,0.48,0.37,0.16,0.99,0.83,0.69,0.64,0.77,0.94,0.71,0.85,0.77]  # sim 2 input 8
# score_list = [0.86,0.59,0.11,0.63,0.4,0.62,0.3,0.81,0.69,0.8,0.82,0.72,0.29,0.99,0.97,0.87,0.41]  # sim 2 input 9
# score_list = [0.84,0.66,0.84,0.53,0.23,0.89,0.42,0.87,0.61,0.83,0.3,0.35,0.81,0.7,0.23,0.84,0.74]  # sim 2 input 10
# score_list = [0.68,0.87,0.86,0.85,0.69,0.38,0.39,0.82,0.31,0.21,0.23,0.88,0.69,0.46,0.3,0.38,0.9]  # sim 2 input 11
# score_list = [0.45,0.99,0.86,0.86,0.25,0.57,0.39,0.7,0.89,0.75,0.12,0.47,0.99,0.3,0.23,0.9,0.72]  # sim 2 input 12
# score_list = [0.4,0.98,0.29,0.45,0.67,0.17,0.58,0.83,0.49,0.92,0.79,0.89,0.78,0.74,0.62,0.42,0.66]  # sim 2 input 13
# score_list = [0.35,0.8,0.36,0.86,0.54,0.76,0.74,0.72,0.87,0.73,0.35,0.26,0.32,0.7,0.63,0.26,0.19]  # sim 2 input 14
# score_list = [0.97,0.9,0.58,0.38,0.72,0.99,0.1,0.6,0.32,0.8,0.86,0.64,0.44,0.34,0.84,0.76,0.71]  # sim 2 input 15
# score_list = [0.79,0.43,0.29,0.62,0.68,0.86,0.72,0.44,0.83,0.99,0.38,0.18,0.35,0.22,0.37,0.19,0.99]  # sim 2 input 16
# score_list = [0.78,0.76,0.41,0.24,0.24,0.79,0.98,0.15,0.59,0.32,0.92,0.99,0.82,0.27,0.92,0.84,0.63]  # sim 2 input 17
# score_list = [0.75,0.23,0.17,0.65,0.8,0.32,0.88,0.44,0.23,0.85,0.88,0.99,0.3,0.66,0.58,0.72,0.75]  # sim 2 input 18
# score_list = [0.18,0.87,0.54,0.5,0.18,0.39,0.99,0.65,0.63,0.86,0.11,0.21,0.13,0.95,0.5,0.39,0.88]  # sim 2 input 20
worksheet = csv_functions.read_csv('Data_Sheet.csv')
total_workcells = 17
total_products = 3
time_interval = 1
output_folder = f"data/simulation_4_input_{input_num}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)    # Create target Directory
    print("Directory ", output_folder,  " Created ")
else:
    print("Directory ", output_folder,  " already exists")
dt = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f"{output_folder}/{dt}_workpiece_{total_products}_input_{input_num}.csv"


def instantiate_objects(threshold, score_list, learning):
    # Instantiate objects
    print("Instantiating objects...")
    workcells = {
        f"wc_{i+1}": Workcell(
            step_idx=i+1,
            id=f"wc_{i+1}",
            ip=ip,
            port=port,
            qc_id=f"wc_{i + 1}",
            consensus_mode="confidence",
            threshold=threshold,
            score=score_list[i],
            capability=capability_list[i],
            learning=learning
        )
        for i in range(total_workcells)
    }
    workpieces = {
        f"wp_{i+1}": Workpiece(id=f"wp_{i+1}")
        for i in range(total_products)
    }
    process_controllers = {  # each workpiece has one process controller
        f"wp_{i+1}": ProcessController(workpiece_id=f"wc_{i+1}")    # same name as workpiece
        for i in range(total_products)
    }
    transporter = Transporter()
    print("Objects instantiated...")
    return workcells, workpieces, transporter, process_controllers


def simulate(workcells, workpieces, transporter, process_controllers, ):
    quality_controllers = workcells

    # Register qc as nodes
    print("Registering nodes...")
    payload = {
        "nodes": {
            qc_id: {
                "address": qc_inst.address
            }
            for qc_id, qc_inst in quality_controllers.items()
        }
    }
    for qc_id, qc_inst in quality_controllers.items():
        res = requests.post(f"{qc_inst.address}/blockchain/registration", data=json.dumps(payload), headers=headers)
        if res.status_code == 200:
            print(f"Nodes registered at {qc_id}.")
        else:
            raise ConnectionError(f"Node {qc_id} refuse to register nodes.")

    # Initialize data logging
    data = {
        "time_step": [],
        "workpiece_id": [],
        "step_idx": [],
        "production_workcell": [],
        "actual_quality": [],
        "state": [],
        "qc": [],
        "consent": [],
        "winner_qc_list": [],
        "score": [],
        "qc_results": [],
        "production_time": [],
        "transport_time": [],
        "inspection_time": [],
        "network_time": [],
    }
    df = csv_functions.create_df(data)

    # Initialize time step for while loop
    time_step = 0
    consent = False
    while True:
        print(f"At {time_step},")
        for wp_id, wp_inst in workpieces.items():
            print(f"    Workpiece {wp_id}: {wp_inst.status}, at: {wp_inst.location}, count down: {wp_inst.count_down}")

            # Reset dict for dataframe
            data = dict()  # Reset
            execution_info = dict()  # Place holder

            # Log general data
            data["workpiece_id"] = [wp_id]
            data["step_idx"] = [wp_inst.step_idx]

            if wp_inst.sink is not None and wp_inst.source is not None:   # Workpiece needs transportation
                print(f"        Travelling from {wp_inst.source} to {wp_inst.sink}...")
                # Start travel
                if wp_inst.location is not None:    # Move workpiece out of location
                    travel_time, travel_dist, splitter = transporter.start_travel(wp_inst)
                    # Log transport data
                    data["time_step"] = [time_step]
                    data["transport_time"] = [travel_time]
                # In travel
                else:
                    if transporter.in_travel(wp_inst, time_interval):    # still can count down with time_interval
                        continue
                    else:   # End travel
                        transporter.end_travel(wp_inst)

            if wp_inst.sink is None and wp_inst.source is None:  # Workpiece does not need transportation
                # Workpiece completed, no actions needed
                if wp_inst.status == "completed":  # if completed
                    continue
                # Get next production step
                elif wp_inst.status == "awaiting next step":     # todo: change to "awaiting next step"
                    pc = process_controllers[wp_id]      # Get next step
                    _, step_idx, sink_id = pc.get_next_step_idx(
                        wp_inst,
                        workcells
                    )  # based on wp pre-conditions and wc state
                    pc.update_workpiece_completion(wp_inst)
                    print(f"        Next step from process controller is {step_idx}...")
                # Start production
                elif wp_inst.status == "awaiting production":
                    # Start production step
                    wc_inst = workcells[wp_inst.location]
                    wc_inst.add_to_production(wp_inst)
                    if wc_inst.inspection_workpiece is not None:
                        if not isinstance(wc_inst.inspection_workpiece, str):
                            if wc_inst.inspection_workpiece.status == "in inspection":  # Inspecting other workpieces
                                continue
                    wc_inst.start_production(worksheet_df=worksheet)
                    print(f"        Start production for step {wp_inst.step_idx}.")
                # Still in production
                elif wp_inst.status == "in production":
                    wc_id = wp_inst.location
                    wc_inst = workcells[wc_id]
                    if wc_inst.in_production(time_interval):  # positive count down
                        continue
                    else:  # negative count down
                        # End production step
                        production_time = wc_inst.production_time
                        execution_info, actual_quality = wc_inst.end_production(worksheet)
                        # Update workpiece status to process controller
                        max_probability = max(probability for state, probability in actual_quality.items())
                        state_list = [state for state, probability in actual_quality.items() if
                                      probability == max_probability]
                        pc = process_controllers[wp_id]
                        pc.update_step_status(wp_inst.step_idx, state_list)
                        if wp_inst.status != "in production":
                            # Log production data
                            data["time_step"] = [time_step - production_time]
                            data["production_workcell"] = [wc_id]
                            data["production_time"] = [production_time]
                            data["actual_quality"] = [actual_quality]
                            data["state"] = [str(state_list)]
                # Start inspection
                elif wp_inst.status == "awaiting inspection":  # Awaiting inspection
                    qc_id = wp_inst.location
                    qc_inst = quality_controllers[qc_id]
                    qc_inst.add_to_inspection(wp_inst)
                    if qc_inst.production_workpiece is not None:
                        if not isinstance(qc_inst.production_workpiece, str):
                            if qc_inst.production_workpiece.actual_quality is None:  # Producing other workpieces
                                continue
                    qc_inst.start_inspection(wp_inst.step_idx, worksheet_df=worksheet)
                    print(f"        Inspection time will end {qc_inst.inspection_time} later.")
                # Still in inspection
                elif wp_inst.status == "in inspection":
                    qc_id = wp_inst.location
                    qc_inst = quality_controllers[qc_id]
                    if qc_inst.in_inspection(time_interval):    # positive count down
                        continue
                    else:   # negative count down
                        # End inspection (Update consent)
                        execution_info["min_qc_required"] = len(wp_inst.actual_quality) + 1
                        inspection_time, network_time, consent, winner_dict = \
                            qc_inst.end_inspection(
                                execution_info=execution_info   # todo: find a way to pass this info
                            )
                        if wp_inst.status != "in inspection":
                            # Log qc data (no consent)
                            data["time_step"] = [time_step - inspection_time]
                            data["qc"] = [qc_id]
                            data["network_time"] = [network_time]
                            data["inspection_time"] = [inspection_time]
                            data["consent"] = [consent]
                            data["in_winner_counter"] = [qc_inst.in_winner_counter]
                            data["in_qc_counter"] = [qc_inst.in_qc_counter]
                            data["score_error"] = [qc_inst.get_score_error()]
                            data["qc_score"] = [qc_inst.score]
                            data["qc_capability"] = [qc_inst.capability]
                            # Log qc data (consent)
                            data["winner_qc_list"] = [winner_dict.get("winner_qc_list", None)]
                            data["score"] = [winner_dict.get("score", None)]
                            data["qc_results"] = [winner_dict.get("results", None)]
            # Append data to dataframe
            if data.get("time_step", None) is not None:
                df = csv_functions.append_to_df(df, data)
            if consent:
                # Write dataframe into csv
                csv_functions.write_csv(filename, df)

        # Add time interval
        time_step += time_interval
        # Termination condition
        if all(wp_inst.status == "completed" for wp_id, wp_inst in workpieces.items()):
            break

        time.sleep(.1)

    # Write dataframe into csv
    csv_functions.write_csv(filename, df)
    print("====================================== PROGRAM END ======================================")


if __name__ == '__main__':
    qc, wp, trans, pc = instantiate_objects(threshold, score_list, learning)
    add_routes(qc, threshold)
    t = Thread(
        target=simulate,
        args=(qc, wp, trans, pc, )
    )
    t.start()
    app.run(host='0.0.0.0', port=port)
