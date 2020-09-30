from elena.emulators.workcell_emulator import Workcell
from elena.emulators.workpiece_emulator import Workpiece

import unittest
import pandas as pd
import requests
import json


class TesterWorkcell(unittest.TestCase):
    def setUp(self):
        self.step = 1
        self.wc1 = Workcell(step_idx=self.step, id=1)

    def test_start_production(self):
        wp1 = Workpiece(id=1)
        data = {
            "Step": [self.step],
            "Production_Time_Min": [20],
            "Production_Time_Max": [80]
        }
        df = pd.DataFrame(data)
        self.wc1.add_to_production(wp1)
        self.wc1.start_production(worksheet_df=df)
        r1 = wp1.status
        a1 = "in production"
        self.assertEqual(a1, r1)

    def test_render_actual_quality(self):
        data = {
            "Step": [1, 1, 1, 2],
            "Possible_State": ["Pass", "Fail", "Nope", "Nope"]
        }
        worksheet = pd.DataFrame(data)
        r1 = self.wc1.render_actual_quality(worksheet)
        print(r1)
        r2 = sum([val for key, val in r1.items()])
        a2 = 100
        self.assertEqual(a2, r2)

    def test_assigned_inspection(self):
        import ast
        payload = {
            "qc_list": ["node1", "node2"],
            "workpiece_id": "wp_id",
            "execution_info": {"production_time": 1}
        }
        headers = {
            'Content-Type': "application/json",
        }
        r1 = requests.post('http://localhost:5000/wc_1/inspection/assignment', data=json.dumps(payload), headers=headers)
        print(r1.text)
        self.assertIsInstance(r1.text, str)
        r2 = ast.literal_eval(r1.text)
        self.assertIsInstance(r2, dict)


if __name__ == '__main__':
    unittest.main()
