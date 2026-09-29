import unittest

from metro_planner.exceptions import (ClosedStationError,
                                      InvalidStationError, NoRouteError)
from metro_planner.metro_data import METRO
from metro_planner.route_finder import (bfs_route, dijkstra_route,
                                        find_route)

# Small graph where fewest-stops and shortest-distance disagree:
#   A-B-C-D  (1+1+1 = 3 km, 3 hops)   vs   A-D direct (10 km, 1 hop)
TRICKY = {
    "A": {"B": 1, "D": 10},
    "B": {"A": 1, "C": 1},
    "C": {"B": 1, "D": 1},
    "D": {"C": 1, "A": 10},
}


class TestDijkstra(unittest.TestCase):
    def test_simple_shortest_route(self):
        self.assertEqual(dijkstra_route(METRO, "Rajiv Chowk", "Delhi Gate"),
                         ["Rajiv Chowk", "Central Secretariat", "Delhi Gate"])

    def test_long_route_to_qutub_minar(self):
        route = dijkstra_route(METRO, "Rajiv Chowk", "Qutub Minar")
        self.assertEqual(route, ["Rajiv Chowk", "Central Secretariat",
                                 "Hauz Khas", "Saket", "Qutub Minar"])

    def test_prefers_distance_over_hops(self):
        self.assertEqual(dijkstra_route(TRICKY, "A", "D"), ["A", "B", "C", "D"])

    def test_same_start_and_destination(self):
        self.assertEqual(dijkstra_route(METRO, "Saket", "Saket"), ["Saket"])

    def test_route_is_symmetric_in_length(self):
        fwd = dijkstra_route(METRO, "Civil Lines", "Qutub Minar")
        back = dijkstra_route(METRO, "Qutub Minar", "Civil Lines")
        self.assertEqual(fwd, list(reversed(back)))


class TestClosedStations(unittest.TestCase):
    def test_alternate_route_avoids_closed_station(self):
        route = dijkstra_route(METRO, "Rajiv Chowk", "Delhi Gate",
                               {"Central Secretariat"})
        self.assertNotIn("Central Secretariat", route)
        self.assertEqual(route, ["Rajiv Chowk", "Kashmere Gate", "Chandni Chowk",
                                 "Red Fort", "Jama Masjid", "Delhi Gate"])

    def test_no_alternate_when_station_is_bottleneck(self):
        with self.assertRaises(NoRouteError):
            dijkstra_route(METRO, "Rajiv Chowk", "Qutub Minar", {"Hauz Khas"})

    def test_multiple_closed_stations(self):
        with self.assertRaises(NoRouteError):
            dijkstra_route(METRO, "Rajiv Chowk", "Delhi Gate",
                           {"Central Secretariat", "Jama Masjid"})

    def test_closed_start_or_destination_rejected(self):
        with self.assertRaises(ClosedStationError):
            dijkstra_route(METRO, "Saket", "Hauz Khas", {"Saket"})
        with self.assertRaises(ClosedStationError):
            bfs_route(METRO, "Saket", "Hauz Khas", {"Hauz Khas"})


class TestBfs(unittest.TestCase):
    def test_prefers_fewest_stops(self):
        self.assertEqual(bfs_route(TRICKY, "A", "D"), ["A", "D"])

    def test_bfs_respects_closed(self):
        route = bfs_route(METRO, "Rajiv Chowk", "Delhi Gate", {"Central Secretariat"})
        self.assertNotIn("Central Secretariat", route)


class TestValidationAndDispatch(unittest.TestCase):
    def test_unknown_station(self):
        with self.assertRaises(InvalidStationError):
            dijkstra_route(METRO, "Atlantis", "Saket")
        with self.assertRaises(InvalidStationError):
            dijkstra_route(METRO, "Saket", "Rajiv Chowk", {"Atlantis"})

    def test_disconnected_graph(self):
        split = {"A": {}, "B": {}}
        with self.assertRaises(NoRouteError):
            dijkstra_route(split, "A", "B")

    def test_find_route_dispatch(self):
        self.assertEqual(find_route(TRICKY, "A", "D", criterion="distance"),
                         ["A", "B", "C", "D"])
        self.assertEqual(find_route(TRICKY, "A", "D", criterion="stops"),
                         ["A", "D"])

    def test_unknown_criterion(self):
        with self.assertRaises(ValueError):
            find_route(TRICKY, "A", "D", criterion="cheapest")


if __name__ == "__main__":
    unittest.main()
