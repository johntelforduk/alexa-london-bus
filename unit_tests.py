# Run a set of unit tests.

import bus_stop
import unittest                                 # These tests based on, https://docs.python.org/3/library/unittest.html


class TestBusStop(unittest.TestCase):

    def test_bus_arrivals(self):
        ba = bus_stop.bus_arrivals('490005183E')                                # Some test naptan ID.

        self.assertNotEqual(ba, None)

        if len(ba) != 0:                                                        # Empty list is OK.
            (_, exp_arrival_mins, bus_stop_name, bus_number, towards) = ba[0]   # Get 1st tuple from list.
            self.assertGreaterEqual(exp_arrival_mins, 0)
            self.assertEqual(bus_stop_name, 'Balgonie Road')                    # The test naptan ID has this name.

    def test_due_mins_to_words(self):
        self.assertEqual(bus_stop.due_mins_to_words(0), 'now')
        self.assertEqual(bus_stop.due_mins_to_words(1), 'in 1 minute')
        self.assertEqual(bus_stop.due_mins_to_words(12), 'in 12 minutes')

    def test_mins_to_words(self):
        self.assertEqual(bus_stop.mins_to_words(0), 'zero minutes')
        self.assertEqual(bus_stop.mins_to_words(1), '1 minute')
        self.assertEqual(bus_stop.mins_to_words(12), '12 minutes')

    def test_buses_to_speech(self):

        # TFL API failed.
        test_q1 = None
        test_a1 = '<speak>Sorry, but I could not get information from <say-as interpret-as="spell-out">TFL</say-as></speak>.'

        # TFL API succeeded, but there are no buses expected at the moment.
        test_q2 = []
        test_a2 = '<speak>There are no buses at the moment.</speak>'

        # 1 bus expected.
        test_q3 = [(226, 3, 'Balgonie Road', '397', 'Chingford')]
        test_a3 = '<speak>The next bus from Balgonie Road is the <say-as interpret-as="digits">397</say-as> towards Chingford due in 3 minutes. There are no more buses expected after that.</speak>'

        # 2 buses expected.
        test_q4 = [(226, 3, 'Balgonie Road', '397', 'Chingford'), (948, 15, 'Balgonie Road', '397', 'Chingford')]
        test_a4 = '<speak>The next bus from Balgonie Road is the <say-as interpret-as="digits">397</say-as> towards Chingford due in 3 minutes. Followed by a bus in 15 minutes from now.</speak>'

        # 3 buses expected.
        test_q5 = [(226, 3, 'Balgonie Road', '397', 'Chingford'), (948, 15, 'Balgonie Road', '397', 'Chingford'), (1205, 20, 'Balgonie Road', '397', 'Chingford')]
        test_a5 = '<speak>The next bus from Balgonie Road is the <say-as interpret-as="digits">397</say-as> towards Chingford due in 3 minutes. And then buses in 15 minutes, and 20 minutes from now.</speak>'

        # 4 buses expected.
        test_q5 = [(226, 3, 'Balgonie Road', '397', 'Chingford'), (948, 15, 'Balgonie Road', '397', 'Chingford'), (1205, 20, 'Balgonie Road', '397', 'Chingford'), (1805, 30, 'Balgonie Road', '397', 'Chingford')]
        test_a5 = '<speak>The next bus from Balgonie Road is the <say-as interpret-as="digits">397</say-as> towards Chingford due in 3 minutes. And then buses in 15 minutes, 20 minutes, and 30 minutes from now.</speak>'

        self.assertEqual(bus_stop.buses_to_speech(test_q1), test_a1)
        self.assertEqual(bus_stop.buses_to_speech(test_q2), test_a2)
        self.assertEqual(bus_stop.buses_to_speech(test_q3), test_a3)
        self.assertEqual(bus_stop.buses_to_speech(test_q4), test_a4)
        self.assertEqual(bus_stop.buses_to_speech(test_q5), test_a5)


if __name__ == '__main__':
    unittest.main()
