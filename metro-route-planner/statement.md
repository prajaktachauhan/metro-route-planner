# Problem Statement

## Problem statement
Commuters in a large metro network often struggle to decide which sequence of
stations to take, how long the trip will take and how much it will cost. When a
station is closed for maintenance or an emergency, finding a workable detour by
hand is even harder. Existing solutions are usually full mobile apps; there is
a need for a small, transparent, easily testable system that shows how the
underlying route computation actually works.

## Scope of the project
**In scope**
- Model the metro network as a weighted, undirected graph (stations = nodes, distances in km = edges).
- Find the best route between any two stations by *shortest distance* (Dijkstra) or *fewest stations* (BFS).
- Compute total distance, estimated travel time and fare for a route.
- Handle one or more closed stations and compute an alternate route with a comparison against the original.
- Validate all user input, log activity and handle errors gracefully.
- Command-line interface with automated unit and end-to-end tests.

**Out of scope**
- Real-time train schedules, crowding or live status feeds.
- Interchange / line-change penalties and multiple metro lines.
- Graphical or web interface, ticket booking and payments.

## Target users
- Daily metro commuters and tourists who want a quick route, time and fare estimate.
- Metro operators / controllers who want to see the effect of closing a station.
- Students learning graph algorithms (Dijkstra, BFS) through a real-world example.

## High-level features
1. **Route finding** - Dijkstra (shortest distance) and BFS (fewest stations).
2. **Journey calculation** - distance, time (at 30 km/h) and slab-based fare.
3. **Closed-station rerouting** - one or many closed stations, with "no alternate" detection and an original-vs-alternate comparison.
4. **Robust input handling** - case-insensitive station names, yes/no and menu validation, re-prompting on every mistake.
5. **Logging and error handling** - file-based logs, custom exceptions, no raw tracebacks shown to users.
6. **Testing** - 50 automated tests covering the graph, algorithms, calculations, input and full workflow.
