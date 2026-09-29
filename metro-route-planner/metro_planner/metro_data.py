"""Metro network stored as an undirected weighted graph.

Structure:  { station: { neighbour_station: distance_in_km, ... }, ... }

Every connection appears in both directions (see graph.validate_network).
"""

METRO = {
    "Rajiv Chowk": {
        "Kashmere Gate": 3,
        "Central Secretariat": 2,
        "Mandi House": 2,
    },
    "Kashmere Gate": {
        "Rajiv Chowk": 3,
        "Chandni Chowk": 2,
        "Civil Lines": 2,
    },
    "Chandni Chowk": {
        "Kashmere Gate": 2,
        "Red Fort": 1,
    },
    "Red Fort": {
        "Chandni Chowk": 1,
        "Jama Masjid": 1,
    },
    "Jama Masjid": {
        "Red Fort": 1,
        "Delhi Gate": 2,
    },
    "Delhi Gate": {
        "Jama Masjid": 2,
        "Central Secretariat": 3,
    },
    "Central Secretariat": {
        "Rajiv Chowk": 2,
        "Delhi Gate": 3,
        "Hauz Khas": 6,
        "Mandi House": 2,
    },
    "Hauz Khas": {
        "Central Secretariat": 6,
        "Saket": 4,
    },
    "Saket": {
        "Hauz Khas": 4,
        "Qutub Minar": 3,
    },
    "Qutub Minar": {
        "Saket": 3,
    },
    "Mandi House": {
        "Rajiv Chowk": 2,
        "Central Secretariat": 2,
    },
    "Civil Lines": {
        "Kashmere Gate": 2,
    },
}
