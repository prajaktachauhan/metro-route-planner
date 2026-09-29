"""End-to-end tests: drive the whole CLI with scripted keyboard input."""

import unittest

from metro_planner.exceptions import NoRouteError
from metro_planner.metro_data import METRO
from metro_planner.planner import plan_journey, run_cli


def run(*answers):
    it = iter(answers)
    lines = []
    journeys = run_cli(METRO, lambda prompt="": next(it), lines.append)
    return journeys, "\n".join(lines)


class TestPlanJourney(unittest.TestCase):
    def test_journey_metrics(self):
        j = plan_journey(METRO, "Rajiv Chowk", "Delhi Gate")
        self.assertEqual((j.distance, j.time_minutes, j.fare, j.stops),
                         (5, 10.0, 20, 2))

    def test_no_route_propagates(self):
        with self.assertRaises(NoRouteError):
            plan_journey(METRO, "Rajiv Chowk", "Qutub Minar", {"Saket"})


class TestFullWorkflow(unittest.TestCase):
    def test_normal_journey_without_closure(self):
        journeys, out = run("Rajiv Chowk", "Qutub Minar", "1", "no")
        self.assertEqual(len(journeys), 1)
        self.assertIn("Rajiv Chowk -> Central Secretariat -> Hauz Khas", out)
        self.assertIn("Distance: 15 km", out)
        self.assertIn("Estimated Cost: Rs. 40", out)

    def test_alternate_route_flow(self):
        journeys, out = run("rajiv chowk", "delhi gate", "1", "yes",
                            "Central Secretariat")
        self.assertEqual(len(journeys), 2)
        self.assertIn("ALTERNATE ROUTE", out)
        self.assertIn("COMPARISON", out)
        self.assertEqual(journeys[1].distance, 9)

    def test_no_alternate_available(self):
        journeys, out = run("Rajiv Chowk", "Qutub Minar", "1", "yes", "Hauz Khas")
        self.assertEqual(len(journeys), 1)
        self.assertIn("No alternate route available.", out)

    def test_bad_inputs_are_recovered(self):
        journeys, out = run("Atlantis", "Saket", "Saket", "Hauz Khas",
                            "7", "2", "maybe", "no")
        self.assertEqual(len(journeys), 1)
        self.assertIn("Invalid station name", out)
        self.assertIn("other than Saket", out)
        self.assertIn("Invalid choice", out)
        self.assertIn("Please answer 'yes' or 'no'.", out)


if __name__ == "__main__":
    unittest.main()
