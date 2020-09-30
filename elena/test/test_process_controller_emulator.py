from elena.emulators.process_controller_emulator import ProcessController
from elena.emulators.workcell_emulator import Workcell
import unittest


class TesterTransportation(unittest.TestCase):
    def setUp(self):
        self.p1 = ProcessController(1)

    def test_get_next_step(self):
        workcells = {
            f"wc_{i + 1}": Workcell(step_idx=i + 1, id=f"wc_{i + 1}")
            for i in range(5)
        }
        self.p1.step_idx_status[1] = True
        r1, r2, r3 = self.p1.get_next_step_idx(workcells)
        a1 = [2, 3, 4]
        print(r2)
        print(r3)
        self.assertEqual(a1, r1)


if __name__ == '__main__':
    unittest.main()
