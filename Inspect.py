from elena.emulators.network_emulator import app, add_routes
from elena.emulators.workcell_emulator import Workcell
from elena.emulators.workpiece_emulator import Workpiece
from elena.emulators.belt_emulator import Transporter
from elena.utils import csv_functions

from ast import literal_eval
from datetime import datetime
from threading import Thread
import json
import os
import requests
import time
import pandas as pd

class QC_simulation:
    def __init__(self,headers = {'Content-Type': "application/json",},consensus_mode = "majority",score_type = "majority",learning = True,threshold = 5,input_num = 1,
                                       total_products = 5, total_workcells = 17,ip = '127.0.0.1'):

       self.headers = headers
       self.consensus_mode = consensus_mode
       self.score_type = score_type
       self.learning = True
       self.threshold = threshold
       self.input_num = input_num
       self.total_products = total_products
       self.total_workcells = total_workcells
       self.ip = ip
       self.input_filename = f"input_{input_num}"
       dt = datetime.now().strftime('%Y%m%d_%H%M%S')
       self.folder = f"data/raw/{self.input_filename}/independent_qc/{self.score_type}/{self.total_products}_workpiece/{dt}"

       if self.consensus_mode == "majority":
           self.port = 4000 + self.input_num * 10 + self.threshold
           self.score_list = [1] * self.total_workcells  # initial score
       else:  # consensus_mode == "confidence"
           self.port = 5000 + self.input_num + int(str(self.threshold)[len("0."):])
           # Get score list
           if self.learning:
               self.score_list = [0.1] * self.total_workcells  # initial score
           else:
               self.trained_folder = f'input_{self.total_products}_workpiece/trained/'
               self.trained_workpiece = 20
               self.trained_filename = f'independent_qc_training_{self.trained_workpiece}_workpiece_{self.selfinput_filename}.xlsx'
               self.trained_df = pd.read_excel(f'{self.trained_folder}/{self.trained_filename}')
               self.score_list = [self.trained_df[f"wc_{i + 1}_score"].iloc[-1] for i in range(total_workcells)]  # todo

       if not os.path.exists(self.folder):
           os.makedirs(self.folder)  # Create target Directory
           print("Directory ", self.folder, " Created ")
       else:
           print("Directory ", self.folder, " already exists")
       self.time_interval = 1
       self.input_worksheet = csv_functions.read_csv(f'input_{self.total_products}_workpiece/{self.input_filename}.csv')
       if self.total_products != len(set(self.input_worksheet.workpiece_id.to_list())):  # check before proceed
           raise KeyError(f"Number of workpieces is not {self.total_products}")


    def instantiate_objects(self,threshold, consensus_mode, score_list, learning):
        # Instantiate objects
        print("Instantiating objects...")
        # Instantiate objects
        quality_controllers = {
          f"wc_{i + 1}": Workcell(
            step_idx=i + 1,
            id=f"wc_{i + 1}",
            ip=self.ip,
            port=self.port,
            qc_id=f"wc_{i + 1}",
            consensus_mode=consensus_mode,
            threshold=threshold,
            score=1,
            learning=False
         )
         for i in range(self.total_workcells)
        }

        workpieces = {
          f"wp_{i+1}": Workpiece(id=f"wp_{i+1}")
          for i in range(self.total_products)
        }
        transporter = Transporter()
        print("Objects instantiated...")
        return quality_controllers, workpieces, transporter

    def simulate(self,quality_controllers, workpieces, transporter):
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
            res = requests.post(f"{qc_inst.address}/blockchain/registration", data=json.dumps(payload), headers=self.headers)
            if res.status_code == 200:
                print(f"Nodes registered at {qc_id}.")
            else:
                raise ConnectionError(f"Node {qc_id} refuse to register nodes.")

        # Each workpiece
        for wp_id, wp_inst in workpieces.items():
            print(f"For workpiece {wp_id},")
            workpiece_df = self.input_worksheet.loc[self.input_worksheet['workpiece_id'] == wp_id]  # Rows of that wp id

            # Initialize data logging for each workpiece
            data = {
                "production_index": [],
                "step_idx": [],
                "production_workcell": [],
                "qc": [],
                "consent": [],
                "winner_qc_list": [],
                "score": [],
                "production_time": [],
                "transport_time": [],
                "inspection_time": [],
                "network_time": [],
                "qc_results": [],
                "actual_quality": [],
            }
            df = csv_functions.create_df(data)
            filename = f"{self.folder}/{wp_id}_qc_{self.score_type}_{self.threshold}.csv"

            # Each production step
            for row in workpiece_df.itertuples():  # workpiece_df haven't reached last production step
                print(f"    Row {row.Index}: at step {row.step_idx}")
                data = dict()  # Reset
                transport_time = list()  # Reset
                wc_time = list()
                bc_time = list()  # Reset
                qc_time = list()  # Reset
                score_list = list()  # Reset
                error_list = list()  # Reset
                in_winner_counter_list = list()  # Reset
                in_qc_counter_list = list()  # Reset
                qc_list = list()  # Reset
                capability_list = list()  # Reset
                winner_qc_list = list()  # Reset
                winner_score_list = list()  # Reset
                winner_results_list = list()  # Reset
                consent_list = list()  # Reset
                consent = False  # Reset
                # Extract actual quality
                actual_quality_dict = literal_eval(row.actual_quality)
                actual_quality = max(actual_quality_dict, key=actual_quality_dict.get)  # Key with max value in dict
                execution_info = {
                    "production_time": row.production_time,
                    "produced_by": row.workcell_id,
                    "min_qc_required": len(actual_quality_dict) + 1
                }
                # Log production information
                data["production_index"] = row.Index
                data["step_idx"] = row.step_idx
                data["production_workcell"] = row.workcell_id
                data["actual_quality"] = actual_quality
                # Do quality control
                while not consent:  # Until consent is achieved for each production step
                    production_time = None  # Place holder
                    travel_time = None  # Place holder
                    network_time = None  # Place holder
                    inspection_time = None  # Place holder
                    qc_id = None  # Place holder
                    score = None  # Place holder
                    score_error = None  # Place holder
                    in_winner_counter = None  # Place holder
                    in_qc_counter = None  # Place holder
                    actual_capability = None  # Place holder
                    winner_dict = dict()  # Place holder

                    if wp_inst.sink is not None and wp_inst.source is not None:  # Workpiece needs transportation
                        print(f"        Travelling from {wp_inst.source} to {wp_inst.sink}...")
                        # Start travel
                        if wp_inst.location is not None:  # Move workpiece out of location
                            travel_time, travel_dist, splitter = transporter.start_travel(wp_inst)
                        # In travel
                        else:
                            if transporter.in_travel(wp_inst, self.time_interval):  # still can count down with time_interval
                                continue
                            else:  # End travel
                                transporter.end_travel(wp_inst)

                    if wp_inst.sink is None and wp_inst.source is None:  # Workpiece does not need transportation
                        # Get next production step
                        if wp_inst.status == "awaiting next step":  # todo: change to "awaiting next step"
                            wc_inst = quality_controllers[row.workcell_id]
                            wp_inst.step_idx = row.step_idx
                            wp_inst.source = wp_inst.location
                            wp_inst.sink = row.workcell_id
                            wp_inst.status = "awaiting production"
                            wc_inst.production_workpiece = wp_id
                        elif wp_inst.status == "awaiting production":
                            # Start production
                            print(f"        Production.")
                            current_wc_inst = quality_controllers[row.workcell_id]
                            current_wc_inst.production_workpiece = wp_inst
                            # Assume done production
                            wp_inst.status = "awaiting inspection"
                            current_wc_inst.pass_to_quality_controller(execution_info)
                            production_time = row.production_time
                        elif wp_inst.status == "awaiting inspection":  # Awaiting inspection
                            # Start inspection
                            qc_id = wp_inst.location
                            qc_inst = quality_controllers[qc_id]
                            qc_inst.add_to_inspection(wp_inst)
                            qc_inst.start_inspection(row.step_idx, inspection_time=getattr(row, f"qc_{qc_id}_time"))
                            print(f"        Inspection time will end {getattr(row, f'qc_{qc_id}_time')} later.")
                            continue  # Don't log info
                        elif wp_inst.status == "in inspection":  # Still in inspection
                            qc_id = wp_inst.location
                            qc_inst = quality_controllers[qc_id]
                            if qc_inst.in_inspection(self.time_interval):  # Still can count down with time_interval
                                continue
                            else:  # Count down is negative, need to stop inspection
                                # End inspection
                                inspection_results = literal_eval(getattr(row, f"qc_{qc_id}_results"))
                                inspection_time, network_time, consent, winner_dict = \
                                    qc_inst.end_inspection(
                                        inspection_results=inspection_results,
                                        execution_info=execution_info
                                    )
                                # Prepare qc data (no consent)
                                score = qc_inst.score
                                score_error = qc_inst.get_score_error()
                                in_winner_counter = qc_inst.in_winner_counter
                                in_qc_counter = qc_inst.in_qc_counter
                                actual_capability = getattr(row, f"qc_{qc_id}_confidence")
                                if consent:
                                    print(f"        Production time: {wc_time}")
                                    print(f"        Transport time: {transport_time}")
                                    print(f"        Network time: {bc_time}")
                                    print(f"        Inspection time: {qc_time}")
                                    print(f"        Sequence of qc: {winner_dict['qc_list']}")
                                    print(f"        Winners: {winner_dict['winner_qc_list']}")
                                    print(f"        Score: {winner_dict['score']}")
                                    print(f"        Results: {winner_dict['results']}")
                                    # Log qc data (no consent)
                                    data["qc_score"] = score_list
                                    data["score_error"] = error_list
                                    data["in_winner_counter"] = in_winner_counter_list
                                    data["in_qc_counter"] = in_qc_counter_list
                                    data["qc_capability"] = capability_list
                                    # Log qc data (consent)
                                    data["production_time"] = wc_time
                                    data["transport_time"] = transport_time
                                    data["network_time"] = bc_time
                                    data["inspection_time"] = qc_time
                                    data["qc"] = qc_list
                                    data["consent"] = consent_list
                                    data["winner_qc_list"] = winner_qc_list
                                    data["score"] = winner_score_list
                                    data["qc_results"] = winner_results_list

                    # Append each qc data into respective list
                    transport_time.append(travel_time)
                    wc_time.append(production_time)
                    bc_time.append(network_time)
                    qc_time.append(inspection_time)
                    score_list.append(score)
                    error_list.append(score_error)
                    in_winner_counter_list.append(in_winner_counter)
                    in_qc_counter_list.append(in_qc_counter)
                    capability_list.append(actual_capability)
                    qc_list.append(qc_id)
                    winner_qc_list.append(winner_dict.get("winner_qc_list", None))
                    winner_score_list.append(winner_dict.get("score", None))
                    winner_results_list.append(winner_dict.get("results", None))
                    consent_list.append(consent)
                    time.sleep(.1)
                # Consent achieved for that row
                # Append log data to dataframe
                df = csv_functions.append_to_df(df, data)
                # print(df)
            # Write dataframe into csv
            csv_functions.write_csv(filename, df)
        print("====================================== PROGRAM END ======================================")


if __name__ == '__main__':
    QC = QC_simulation()

    qc, wp, trans = QC.instantiate_objects(threshold = 5, consensus_mode = "majority" , score_list ="majority", learning =True)
    add_routes(qc, threshold = 5)
    t = Thread(
        target=QC.simulate,
        args=(qc, wp, trans, )
    )
    t.start()
    app.run(host='0.0.0.0',port=QC.port)