from elena.emulators.network_emulator import app, add_routes
from elena.emulators.workpiece_emulator import Workpiece
from elena.emulators.workcell_emulator import Workcell
from elena.emulators.quality_controller_emulator import QualityController

import json
import unittest

headers = {
    'Content-Type': "application/json",
}


class TesterQualityController(unittest.TestCase):
    def setUp(self):
        self.qc = QualityController(id="wc_1", ip="localhost", port=5000)

    def test_register_workpiece(self):
        self.qc.register_workpiece("wp")
        self.assertTrue(self.qc.blockchain_dict.get("wp"))

    def test_get_winner_by_majority(self):
        grouped_results = {
            "r1": [("qc1", 1), ("qc2", 1)],
            "r2": [("qc3", 1)],
        }
        r1 = self.qc.get_winner_by_majority(grouped_results)
        print(r1)
        self.assertEqual("r1", r1[0])
        self.assertEqual(2, r1[1])

    def test_get_winner_by_confidence(self):
        grouped_results = {
            "r1": [("qc1", 0.6), ("qc2", 0.6)],
            "r2": [("qc3", 0.3), ("qc4", 0.6)],
        }
        r1 = self.qc.get_winner_by_confidence(grouped_results)
        print(r1)
        self.assertEqual("r1", r1[0])
        self.assertEqual(0.84, r1[1])


class TesterBlockChain(unittest.TestCase):
    def setUp(self):
        self.qc = QualityController(id="wc_1", ip="localhost", port=5000)
        self.qc.register_workpiece("wp")

    def test_new_transaction(self):
        bc = self.qc.blockchain_dict["wp"]
        data = {
            "workpiece_id": "wp",
            "execution_info": None,
            "winner_qc_list": None,
            "qc_list": None,
            "results": None,
            "score": None
        }
        print(data.keys())
        r1 = bc.new_transaction(data)
        self.assertTrue(r1)


class TesterQualityControllerRoute(unittest.TestCase):
    def setUp(self):
        # app.config["TESTING"] = True
        self.app = app.test_client()
        total_workcells = 2
        print("Instantiating objects...")
        quality_controllers = {
            f"wc_{i + 1}": Workcell(step_idx=i + 1, id=f"wc_{i + 1}", ip="localhost", port=5000, qc_id=f"wc_{i + 1}")
            for i in range(total_workcells)
        }
        print("Completed instantiating objects")
        add_routes(quality_controllers, 3)
        self.qc = quality_controllers["wc_1"]
        self.qc2 = quality_controllers["wc_2"]
        self.qc.register_workpiece("wp")
        self.qc2.register_workpiece("wp")
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
            res = self.app.post(f"{qc_inst.address}/blockchain/registration", data=json.dumps(payload), headers=headers)
            if res.status_code == 200:
                print(f"Nodes registered at {qc_id}.")
            else:
                raise ConnectionError(f"Node {qc_id} refuse to register nodes.")
        print("SetUp complete")

    def test_inspection(self):
        payload = {
            "workpiece_id": "wp",
            "execution_info": None,
            "qc_list": None,
        }
        r1 = self.app.post(f"{self.qc.address}/inspection", data=json.dumps(payload), headers=headers)
        print(r1.data.decode())
        self.assertEqual(200, r1.status_code)
        self.assertEqual("wp", self.qc.inspection_workpiece)

    def test_results(self):
        self.qc.inspection_workpiece = Workpiece(id="wp")
        payload = {
            "wp": {
                "wc_1": {
                    "results": ["Pass"],
                    "score": 1
                }
            }
        }
        r1 = self.app.post(f"{self.qc.address}/inspection/results", data=json.dumps(payload), headers=headers)
        print(r1.data.decode())
        self.assertEqual(200, r1.status_code)   # todo: Error

    def test_assignment(self):
        self.assertEqual(None, self.qc.inspection_workpiece)
        payload = {
            "workpiece_id": "wp",
            "execution_info": None,
            "qc_list": None,
        }
        r1 = self.app.post(f"{self.qc.address}/inspection/assignment", data=json.dumps(payload), headers=headers)
        print(r1.data.decode())
        self.assertEqual(202, r1.status_code)
        self.assertEqual("wp", self.qc.inspection_workpiece)
        r1 = self.app.post(f"{self.qc.address}/inspection/assignment", data=json.dumps(payload), headers=headers)
        print(r1.data.decode())
        self.assertEqual(303, r1.status_code)

    def test_registration(self):
        payload = {
            "nodes": {
                "wc": {
                    "address": None
                }
            }
        }
        r1 = self.app.post(f"{self.qc.address}/blockchain/registration", data=json.dumps(payload), headers=headers)
        print(r1.data.decode())
        self.assertEqual(200, r1.status_code)

    def test_mine(self):
        self.assertTrue(self.qc.blockchain_dict.get("wp"))
        winner = {
            "results": 0,
            "winner_qc_list": None,
            "score": 0,
            "qc_list": None
        }
        payload = {
            "workpiece_id": "wp",
            "execution_info": None,
            "winner_qc_list": None,
            "qc_list": None,
        }
        self.qc.post_transaction("wp", winner, None)
        r1 = self.app.post(f"{self.qc.address}/blockchain/mine", data=json.dumps(payload), headers=headers)
        print(r1.data.decode())
        self.assertEqual(200, r1.status_code)

    def test_consensus_1(self):
        dct = {
            "wc_1": {"results": ["yes"], "score": 1},
            "wc_2": {"results": ["no"], "score": 1}
        }
        self.qc.inspection_results["wp"] = dct
        self.qc2.inspection_results["wp"] = dct
        payload = {
            "workpiece_id": "wp",
            "execution_info": {},
            "winner_qc_list": [],
            "qc_list": [],
            "results": None,
            "score": None,
            "miner": "wc_3"
        }
        payload["chain"] = "Invalid chain"
        r1 = self.app.post(f"{self.qc.address}/blockchain/consensus", data=json.dumps(payload), headers=headers)
        print(r1.data.decode())
        self.assertEqual(406, r1.status_code)

    def test_consensus_2(self):
        payload = {
            "workpiece_id": "wp",
            "execution_info": {},
            "winner_qc_list": [],
            "qc_list": [],
            "results": None,
            "score": None,
            "miner": "wc_2"
        }
        block1 = {
            "head": {
                "previous_hash": 1,
            }
        }
        block2 = {
            "head": {
                "previous_hash": self.qc.blockchain_dict["wp"].hash(block1),
            }
        }
        payload["chain"] = [
            block1,
            block2,
        ]
        r1 = self.app.post(f"{self.qc.address}/blockchain/consensus", data=json.dumps(payload), headers=headers)
        print(r1.data.decode())
        self.assertEqual(202, r1.status_code)
        self.assertEqual(payload["chain"], self.qc.blockchain_dict["wp"].chain)


if __name__ == '__main__':
    unittest.main()
