import unittest

from metro_planner.calculator import (build_journey, calculate_distance,
                                      calculate_fare, calculate_time)
from metro_planner.metro_data import METRO


class TestDistance(unittest.TestCase):
    def test_sum_of_edges(self):
        route = ["Rajiv Chowk", "Central Secretariat", "Hauz Khas"]
        self.assertEqual(calculate_distance(route, METRO), 8)

    def test_single_station_is_zero(self):
        self.assertEqual(calculate_distance(["Saket"], METRO), 0)

    def test_non_adjacent_stations_raise(self):
        with self.assertRaises(ValueError):
            calculate_distance(["Rajiv Chowk", "Saket"], METRO)


class TestTime(unittest.TestCase):
    def test_30km_takes_60_minutes(self):
        self.assertEqual(calculate_time(30), 60)

    def test_rounding(self):
        self.assertEqual(calculate_time(5), 10.0)
        self.assertEqual(calculate_time(1), 2.0)

    def test_negative_distance(self):
        with self.assertRaises(ValueError):
            calculate_time(-1)

    def test_bad_speed(self):
        with self.assertRaises(ValueError):
            calculate_time(5, speed=0)


class TestFare(unittest.TestCase):
    def test_slab_boundaries(self):
        cases = {0: 10, 2: 10, 3: 20, 5: 20, 6: 30, 10: 30,
                 11: 40, 15: 40, 16: 50, 100: 50}
        for distance, fare in cases.items():
            with self.subTest(distance=distance):
                self.assertEqual(calculate_fare(distance), fare)

    def test_negative_distance(self):
        with self.assertRaises(ValueError):
            calculate_fare(-3)


class TestBuildJourney(unittest.TestCase):
    def test_metrics(self):
        route = ["Rajiv Chowk", "Central Secretariat", "Hauz Khas",
                 "Saket", "Qutub Minar"]
        journey = build_journey(route, METRO)
        self.assertEqual(journey.distance, 15)
        self.assertEqual(journey.time_minutes, 30.0)
        self.assertEqual(journey.fare, 40)
        self.assertEqual(journey.stops, 4)


if __name__ == "__main__":
    unittest.main()
