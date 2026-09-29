import copy
import unittest

from metro_planner.graph import (get_stations, is_connected,
                                 normalize_station, validate_network)
from metro_planner.metro_data import METRO


class TestNetworkValidation(unittest.TestCase):
    def test_real_network_is_valid(self):
        self.assertTrue(validate_network(METRO))

    def test_real_network_is_connected(self):
        self.assertTrue(is_connected(METRO))

    def test_unknown_neighbour_rejected(self):
        bad = copy.deepcopy(METRO)
        bad["Saket"]["Nowhere"] = 1
        with self.assertRaises(ValueError):
            validate_network(bad)

    def test_asymmetric_edge_rejected(self):
        bad = copy.deepcopy(METRO)
        bad["Saket"]["Qutub Minar"] = 99
        with self.assertRaises(ValueError):
            validate_network(bad)

    def test_non_positive_distance_rejected(self):
        bad = {"A": {"B": 0}, "B": {"A": 0}}
        with self.assertRaises(ValueError):
            validate_network(bad)

    def test_disconnected_network_detected(self):
        split = {"A": {"B": 1}, "B": {"A": 1}, "C": {}}
        self.assertFalse(is_connected(split))


class TestStationHelpers(unittest.TestCase):
    def test_normalize_ignores_case_and_spaces(self):
        self.assertEqual(normalize_station("  rajiv   CHOWK ", METRO), "Rajiv Chowk")

    def test_normalize_unknown_returns_none(self):
        self.assertIsNone(normalize_station("Atlantis", METRO))

    def test_get_stations_sorted(self):
        names = get_stations(METRO)
        self.assertEqual(names, sorted(names))
        self.assertEqual(len(names), len(METRO))


if __name__ == "__main__":
    unittest.main()
