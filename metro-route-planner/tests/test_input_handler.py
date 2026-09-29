import unittest

from metro_planner.config import CRITERION_DISTANCE, CRITERION_STOPS
from metro_planner.input_handler import (ask_yes_no, read_closed_stations,
                                         read_criterion, read_station)
from metro_planner.metro_data import METRO


def scripted(*answers):
    """Return an input() replacement that yields the given answers."""
    it = iter(answers)
    return lambda prompt="": next(it)


class Sink:
    def __init__(self):
        self.lines = []

    def __call__(self, text=""):
        self.lines.append(text)


class TestReadStation(unittest.TestCase):
    def test_accepts_valid_station_any_case(self):
        out = Sink()
        self.assertEqual(read_station("?", METRO, scripted("saket"), out), "Saket")
        self.assertEqual(out.lines, [])

    def test_reprompts_on_invalid(self):
        out = Sink()
        result = read_station("?", METRO, scripted("nope", "", "Saket"), out)
        self.assertEqual(result, "Saket")
        self.assertEqual(len(out.lines), 2)

    def test_exclude_rejects_same_station(self):
        out = Sink()
        result = read_station("?", METRO, scripted("Saket", "Hauz Khas"),
                              out, exclude="Saket")
        self.assertEqual(result, "Hauz Khas")


class TestYesNo(unittest.TestCase):
    def test_yes_variants(self):
        for word in ("yes", "YES", " y "):
            self.assertTrue(ask_yes_no("?", scripted(word), Sink()))

    def test_no_variants(self):
        for word in ("no", "N"):
            self.assertFalse(ask_yes_no("?", scripted(word), Sink()))

    def test_invalid_then_valid(self):
        out = Sink()
        self.assertTrue(ask_yes_no("?", scripted("maybe", "yes"), out))
        self.assertEqual(len(out.lines), 1)


class TestCriterion(unittest.TestCase):
    def test_default_and_options(self):
        self.assertEqual(read_criterion(scripted(""), Sink()), CRITERION_DISTANCE)
        self.assertEqual(read_criterion(scripted("1"), Sink()), CRITERION_DISTANCE)
        self.assertEqual(read_criterion(scripted("2"), Sink()), CRITERION_STOPS)

    def test_invalid_then_valid(self):
        self.assertEqual(read_criterion(scripted("9", "2"), Sink()), CRITERION_STOPS)


class TestClosedStations(unittest.TestCase):
    def test_multiple_stations(self):
        result = read_closed_stations(
            METRO, "Rajiv Chowk", "Saket",
            scripted("hauz khas, Mandi House"), Sink())
        self.assertEqual(result, {"Hauz Khas", "Mandi House"})

    def test_rejects_start_destination_and_unknown(self):
        out = Sink()
        result = read_closed_stations(
            METRO, "Rajiv Chowk", "Saket",
            scripted("", "Rajiv Chowk", "Atlantis", "Red Fort"), out)
        self.assertEqual(result, {"Red Fort"})
        self.assertEqual(len(out.lines), 3)


if __name__ == "__main__":
    unittest.main()
