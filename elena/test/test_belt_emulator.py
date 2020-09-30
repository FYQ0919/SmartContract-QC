from elena.emulators.belt_emulator import Transporter
from elena.emulators.workpiece_emulator import Workpiece
import unittest


class TesterTransportation(unittest.TestCase):
    def setUp(self):
        self.t1 = Transporter()
        self.w1 = Workpiece()

    def test_transport_workcell(self):
        r1, r2 = self.t1.estimate_travel_distance(self.w1, 6)
        r3 = self.w1.location = 6
        a1 = 8
        a2 = 2
        a3 = 6
        self.assertEqual(a1, r1)
        self.assertEqual(a2, r2)
        self.assertEqual(a3, r3)


if __name__ == '__main__':
    unittest.main()
