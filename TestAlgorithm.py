import unittest
import pandas as pd
from main import forward_algorithm


class TestForward(unittest.TestCase):

    def test_forward_algorithm(self):
        trans_p = {'S0': {"S0": 0, "H": 0, "L": 0}, 'H': {"S0": 0.5, "H": 0.5, "L": 0.4},
                   'L': {"S0": 0.5, "H": 0.5, "L": 0.6}}
        transitions = pd.DataFrame(trans_p)
        emit_p = dict(A={"H": 0.2, "L": 0.3}, C={"H": 0.3, "L": 0.2}, T={"H": 0.2, "L": 0.3}, G={"H": 0.3, "L": 0.2})
        emissions = pd.DataFrame(emit_p)
        sequence = list('GGCA')
        forward = forward_algorithm(transitions=transitions, emissions=emissions, chain=sequence)
        forward = round(forward, 7)
        self.assertEqual(forward, 0.0038432, "Not equal")


if __name__ == '__main__':
    unittest.main()
